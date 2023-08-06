_F='location'
_E='pod_name'
_D='max_version'
_C='presigned_urls'
_B=True
_A=False
import json,logging
from abc import ABC,abstractmethod
from dataclasses import dataclass
from typing import Dict,List,Optional,Set,Tuple
import requests,yaml
from localstack import constants
from localstack.utils.files import new_tmp_file
from localstack.utils.http import download,safe_requests
from localstack.utils.objects import get_all_subclasses
from localstack.utils.strings import to_str
from requests import Response
from localstack_ext.bootstrap.licensing import get_auth_headers
from localstack_ext.bootstrap.pods.client_api import CloudPodsClientApi
from localstack_ext.bootstrap.pods.utils.common import PodsConfigContext
LOG=logging.getLogger(__name__)
@dataclass
class RemoteConfig:remote_url:str
class CloudPodsRemote(ABC):
	config_context:PodsConfigContext;remote_config:RemoteConfig
	def __init__(A,config_context,remote_config):A.remote_config=remote_config;A.pods_api=CloudPodsClientApi(config_context)
	@classmethod
	@abstractmethod
	def protocols(cls):0
	@abstractmethod
	def list_pods(self):0
	@abstractmethod
	def get_max_version(self,pod_name):0
	@abstractmethod
	def pull_versions(self,pod_name,required_versions):0
	@abstractmethod
	def is_registered(self,pod_name):0
	def push_pod(A,pod_name,version,overwrite=_A):0
	def register_remote(A,pod_name,ci_pod=None):0
	def rename_pod(A,current_name,new_name):0
	def delete_pod(A,pod_name):0
	@classmethod
	def get_for_protocol(E,protocol,**C):
		A=protocol;D=get_all_subclasses(CloudPodsRemote)
		for B in D:
			if A in B.protocols():return B(**C)
		raise Exception(f"Unable to find cloud pod remote implementation for protocol '{A}'")
class CloudPodsRemotePlatform(CloudPodsRemote):
	@classmethod
	def protocols(A):return{'platform'}
	def get_max_version(A,pod_name):
		C=A.create_platform_url(pod_name);D=get_auth_headers();B=safe_requests.get(url=C,headers=D);E='Failed to get version information from platform.. aborting'
		if not A._check_response(B,message=E,raise_error=_B):return
		F=json.loads(B.content);G=int(F[_D]);return G
	def pull_versions(A,pod_name,required_versions):
		D=','.join((str(A)for A in required_versions));E=A.create_platform_url(f"{pod_name}/data?versions={D}");F=get_auth_headers();C=safe_requests.get(url=E,headers=F);G='Failed to pull requested versions from platform (code <status_code>)'
		if not A._check_response(C,message=G,raise_error=_B):return
		H=json.loads(C.content);B=A._prepare_archives_from_pre_signed_urls(H);I=B[0];J=B[1];K=B[2];A.pods_api.merge_from_remote(version_space_archive=I,meta_archives=J,state_archives=K)
	def push_pod(A,pod_name,version,overwrite=_A):
		B=A.create_platform_url(f"{pod_name}/data?version={version}")
		if overwrite:B+='&overwrite=true'
		D=get_auth_headers();C=safe_requests.post(url=B,headers=D);E='Failed to get presigned URLs to upload new version.. aborting'
		if not A._check_response(C,message=E):return
		F=json.loads(C.content);G=F.get(_C);A.pods_api.upload_version_and_product_space(presigned_urls=G)
	def list_pods(A):C=get_auth_headers();D=A.create_platform_url();B=safe_requests.get(D,headers=C);A._check_response(B,message='Error fetching list of pods from API (status <status_code>)',raise_error=_B);E=json.loads(B.content);return E
	def delete_pod(A,pod_name):B=A.create_platform_url(pod_name);C=get_auth_headers();D=safe_requests.delete(url=B,headers=C);return D.ok
	def is_registered(G,pod_name):
		A=pod_name
		try:C=CloudPodsRemotePlatform.create_platform_url();D=get_auth_headers();B=safe_requests.get(C,headers=D)
		except Exception as E:LOG.debug('An error occurred while checking remote management for pod "%s": "%s"',A,E);return _A
		if not B.ok:return _A
		F=json.loads(B.content);return A in[A[_E]for A in F]
	def register_remote(A,pod_name,ci_pod=None):
		B=pod_name;C=A.pods_api.get_max_version_no(require_state_archive=_B)
		if C==0:A.pods_api.push('Initial Version');C=1
		F=get_auth_headers();G=A.create_platform_url(B);D={_E:B,_D:C,'ci_pod':ci_pod};D=json.dumps(D);E=safe_requests.put(G,D,headers=F);H=f"Failed to register pod {B}: <content>"
		if not A._check_response(E,message=H):return _A
		I=json.loads(E.content);J=I.get(_C);A.pods_api.upload_version_and_product_space(presigned_urls=J);return _B
	def rename_pod(B,current_name,new_name):D=new_name;C=current_name;E=get_auth_headers();F=B.create_platform_url(f"{C}/rename");A={'new_pod_name':D};A=json.dumps(A);G=safe_requests.put(F,A,headers=E);H=f"Failed to rename {C} to {D}: <content>";return B._check_response(G,message=H)
	@staticmethod
	def create_platform_url(path=None):
		A=path;B=f"{constants.API_ENDPOINT}/cloudpods"
		if not A:return B
		A=A if A.startswith('/')else f"/{A}";return f"{B}{A}"
	@classmethod
	def _check_response(C,response,message,raise_error=_A):
		B=response;A=message
		if B.ok:return _B
		if B.status_code in[401,403]:raise Exception('Access denied - please log in first.')
		A=A.replace('<content>',to_str(B.content));A=A.replace('<status_code>',str(B.status_code))
		if raise_error:raise Exception(A)
		LOG.warning(A);return _A
	@staticmethod
	def _prepare_archives_from_pre_signed_urls(content):
		A=new_tmp_file();B=content.get(_C);I=B.get('version_space_url');download(url=I,path=A);C={};D={};J=B.get('meta_state_urls')
		for (E,F) in J.items():G=new_tmp_file();H=new_tmp_file();K=F['meta'];L=F['state'];download(K,G);download(L,H);D[E]=G;C[E]=H
		return A,D,C
	def _get_presigned_url_for_version_product(B,pod_name,version):
		C=pod_name;A=version;D=B.create_platform_url(f"{C}/version/product")
		if A!=-1:D+=f"?version={A}"
		F=get_auth_headers();E=safe_requests.get(D,headers=F);G=f"Failed to retrieve presigned URL from remote for version {A} of pod {C}"
		if not B._check_response(E,message=G,raise_error=_B):return
		return json.loads(E.content)
class CloudPodsRemoteGithub(CloudPodsRemote):
	@classmethod
	def protocols(A):return{'github'}
	def list_pods(A):raise NotImplementedError
	def get_max_version(A,pod_name):return 1
	def is_registered(A,pod_name):return _A
	def pull_versions(C,pod_name,required_versions):
		A=pod_name;LOG.debug('Pulling versions of cloud pod `%s` from Github remote',A);F,A=C._repo_and_pod_name(A);I=C._base_url(F);G=f"{I}/cloudpods.yml";D=requests.get(G)
		if not D.ok:raise Exception(f"Unable to fetch cloudpods.yml from URL {G}: {D.status_code} {D.content}")
		E=yaml.safe_load(to_str(D.content));B=[B for B in E.get('pods',[])if B.get('name')==A]
		if not B:raise Exception(f"Unable to find config for pod `{A}` in cloudpods.yml: {E}")
		B=B[0];J=B.get(_F)
		if not J:raise Exception(f"Unable to find config for pod `{A}` in cloudpods.yml: {E}")
		K=C._pod_zip_url(F,B);H=new_tmp_file();download(K,H);C.pods_api.merge_from_remote(version_space_archive=H,meta_archives={},state_archives={})
	def _repo_and_pod_name(B,pod_name):A=pod_name.rpartition('/');return A[0],A[2]
	def _pod_zip_url(C,repo_name,pod_config):
		B=pod_config;A=B.get(_F)
		if not A:raise Exception(f"Unable to find `location` for pod in cloudpods.yml: {B}")
		D=C._base_url(repo_name);A=A.removeprefix('./');E=f"{D}/{A}";return E
	def _base_url(A,repo_name):return f"https://raw.githubusercontent.com/{repo_name}/main"