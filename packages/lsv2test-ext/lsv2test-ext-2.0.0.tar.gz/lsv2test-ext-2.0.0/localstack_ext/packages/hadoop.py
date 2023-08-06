_B='hadoop'
_A='2.10.2'
import glob,os
from typing import List
from localstack import config
from localstack.constants import MAVEN_REPO_URL
from localstack.packages import InstallTarget,Package
from localstack.packages.core import ArchiveDownloadAndExtractInstaller
from localstack.utils.files import file_exists_not_empty,rm_rf,save_file
from localstack.utils.http import download
from localstack_ext import config as ext_config
from localstack_ext.packages.spark import AWS_SDK_VER
URL_PATTERN_HADOOP='https://downloads.apache.org/hadoop/common/hadoop-{version}/hadoop-{version}.tar.gz'
AWS_SDK_BUNDLE_JAR=f"aws-java-sdk-bundle-{AWS_SDK_VER}.jar"
AWS_SDK_BUNDLE_JAR_URL=f"{MAVEN_REPO_URL}/com/amazonaws/aws-java-sdk-bundle/{AWS_SDK_VER}/{AWS_SDK_BUNDLE_JAR}"
HADOOP_DEFAULT_VERSION=_A
if ext_config.BIGDATA_MONO_CONTAINER:HADOOP_DEFAULT_VERSION='3.3.1'
HADOOP_VERSIONS=[_A,'3.3.1']
class HadoopInstaller(ArchiveDownloadAndExtractInstaller):
	def __init__(A,version):super().__init__(name=_B,version=version,extract_single_directory=True)
	def _get_download_url(A):return URL_PATTERN_HADOOP.format(version=A.version)
	def _get_install_marker_path(A,install_dir):return os.path.join(install_dir,'bin',_B)
	def is_installed(A):
		if not ext_config.BIGDATA_MONO_CONTAINER:return True
		return super().is_installed()
	def get_hadoop_home(A):return get_hadoop_home_in_container(A.version)
	def _post_process(F,target):
		from localstack_ext.utils.bigdata.bigdata_utils import HADOOP_FS_S3_PROPS as G
		if not ext_config.BIGDATA_MONO_CONTAINER:return
		B=F.get_hadoop_home();A='\n'.join((f"<property><name>{A}</name><value>{B}</value></property>"for(A,B)in G.items()));H=config.service_url('s3');A=A.format(s3_endpoint=H);I=f"""
          <configuration>
            <property>
              <name>fs.defaultFS</name>
              <value>file://{config.TMP_FOLDER}/hadoop-fs</value>
            </property>
            <property>
              <name>fs.default.name</name>
              <value>file://{config.TMP_FOLDER}/hadoop-fs</value>
            </property>
            {A}
          </configuration>
        """;save_file(os.path.join(B,'etc/hadoop/core-site.xml'),I);C=os.path.join(B,'share/hadoop/tools/lib');D=glob.glob(os.path.join(C,'aws-java-sdk-*.jar'))
		for J in D:rm_rf(J)
		if D:
			E=os.path.join(C,AWS_SDK_BUNDLE_JAR)
			if not file_exists_not_empty(E):download(AWS_SDK_BUNDLE_JAR_URL,E)
class HadoopPackage(Package):
	def __init__(A,default_version=HADOOP_DEFAULT_VERSION):super().__init__(name='Hadoop',default_version=default_version)
	def get_versions(A):return HADOOP_VERSIONS
	def _get_installer(A,version):return HadoopInstaller(version)
hadoop_package=HadoopPackage()
def get_hadoop_home_in_container(hadoop_version=None):
	B=hadoop_version;B=B or HADOOP_DEFAULT_VERSION;D=hadoop_package.get_installer(B);A=D.get_installed_dir();C=os.listdir(A)
	if len(C)==1:A=os.path.join(A,C[0])
	E=os.path.join(A,'bin/hadoop')
	if not os.path.exists(E):raise Exception(f"Hadoop not fully installed in directory {A}")
	return A