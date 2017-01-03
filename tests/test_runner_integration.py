from pytest import fixture
from unittest.mock import patch
import tests.fixtures.journal as FakeJournalExporter
from systemdlogger.elasticsearch import ElasticsearchLogger


@fixture
def config_path():
    return 'tests/fixtures/config_es.json'


class TestRunner:

    def setup_method(self, method):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        modules = {
            'systemdlogger.journal': FakeJournalExporter
        }

        self.module_patcher = patch.dict('sys.modules', modules)
        self.module_patcher.start()
        from systemdlogger.runner import Runner
        self.Runner = Runner

    def teardown_method(self, method):
        """ teardown any state that was previously setup with a setup_method
        call.
        """
        self.module_patcher.stop()

    def test_init(self, config_path):
        runner = self.Runner(config_path)
        assert len(runner.loggers) == 1
        assert isinstance(runner.loggers[0], ElasticsearchLogger)

    def test_run(self, config_path):
        runner = self.Runner(config_path)
        runner.run()
