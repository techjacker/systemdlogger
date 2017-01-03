from pytest import fixture
from unittest.mock import Mock, patch


@fixture
def config_path():
    return 'tests/fixtures/config.json'


class TestRunner:

    def setup_method(self, method):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """

        self.journal_mock = Mock()
        self.cw_mock = Mock()
        self.cw_mock.CloudwatchLogger.return_value = 'hello'
        self.es_mock = Mock()
        self.es_mock.ElasticsearchLogger.return_value = 'bye'

        modules = {
            'systemdlogger.journal': self.journal_mock,
            'systemdlogger.cloudwatch': self.cw_mock,
            'systemdlogger.elasticsearch': self.es_mock
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

        # assertions
        mj = Mock()
        mj.JournalExporter(**self.Runner.load_config(config_path)["systemd"])
        assert self.journal_mock.mock_calls == mj.mock_calls

        assert len(runner.loggers) == 2
        assert self.cw_mock.CloudwatchLogger.return_value in runner.loggers
        assert self.es_mock.ElasticsearchLogger.return_value in runner.loggers
