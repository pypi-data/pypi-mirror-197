"""
spark-helper

在k8s集群中调用spark (https://github.com/GoogleCloudPlatform/spark-on-k8s-operator)

Author: yuchao.li@liangdao.ai
Created: 2023.3.9

Usage:
    s3_config = {'endpoint': 'http://minio.minio-tenant',
                'access': 'xxx',
                'secret': 'xxx'}

    set_config(image='pyspark:driver-3.3.1',
               namespace='spark-operator',
               service_account='sparkoperator',
               s3_config = s3_config )

    start_spark('hello-world-spark',
                's3a://airflow-dags/spark/pyspark_helloworld.py',
                False)

配置优先级：
    从高到低
    set_config 设置的配置
    auto_load_config 自动加载的环境变量配置
"""

import os
import yaml
import copy
import time

from kubernetes import config, dynamic
from kubernetes.client import api_client

SPARK_YAML_TEMPLATE = """
apiVersion: "sparkoperator.k8s.io/v1beta2"
kind: SparkApplication
metadata:
  name: start-from-yaml
  namespace: spark-operator 
spec:
  type: Python
  pythonVersion: "3"
  mode: cluster
  image: 295313735635.dkr.ecr.cn-north-1.amazonaws.com.cn/pyspark:driver-3.3.1
  imagePullPolicy: Always
  imagePullSecrets:
    - regcred
  mainApplicationFile: s3a://airflow-dags/spark/pyspark_helloworld.py  # s3
  sparkVersion: "3.1.1"
  sparkConf:
    spark.hadoop.fs.s3a.endpoint: http://minio.minio-tenant
    spark.hadoop.fs.s3a.access.key: access
    spark.hadoop.fs.s3a.secret.key: secret
    spark.hadoop.fs.s3a.path.style.access: "true"
    spark.hadoop.fs.s3a.connection.sslenabled: "false"
    spark.hadoop.fs.s3a.impl: org.apache.hadoop.fs.s3a.S3AFileSystem
    spark.hadoop.fs.s3a.aws.credentials.provider: org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider
  driver:
    serviceAccount: sparkoperator
    env:
    - name: SPARK_PYTHON
      value: /opt/spark/python
  executor:
    env:
    - name: SPARK_PYTHON
      value: /opt/spark/python    
"""

G_CONFIG = yaml.load(SPARK_YAML_TEMPLATE, yaml.FullLoader)


def create_spark(yaml_obj, in_cluster):
    """
        创建一个spark任务
    """
    if in_cluster:
        config.load_incluster_config()
    else:
        config.load_kube_config()

    client = dynamic.DynamicClient(api_client.ApiClient())
    crd_api = client.resources.get(api_version='sparkoperator.k8s.io/v1beta2',
                                   kind='SparkApplication')

    crd_creation_response = crd_api.create(yaml_obj)

    print('\n[INFO] Spark appliaction created\n')
    print('%s\t\t%s' % ('SCOPE', 'NAME'))
    print('%s\t\t%s\n' % (crd_creation_response.spec.scope,
                          crd_creation_response.metadata.name))

    crd_api.current_namespace = yaml_obj['metadata']['namespace']
    crd_api.current_name = yaml_obj['metadata']['name']

    return True, crd_api


def set_config(image='', namespace='', service_account='', s3_config=None):
    """
        加载部分配置
        说明:
            image pyspark镜像
            namespace和service_account决定了spark程序运行的空间和权限
            在指定的namespace中, service_account必须有建立spark application的权限
            s3_config {
                        endpoint: '',
                        access: '',
                        secret: '',
                      }

    """
    global G_CONFIG

    if image:
        G_CONFIG['spec']['image'] = image

    if namespace and service_account:
        G_CONFIG['metadata']['namespace'] = namespace
        G_CONFIG['spec']['driver']['serviceAccount'] = service_account

    if s3_config:
        conf = G_CONFIG['spec']['sparkConf']
        conf['spark.hadoop.fs.s3a.endpoint'] = s3_config['endpoint']
        conf['spark.hadoop.fs.s3a.access.key'] = s3_config['access']
        conf['spark.hadoop.fs.s3a.secret.key'] = s3_config['secret']


def auto_load_config():
    """
        自动加载配置，环境变量以及s3(MINIO)配置读取
        策略:
            环境变量 MINIO_URL: spark.hadoop.fs.s3a.endpoint
            文件 /etc/minio-password: MINIO的 access:secret
    """

    s3_config = G_CONFIG['spec']['sparkConf']
    endpoint = os.getenv('MINIO_URL')
    if endpoint:
        s3_config['spark.hadoop.fs.s3a.endpoint'] = endpoint

    if os.access('/etc/minio-password', os.F_OK):
        with open('/etc/minio-password', 'r', encoding='utf8') as f:
            content = f.read()
            clist = content.rstrip().split(':')
            s3_config['spark.hadoop.fs.s3a.access.key'] = clist[0]
            s3_config['spark.hadoop.fs.s3a.secret.key'] = clist[1]


def start_spark_from_yaml(yaml_string, in_cluster=True):
    """
        使用yaml启动一个spark任务
        yaml_string: 可以提交至spark-operator并成功启动的yaml代码
        in_cluster: 是否在集群内部调用
    """

    obj = yaml.load(yaml_string, yaml.FullLoader)
    return create_spark(obj, in_cluster)


def start_spark(task_name, app_file, in_cluster=True):
    """
        启动一个spark任务
        task_name: 任务名称，唯一, 支持小写字母和数字以及-，不支持下划线
        app_file: 代码位置，支持local和s3a
                  * local:///pyspark_helloworld.py
                  * s3a://airflow-dags/spark/pyspark_helloworld.py
        in_cluster: 是否在集群内部调用

        返回:
            True, crd对象(可用于后续查询任务状态)
        或抛出kubernetes.client错误
    """
    auto_load_config()

    obj = copy.deepcopy(G_CONFIG)
    obj['metadata']['name'] = task_name
    obj['spec']['mainApplicationFile'] = app_file

    return create_spark(obj, in_cluster)


def get_spark_status(crd_api):
    """
        获取当前状态
            crd_api: 使用start_spark返回的crd对象
    """
    result = crd_api.get(namespace=crd_api.current_namespace,
                         name=crd_api.current_name)
    print(result)
    if result is None:
        return 'NOT FOUND'

    if result['status'] is None:
        return 'INIT'

    return result['status']['applicationState']['state']


__all__ = [
    'start_spark', 'start_spark_from_yaml', 'get_spark_status',
    'SPARK_YAML_TEMPLATE'
]


def test():
    _, crd_api = start_spark('hello-world-spark',
                             's3a://airflow-dags/spark/pyspark_helloworld.py',
                             False)

    time.sleep(3)
    while get_spark_status(crd_api) not in [
            'COMPLETED', 'FAILED', 'NOT FOUND'
    ]:
        print('waiting...')
        time.sleep(1)

    print(f'Done: task {get_spark_status(crd_api)}')


if __name__ == '__main__':
    test()
