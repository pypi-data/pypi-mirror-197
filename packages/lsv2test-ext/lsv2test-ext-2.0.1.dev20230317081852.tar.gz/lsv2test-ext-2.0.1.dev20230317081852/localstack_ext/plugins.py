_J='Unable to start DNS: %s'
_I='neptune'
_H='transfer'
_G='mediastore'
_F='elasticache'
_E='apigatewayv2'
_D='apigateway'
_C='athena'
_B='s3'
_A='rds'
import logging,os
from localstack import config as localstack_config
from localstack.runtime import hooks
from localstack.runtime.hooks import on_infra_ready
from localstack.utils import net
from localstack.utils.bootstrap import API_DEPENDENCIES,LocalstackContainer,get_enabled_apis
from localstack.utils.container_utils.container_client import VolumeBind
from localstack_ext import config as config_ext
from localstack_ext.bootstrap import licensing,local_daemon
from localstack_ext.bootstrap.licensing import is_enterprise
LOG=logging.getLogger(__name__)
EXTERNAL_PORT_APIS=_D,_E,_C,'cloudfront','codecommit','ecs','ecr',_F,_G,_A,_H,'kafka',_I,'azure'
API_DEPENDENCIES.update({'amplify':[_B,'appsync','cognito'],_D:[_E],_C:['emr'],'docdb':[_A],'ecs':['ecr'],_F:['ec2'],'elb':['elbv2'],'emr':[_C,_B],'glacier':[_B],'glue':[_A],'iot':['iotanalytics','iot-data','iotwireless'],'kinesisanalytics':['kinesis','dynamodb'],_I:[_A],_A:['rds-data'],_G:['mediastore-data'],'redshift':['redshift-data'],'timestream':['timestream-write','timestream-query'],_H:[_B]})
get_enabled_apis.cache_clear()
def api_key_configured():A='LOCALSTACK_API_KEY';return True if os.environ.get(A)and os.environ.get(A).strip()else False
def modify_edge_port_config():
	if os.environ.get('EDGE_PORT')and not localstack_config.EDGE_PORT_HTTP:LOG.warning(('!! Configuring EDGE_PORT={p} without setting EDGE_PORT_HTTP may lead '+'to issues; better leave the defaults, or set EDGE_PORT=443 and EDGE_PORT_HTTP={p}').format(p=localstack_config.EDGE_PORT))
	else:A=localstack_config.EDGE_PORT;localstack_config.EDGE_PORT=443;localstack_config.EDGE_PORT_HTTP=A
@hooks.on_infra_start(should_load=api_key_configured)
def add_custom_edge_routes():from localstack.services.edge import ROUTER as A;from localstack_ext.services.xray.routes import store_xray_records as B;A.add('/xray_records',B,methods=['POST'])
@hooks.prepare_host(priority=100,should_load=api_key_configured)
def activate_pro_key_on_host():
	with licensing.prepare_environment():LOG.debug('pro activation done')
@hooks.prepare_host(should_load=api_key_configured)
def create_dns_forward():
	try:from localstack_ext.services import dns_server as A;A.setup_network_configuration()
	except Exception as B:LOG.warning(_J,B)
@hooks.on_infra_start(should_load=api_key_configured)
def start_dns_server():
	try:from localstack_ext.services import dns_server as A;A.start_dns_server(asynchronous=True)
	except Exception as B:LOG.warning(_J,B)
@hooks.prepare_host(should_load=api_key_configured)
def start_ec2_daemon():
	try:
		if config_ext.EC2_AUTOSTART_DAEMON:LOG.debug('Starting EC2 daemon...');local_daemon.start_in_background()
	except Exception as A:LOG.warning('Unable to start local daemon process: %s'%A)
@hooks.configure_localstack_container(priority=10,should_load=api_key_configured)
def configure_pro_container(container):
	A=container
	try:
		from localstack_ext.services import dns_server as B;C=[]
		if config_ext.use_custom_dns():
			if not net.is_port_open(B.DNS_PORT,protocols='tcp'):C+=['-p','{a}:{p}:{p}'.format(a=config_ext.DNS_ADDRESS,p=B.DNS_PORT)]
			if not net.is_port_open(B.DNS_PORT,protocols='udp'):C+=['-p','{a}:{p}:{p}/udp'.format(a=config_ext.DNS_ADDRESS,p=B.DNS_PORT)]
		A.additional_flags.extend(C)
	except Exception as E:LOG.warning('failed to configure DNS: %s',E)
	modify_edge_port_config();D=os.path.expanduser('~/.kube/config')
	if os.path.exists(D):A.volumes.add(VolumeBind(D,'/root/.kube/config'))
	if localstack_config.is_env_true('AZURE'):A.ports.add(5671);A.ports.add(config_ext.PORT_AZURE)
@hooks.on_infra_start(should_load=is_enterprise,priority=100)
def configure_enterprise():from localstack import config as A;LOG.debug('Disabling SSL cert download (enterprise image).');A.SKIP_SSL_CERT_DOWNLOAD=True
@hooks.on_infra_start(should_load=api_key_configured,priority=10)
def setup_pro_infra():
	_setup_logging();modify_edge_port_config()
	with licensing.prepare_environment():
		try:from localstack_ext.services import dns_server as B;B.setup_network_configuration()
		except Exception as A:LOG.warning('error setting up dns server: %s',A)
		try:from localstack_ext.aws.protocol import service_router as C;from localstack_ext.services import edge;from localstack_ext.utils.aws import aws_utils as D;C.patch_service_router();edge.patch_start_edge();patch_start_infra();D.patch_aws_utils();set_default_providers_to_pro()
		except Exception as A:
			if LOG.isEnabledFor(level=logging.DEBUG):LOG.exception('error enabling pro code')
			else:LOG.error('error enabling pro code: %s',A)
def set_default_providers_to_pro():
	D='pro';from localstack.services.plugins import SERVICE_PLUGINS as B
	if not config_ext.PROVIDER_FORCE_EXPLICIT_LOADING:
		for (A,E) in localstack_config.SERVICE_PROVIDER_CONFIG._provider_config.items():
			F=B.api_provider_specs[A];C=[A for A in F if A==f"{E}_pro"]
			if C:localstack_config.SERVICE_PROVIDER_CONFIG.set_provider(A,C[0])
	G=B.apis_with_provider(D);localstack_config.SERVICE_PROVIDER_CONFIG.bulk_set_provider_if_not_exists(G,D);H=['azure']if localstack_config.is_env_true('AZURE')else[]
	for A in H:
		try:LOG.debug('loading service plugin for %s',A);B.get_service_container(A).start()
		except Exception as I:LOG.error('error while loading service %s: %s',A,I)
def patch_start_infra():
	from localstack.services import infra as A
	def B(asynchronous,apis,is_in_docker,*A,**B):
		D=config_ext.ENFORCE_IAM
		try:config_ext.ENFORCE_IAM=False;return C(asynchronous,apis,is_in_docker,*(A),**B)
		finally:config_ext.ENFORCE_IAM=D
	C=A.do_start_infra;A.do_start_infra=B
@on_infra_ready(should_load=api_key_configured)
def initialize_health_info():from localstack_ext.utils.persistence import update_persistence_health_info as A;A()
@hooks.on_infra_start(priority=100)
def deprecation_warnings_pro():from localstack.deprecations import DEPRECATIONS as A,EnvVarDeprecation as B;A.append(B('LEGACY_IAM_ENFORCEMENT','1.0.0','Please migrate to the new IAM enforcements by removing this environment variable.'))
def _setup_logging():A=logging.DEBUG if localstack_config.DEBUG else logging.INFO;logging.getLogger('localstack_ext').setLevel(A);logging.getLogger('asyncio').setLevel(logging.INFO);logging.getLogger('botocore').setLevel(logging.INFO);logging.getLogger('dulwich').setLevel(logging.ERROR);logging.getLogger('hpack').setLevel(logging.INFO);logging.getLogger('jnius.reflect').setLevel(logging.INFO);logging.getLogger('kazoo').setLevel(logging.ERROR);logging.getLogger('kubernetes').setLevel(logging.INFO);logging.getLogger('parquet').setLevel(logging.INFO);logging.getLogger('pyftpdlib').setLevel(logging.INFO);logging.getLogger('pyhive').setLevel(logging.INFO);logging.getLogger('pyqldb').setLevel(logging.INFO);logging.getLogger('redshift_connector').setLevel(logging.INFO);logging.getLogger('websockets').setLevel(logging.INFO);logging.getLogger('Parser').setLevel(logging.CRITICAL);logging.getLogger('postgresql_proxy').setLevel(logging.WARNING);logging.getLogger('intercept').setLevel(logging.WARNING);logging.getLogger('root').setLevel(logging.WARNING);logging.getLogger('').setLevel(logging.WARNING)