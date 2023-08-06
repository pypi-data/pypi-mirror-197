from localstack.runtime import hooks
@hooks.on_infra_start()
def _run_dill_patch():from localstack_ext.bootstrap.pods.server.persistence import patch_cryptography_pickling as A;A()