_C='spark-submit'
_B=False
_A='2.2.1'
import glob,logging,os,textwrap
from typing import Dict,List
from localstack.constants import MAVEN_REPO_URL
from localstack.packages import InstallTarget,Package,PackageInstaller
from localstack.packages.core import ArchiveDownloadAndExtractInstaller
from localstack.utils.archives import unzip
from localstack.utils.collections import select_attributes
from localstack.utils.docker_utils import DOCKER_CLIENT
from localstack.utils.files import cp_r,file_exists_not_empty,load_file,mkdir,new_tmp_dir,new_tmp_file,rm_rf,save_file
from localstack.utils.http import download
from localstack.utils.run import run,to_str
from localstack.utils.testutil import create_zip_file
from localstack_ext import config as ext_config
LOG=logging.getLogger(__name__)
SPARK_URL='https://archive.apache.org/dist/spark/spark-{version}/spark-{version}-bin-without-hadoop.tgz'
DEFAULT_SPARK_VERSION='2.4.3'
SPARK_VERSIONS=[DEFAULT_SPARK_VERSION,_A,'2.4.8','3.1.1','3.1.2']
AWS_SDK_VER='1.12.339'
HADOOP_VERSION='2.9.2'
JAR_URLS=[f"{MAVEN_REPO_URL}/com/amazonaws/aws-java-sdk-bundle/{AWS_SDK_VER}/aws-java-sdk-bundle-{AWS_SDK_VER}.jar",f"{MAVEN_REPO_URL}/org/apache/hadoop/hadoop-hdfs/{HADOOP_VERSION}/hadoop-hdfs-{HADOOP_VERSION}.jar",f"{MAVEN_REPO_URL}/org/apache/hadoop/hadoop-common/{HADOOP_VERSION}/hadoop-common-{HADOOP_VERSION}.jar",f"{MAVEN_REPO_URL}/org/apache/hadoop/hadoop-auth/{HADOOP_VERSION}/hadoop-auth-{HADOOP_VERSION}.jar",f"{MAVEN_REPO_URL}/org/apache/hadoop/hadoop-aws/{HADOOP_VERSION}/hadoop-aws-{HADOOP_VERSION}.jar",f"{MAVEN_REPO_URL}/com/typesafe/config/1.3.3/config-1.3.3.jar",f"{MAVEN_REPO_URL}/com/fasterxml/jackson/dataformat/jackson-dataformat-csv/2.11.4/jackson-dataformat-csv-2.11.4.jar",f"{MAVEN_REPO_URL}/com/fasterxml/jackson/core/jackson-core/2.11.4/jackson-core-2.11.4.jar",f"{MAVEN_REPO_URL}/com/github/tony19/named-regexp/0.2.6/named-regexp-0.2.6.jar",f"{MAVEN_REPO_URL}/com/amazon/emr/emr-dynamodb-hadoop/4.12.0/emr-dynamodb-hadoop-4.12.0.jar",f"{MAVEN_REPO_URL}/de/undercouch/bson4jackson/2.11.0/bson4jackson-2.11.0.jar",f"{MAVEN_REPO_URL}/com/google/guava/guava/30.0-jre/guava-30.0-jre.jar",f"{MAVEN_REPO_URL}/org/apache/commons/commons-configuration2/2.7/commons-configuration2-2.7.jar",f"{MAVEN_REPO_URL}/commons-configuration/commons-configuration/1.10/commons-configuration-1.10.jar",f"{MAVEN_REPO_URL}/org/apache/commons/commons-text/1.9/commons-text-1.9.jar",f"{MAVEN_REPO_URL}/commons-lang/commons-lang/2.6/commons-lang-2.6.jar",f"{MAVEN_REPO_URL}/org/apache/logging/log4j/log4j-api/2.14.0/log4j-api-2.14.0.jar",f"{MAVEN_REPO_URL}/org/postgresql/postgresql/42.3.1/postgresql-42.3.1.jar",f"{MAVEN_REPO_URL}/com/google/guava/failureaccess/1.0.1/failureaccess-1.0.1.jar",f"{MAVEN_REPO_URL}/org/apache/hadoop/thirdparty/hadoop-shaded-protobuf_3_7/1.0.0/hadoop-shaded-protobuf_3_7-1.0.0.jar",f"{MAVEN_REPO_URL}/com/google/re2j/re2j/1.5/re2j-1.5.jar"]
REPO_URL_GLUE_LIBS='git+https://github.com/awslabs/aws-glue-libs.git#egg=aws-glue-libs'
REPO_URL_GLUE_LIBS_0_9='git+https://github.com/localstack/aws-glue-libs.git@glue-0.9#egg=aws-glue-libs'
BIGDATA_CONTAINER_NAME='localstack_bigdata'
EXTERNAL_CONTAINER_DEFAULT_SPARK_HOME='/usr/local/spark-2.4.3-bin-without-hadoop-scala-2.12'
class SparkPackage(Package):
	def __init__(A):super().__init__('Spark',default_version=DEFAULT_SPARK_VERSION)
	def get_versions(A):return SPARK_VERSIONS
	def _get_installer(A,version):return SparkInstaller(version)
class SparkInstaller(ArchiveDownloadAndExtractInstaller):
	def __init__(A,version):super().__init__(name='spark',version=version,extract_single_directory=True)
	def get_installed_dir(B):
		A=super().get_installed_dir()
		if A:
			if ext_config.BIGDATA_MONO_CONTAINER:return A
			C=f"/usr/local/spark-{B.version}"
			if path_exists_mono_and_external(C):return A
	def _get_download_url(A):return SPARK_URL.format(version=A.version)
	def _get_install_marker_path(A,install_dir):return os.path.join(install_dir,'bin',_C)
	def _post_process(A,target):B=A._get_install_dir(target);D=A._get_install_marker_path(B);C=f"/usr/local/spark-{A.version}";E=os.path.join(C,'bin',_C);copy_local_into_external(B,D,C,E);post_process_spark(A)
spark_package=SparkPackage()
def copy_local_into_external(mono_spark_home,mono_spark_submit,external_spark_home,external_spark_submit):
	C=mono_spark_submit;B=external_spark_home;A=mono_spark_home
	if ext_config.BIGDATA_MONO_CONTAINER:return
	if path_exists_mono_and_external(external_spark_submit):return
	if not os.path.exists(C):
		LOG.warning("Unable to find 'spark-submit' in the downloaded archive: %s",C)
		if not os.path.exists(A):LOG.warning('Target installation dir does not exist: %s',A)
		return
	LOG.debug('Copying Spark installation into bigdata container: %s',B);copy_mono_and_external(A,B);D=['cp',f"{EXTERNAL_CONTAINER_DEFAULT_SPARK_HOME}/conf/spark-env.sh",f"{B}/conf/spark-env.sh"];run_mono_and_external(D)
def post_process_spark(installer=None):
	A=installer;A=A or spark_package.get_installer()
	if ext_config.BIGDATA_MONO_CONTAINER:B=A.get_installed_dir()
	else:B=f"/usr/local/spark-{A.version}"
	patch_spark_class(B);patch_spark_defaults(B)
	if ext_config.BIGDATA_MONO_CONTAINER:post_process_spark_mono_container(A)
def post_process_spark_mono_container(installer):
	A=installer
	if not ext_config.BIGDATA_MONO_CONTAINER:return
	B=A.get_installed_dir();install_hadoop_for_spark(A);install_awsglue_local(A);patch_additional_jar_files(B);patch_spark_python_dependencies(B)
	if A.version.startswith('2.'):from localstack_ext.packages.java import java_package as C;C.get_installer('8').install()
def patch_spark_class(spark_home):A=['sed','-ie','$s/^exec "\\${CMD\\[@]}"/if [ -n "$SPARK_OVERWRITE_CP" ]; then CMD[2]="$SPARK_OVERWRITE_CP:${CMD[2]}"; fi\\nCMD=("${CMD[0]}" "-Dcom.amazonaws.sdk.disableCertChecking=true" "${CMD[@]:1}"); exec "${CMD[@]}"/',f"{spark_home}/bin/spark-class"];run_mono_and_external(A)
def patch_spark_defaults(spark_home):A=new_tmp_file();B=textwrap.dedent(f"spark.driver.extraClassPath {spark_jar_lib_location()}/*\n    spark.executor.extraClassPath {spark_jar_lib_location()}/*\n    spark.driver.allowMultipleContexts = true\n    ");save_file(A,B);copy_mono_and_external(A,f"{spark_home}/conf/spark-defaults.conf");rm_rf(A)
def install_hadoop_for_spark(spark_installer):
	C=spark_installer;from localstack_ext.packages.hadoop import hadoop_package as F;G=get_hadoop_version_for_spark_version(C.version);D=F.get_installer(G);D.install();A=D.get_installed_dir();E=os.listdir(A)
	if len(E)==1:A=os.path.join(A,E[0])
	H=os.path.join(A,'bin/hadoop')
	if not os.path.exists(H):raise Exception(f"Hadoop not fully installed in directory {A}")
	B=new_tmp_file();I=f'\n    export SPARK_DIST_CLASSPATH="$({A}/bin/hadoop classpath)"\n    export HADOOP_CONF_DIR="{A}/etc/hadoop"\n    ';save_file(B,I);copy_mono_and_external(B,f"{C.get_installed_dir()}/conf/spark-env.sh");rm_rf(B)
def install_awsglue_local(spark_installer):
	A=REPO_URL_GLUE_LIBS
	if spark_installer.version==_A:A=REPO_URL_GLUE_LIBS_0_9
	B=['pip','install',A];run(B)
def patch_additional_jar_files(spark_home):
	download_additional_jar_files();B=f"{spark_home}/conf/spark-defaults.conf";A=load_file(B)
	if'/gluePyspark'not in A:A+=f"\nspark.driver.extraClassPath {spark_jar_lib_location()}/*\nspark.executor.extraClassPath {spark_jar_lib_location()}/*\nspark.driver.allowMultipleContexts = true\n";save_file(B,A)
def patch_spark_python_dependencies(spark_home):C=spark_home;A=os.path.join(C,'python/lib/py4j-*-src.zip');A=glob.glob(A)[0];B={'from collections import':'from collections.abc import'};replace_in_zip_file(A,'py4j/java_collections.py',B);A=os.path.join(C,'python/lib/pyspark.zip');B={'import collections\n':'import collections.abc\n','collections.Iterable':'collections.abc.Iterable'};replace_in_zip_file(A,'pyspark/resultiterable.py',B);B={'_cell_set_template_code =':'# _cell_set_template_code ='};replace_in_zip_file(A,'pyspark/cloudpickle.py',B)
def replace_in_zip_file(zip_file,file_path,search_replace,raise_if_missing=_B):
	C=zip_file;A=new_tmp_dir();unzip(C,A);B=os.path.join(A,file_path)
	if not os.path.exists(B):
		if raise_if_missing:raise Exception(f"Unable to replace content in non-existing file in archive: {B}")
		return
	replace_in_file(B,search_replace);create_zip_file(A,C);rm_rf(A)
def replace_in_file(file_path,search_replace):
	B=file_path;A=load_file(B)
	for (C,D) in search_replace.items():A=A.replace(C,D)
	save_file(B,A)
def get_hadoop_version_for_spark_version(spark_version):
	from localstack_ext.packages.hadoop import HADOOP_DEFAULT_VERSION as A
	if ext_config.BIGDATA_MONO_CONTAINER and spark_version==_A:return'2.10.2'
	return A
def get_spark_install_cache_dir(spark_version):A=spark_package.get_installer(spark_version);return A.get_installed_dir()or A._get_install_dir(InstallTarget.VAR_LIBS)
def download_additional_jar_files():
	for A in JAR_URLS:download_and_cache_jar_file(A)
	return spark_jar_lib_location()
def download_and_cache_jar_file(jar_url):
	B=jar_url;mkdir(spark_jar_lib_location());C=os.path.join(spark_jar_lib_location(),B.split('/')[-1])
	if file_exists_not_empty(C):return C
	A=os.path.join(spark_jar_lib_location(cache=True),B.split('/')[-1])
	if not file_exists_not_empty(A):download(B,A)
	cp_r(A,C);return A
def spark_jar_lib_location(cache=_B):
	if ext_config.BIGDATA_MONO_CONTAINER:A=spark_package.get_installed_dir();B=os.path.dirname(os.path.dirname(A));return os.path.join(B,'gluePyspark'if not cache else'bigdata-jars')
	else:return'/usr/local/gluePyspark'
def mono_and_external_spark_home(spark_version):
	if ext_config.BIGDATA_MONO_CONTAINER:return spark_package.get_installed_dir()
	return f"/usr/local/spark-{spark_version}"
def run_mono_and_external(command,**A):
	B=command
	if ext_config.BIGDATA_MONO_CONTAINER:A=select_attributes(A,['env_vars']);return run(B,**A)
	else:A=select_attributes(A,['env','stdin','stdout','stderr','cwd','shell']);C,D=DOCKER_CLIENT.exec_in_container(BIGDATA_CONTAINER_NAME,B,**A);return to_str(C or'')
def path_exists_mono_and_external(path):
	try:run_mono_and_external(['test','-e',path]);return True
	except Exception:return _B
def copy_mono_and_external(source_path,target_path):
	B=source_path;A=target_path
	if ext_config.BIGDATA_MONO_CONTAINER:
		if os.path.realpath(B)==os.path.realpath(A):return
		mkdir(os.path.dirname(A));cp_r(B,A)
	else:DOCKER_CLIENT.copy_into_container(BIGDATA_CONTAINER_NAME,B,A)