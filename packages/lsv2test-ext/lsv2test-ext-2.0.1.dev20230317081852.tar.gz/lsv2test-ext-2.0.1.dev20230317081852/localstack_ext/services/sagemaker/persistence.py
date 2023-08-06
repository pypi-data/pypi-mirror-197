_A='sagemaker'
from localstack_ext.bootstrap.pods.server.plugins import StateLifecyclePlugin
def restore_endpoints(*E):
	from localstack_ext.services.sagemaker.models import sagemaker_stores as A
	for (F,B) in A.items():
		for (G,C) in B.items():
			for (H,D) in C.endpoints.items():D.redeploy()
def shutdown_endpoints(*E):
	from localstack_ext.services.sagemaker.models import sagemaker_stores as A
	for B in A.values():
		for C in B.values():
			for D in C.endpoints.values():D.shutdown_all()
class SageMakerPersistenceLifeCycle(StateLifecyclePlugin):
	name=_A;service=_A
	def inject_assets(A,pod_asset_directory):super().inject_assets(pod_asset_directory);restore_endpoints()