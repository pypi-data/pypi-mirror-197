import logging,os
from typing import Dict,Optional
from localstack import config
from localstack.utils.files import cp_r,rm_rf
from plugin import Plugin
LOG=logging.getLogger(__name__)
class StateLifecyclePlugin(Plugin):
	namespace='localstack.state.lifecycle';service:str
	def get_assets_location(A):B=config.dirs.data;return os.path.join(B,A.service)
	def has_assets(B):
		A=B.get_assets_location()
		if os.path.exists(A)and len(os.listdir(A))>0:return True
		return False
	def retrieve_assets(I):
		A=I.get_assets_location();B={}
		if not os.path.isdir(A):return B
		for (D,J,G) in os.walk(A,topdown=True):
			for E in G:
				C=os.path.relpath(D,A);K=os.path.join(C,E)if C!='.'else E;H=os.path.join(D,E)
				if os.path.isfile(H):F=K;L=_load_asset_binary(H);B[F]=L
			if not G and not J:C=os.path.relpath(D,A);F=C+'/';B[F]=''
		return B
	def inject_assets(A,pod_asset_directory):
		B=A.get_assets_location();C=os.path.join(pod_asset_directory,A.service);rm_rf(B)
		if os.path.exists(C):cp_r(C,B)
	def reset_state(A):A.on_after_reset()
	def on_after_reset(A):0
def _load_asset_binary(file_path):
	A=file_path
	try:
		with open(A,'rb')as B:return B.read()
	except Exception as C:LOG.warning(f"Could not load assets binary for file {A} due to {C}.");return None