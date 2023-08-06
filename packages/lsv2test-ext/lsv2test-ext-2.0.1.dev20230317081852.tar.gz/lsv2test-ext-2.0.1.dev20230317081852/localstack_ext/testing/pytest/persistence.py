_F='function'
_E='persistence_validations'
_D='snapshot'
_C=None
_B=False
_A=True
import logging,os,tempfile,time
from contextlib import contextmanager
from enum import Enum
from typing import Callable
import pytest
from _pytest._code import ExceptionInfo
from _pytest._code.code import Code,filter_traceback
from _pytest.compat import get_real_func
from _pytest.config import Config,PytestPluginManager
from _pytest.config.argparsing import Parser
from _pytest.fixtures import FixtureRequest
from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.runner import CallInfo
from localstack import constants
from localstack.testing.snapshots import SnapshotSession
from localstack.testing.snapshots.transformer_utility import SNAPSHOT_BASIC_TRANSFORMER
from localstack.utils import files,sync
from localstack.utils.container_utils.container_client import ContainerException
from localstack.utils.docker_utils import DOCKER_CLIENT
from localstack.utils.patch import patch
from localstack.utils.run import ShellCommandThread
from localstack.utils.serving import Server
from localstack.utils.strings import short_uid
from localstack.utils.sync import poll_condition
from localstack.utils.threads import FuncThread
from localstack_ext.config import ROOT_FOLDER
LOG=logging.getLogger(__name__)
COVERAGE_FILE_NAME='.coverage'
class LocalstackPersistenceMode(Enum):snapshot=_D;cloudpods='cloudpods'
class PersistenceSnapshotSession(SnapshotSession):
	def __init__(C,*A,**B):super().__init__(*(A),**B)
	def _persist_state(A):return
	def _load_state(A):return{}
	@contextmanager
	def record_state(self):A=self;B=A.update;C=A.verify;A.update=_A;A.verify=_B;yield;A.recorded_state=A.observed_state;A.recorded_state=A._transform(A.recorded_state);A.observed_state={};A.called_keys.clear();A.update=B;A.verify=C
class PersistenceValidator:
	test:Item;function:Callable;snapshot:PersistenceSnapshotSession
	def __init__(A,test,function,snapshot):A.test=test;A.function=function;A.snapshot=snapshot
class PersistenceValidations:
	test:Item;validators:list[PersistenceValidator]
	def __init__(A,test,snapshot):A.test=test;A.validators=[];A.snapshot=snapshot
	def register(A,fn):A.validators.append(PersistenceValidator(A.test,fn,A.snapshot))
	def run_setup(A):
		with A.snapshot.record_state():
			for B in A.validators:B.function()
	def match(A,key,value):return A.snapshot.match(key,value)
class PersistenceValidationsItem(Item):
	test:Item;validations:PersistenceValidations
	def __init__(A,parent,name,test,validations):super().__init__(parent=parent,name=name);A.own_markers=list(test.own_markers);A.test=test;A.validations=validations;A.funcargs={};A.failed_validator=_C
	def reportinfo(A):return A.fspath,A.validations.test.reportinfo()[1],A.name
	def runtest(A):
		D=_A;B=[];E=A.validations.test
		for F in E.iter_markers(name='skip_snapshot_verify'):G=F.kwargs.get('paths',[]);B.extend(G)
		for C in A.validations.validators:
			try:C.function()
			except Exception:A.failed_validator=C;raise
		A.validations.snapshot._assert_all(D,B)
	def _prunetraceback(B,excinfo):
		G='auto';C=excinfo
		if B.config.getoption('fulltrace',_B):return
		if not B.failed_validator:return
		E=Code.from_function(get_real_func(B.failed_validator.function));F,H=E.path,E.firstlineno;D=C.traceback;A=D.cut(path=F,firstlineno=H)
		if A==D:
			A=A.cut(path=F)
			if A==D:
				A=A.filter(filter_traceback)
				if not A:A=D
		C.traceback=A.filter()
		if B.config.getoption('tbstyle',G)==G:
			if len(C.traceback)>2:
				for I in C.traceback[1:-1]:I.set_repr_style('short')
class RestartLocalstack(Item):
	funcargs={}
	def runtest(A):
		match A.config.option.persistence_mode:
			case LocalstackPersistenceMode.snapshot:B=A._persistence_restore()
			case LocalstackPersistenceMode.cloudpods:B=A._cloudpods_restore()
			case _:B=A._persistence_restore()
		with B:
			try:persistence_session.restart_localstack()
			except Exception:A.session.shouldfail=_A;raise
	@contextmanager
	def _persistence_restore(self):yield
	@contextmanager
	def _cloudpods_restore(self):from localstack_ext.bootstrap import pods_client as A;C=os.path.abspath(persistence_session.localstack_session.volume_dir);B=f"file:{C}/test-pod-{short_uid()}.zip";A.export_pod(target=B);yield;A.import_pod(source=B,merge_strategy='merge')
class LocalstackSession:
	def __init__(A,persistence_mode,port=4566):A.port=port;A.volume_dir=tempfile.mkdtemp(prefix='localstack-pytest-');A.persistence_mode=persistence_mode;A.server=_C
	def start(A,timeout):
		B=timeout
		if A.server:return
		A.server=A._create_localstack_server();A.server.start()
		if not A.server.wait_is_up(timeout=B):raise TimeoutError(f"gave up waiting for localstack startup after {B} seconds")
	def stop(A,timeout):
		B=timeout
		if not A.server:return
		A.server.shutdown()
		def C():
			try:return not A.server.health()
			except Exception:return _B
		if not sync.poll_condition(C,timeout=B):raise TimeoutError(f"gave up waiting for localstack stop after {B} seconds")
		A._extract_current_coverage_file()
	def _extract_current_coverage_file(B):
		A=os.path.join(B.volume_dir,'localstack',COVERAGE_FILE_NAME)
		if not os.path.exists(A):return
		C=os.path.join(ROOT_FOLDER,f".coverage.persistence.{int(time.time())}");files.cp_r(A,C)
	def restart(A,timeout):B=timeout;A.stop(B);A.server=_C;A.start(B)
	def close(A):
		try:files.rm_rf(A.volume_dir)
		except Exception as B:LOG.warning('could not delete temporary localstack volume dir %s: %s',A.volume_dir,B)
	def _create_localstack_server(A):B=A.persistence_mode==LocalstackPersistenceMode.snapshot;C={'PERSISTENCE':'1'if B else'0'};return LocalstackDevContainerServer(volume_dir=A.volume_dir,port=A.port,env=C)
class PersistenceSession:
	validations:dict[str,PersistenceValidations];validations_items:dict[str,PersistenceValidationsItem]
	def __init__(A):A.validations={};A.validations_items={};A.config=_C;A.session=_C;A.localstack_session=_C;A.default_localstack_timeout=60*2
	def configure(A,config):B=config;A.config=B;C=B.option.persistence_mode or LocalstackPersistenceMode.snapshot;A.localstack_session=LocalstackSession(C)
	def stop_localstack(A):A.localstack_session.stop(timeout=A.default_localstack_timeout)
	def start_localstack(A):A.localstack_session.start(timeout=A.default_localstack_timeout)
	def restart_localstack(A):A.localstack_session.restart(timeout=A.default_localstack_timeout)
	def register_test(B,test):A=test;E=B._new_snapshot_session(A);C=PersistenceValidations(A,E);D=PersistenceValidationsItem.from_parent(parent=A.parent,name=f"{A.name}[persistence_validations]",test=A,validations=C);B.validations[A.nodeid]=C;B.validations_items[A.nodeid]=D;return D
	def _new_snapshot_session(C,item):A=item;B=PersistenceSnapshotSession(file_path=os.path.join(os.path.relpath(A.fspath.dirname,ROOT_FOLDER),f"{A.fspath.purebasename}.snapshot.json"),scope_key=A.nodeid,update=_B,verify=_A);B.add_transformer(SNAPSHOT_BASIC_TRANSFORMER,priority=2);return B
	def is_persistence_test(A,item):
		if _E not in item._fixtureinfo.argnames:return _B
		return _A
	def close(A):
		if(B:=A.localstack_session):B.close()
class LocalstackDevContainerServer(Server):
	def __init__(A,volume_dir,port=4566,env=_C):super().__init__(port);A.container_name=f"ls-dev-{short_uid()}";A.volume_dir=volume_dir;A.env=env or{}
	def _get_env_vars(A):B={'EDGE_PORT':A.port,'INTERACTIVE_FLAGS':'-i','CONTAINER_NAME':A.container_name,'COVERAGE_FILE':os.path.join('/var/lib/localstack',COVERAGE_FILE_NAME),'RDS_MYSQL_DOCKER':'1','TMPDIR':A.volume_dir};B.update(A.env);return B
	def _get_coverage_file_path_on_host(A):return os.path.join(A.volume_dir,COVERAGE_FILE_NAME)
	def do_start_thread(A):
		C='. .venv/bin/activate; bin/coverage-run.py run --source localstack_ext -m localstack.cli.main start --host';B=ShellCommandThread(cmd=['./bin/docker-run.sh','bash','-c',C],env_vars=A._get_env_vars(),cwd=ROOT_FOLDER,log_listener=A._log_listener,name='docker-run-sh')
		@patch(B.stop)
		def D(_self,fn,*B):A._terminate_coverage();return fn(*(B))
		B.start();return B
	def _log_listener(A,line,**B):print(f"docker-run.sh: {line.rstrip()}")
	def _terminate_coverage(A):DOCKER_CLIENT.exec_in_container(A.container_name,['bash','-c','pkill -f coverage-run.py']);poll_condition(lambda:os.path.exists(A._get_coverage_file_path_on_host()),timeout=10)
	def is_container_running(A):return DOCKER_CLIENT.is_container_running(A.container_name)
	def do_shutdown(A):
		try:DOCKER_CLIENT.remove_container(A.container_name)
		except ContainerException:pass
	def is_up(A):
		if not A.is_container_running():return _B
		B=DOCKER_CLIENT.get_container_logs(A.container_name)
		if constants.READY_MARKER_OUTPUT not in B.splitlines():return _B
		return super().is_up()
persistence_session=PersistenceSession()
class PersistenceTestPlugin:
	@pytest.hookimpl()
	def pytest_addoption(self,parser,pluginmanager):parser.addoption('--persistence-mode',type=LocalstackPersistenceMode,choices=list(LocalstackPersistenceMode))
	@pytest.hookimpl(trylast=_A)
	def pytest_configure(self,config):persistence_session.configure(config)
	@pytest.hookimpl(trylast=_A)
	def pytest_sessionstart(self,session):persistence_session.start_localstack()
	@pytest.hookimpl()
	def pytest_sessionfinish(self,session):persistence_session.stop_localstack();persistence_session.close()
	@pytest.hookimpl()
	def pytest_collection_modifyitems(self,session,config,items):
		B=items
		for A in B:
			if not persistence_session.is_persistence_test(A):continue
			persistence_session.register_test(A);A.name=f"{A.name}[setup]"
		B.append(RestartLocalstack.from_parent(parent=session,name='restart_localstack'))
		for A in persistence_session.validations_items.values():B.append(A)
	@pytest.hookimpl(hookwrapper=_A)
	def pytest_runtest_call(self,item):
		B=yield
		if item.nodeid not in persistence_session.validations:return
		A=persistence_session.validations[item.nodeid];A.run_setup()
	@pytest.fixture(name=_E,scope=_F)
	def fixture_persistence_validations(self,request):
		A=request
		if(B:=persistence_session.validations.get(A.node.nodeid)):return B
		raise ValueError(f"Node {A.node.nodeid} not registered in persistence session")
	@pytest.fixture(name=_D,scope=_F)
	def fixture_persistence_snapshot(self,request):
		A=request
		if(B:=persistence_session.validations.get(A.node.nodeid)):return B.snapshot
		raise ValueError(f"Node {A.node.nodeid} not registered in persistence session, cannot use snapshot")