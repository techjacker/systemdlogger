from pytest import fixture
from unittest.mock import patch, Mock
from systemdlogger.plugin import PluginBase
import systemdlogger.elasticsearch as es


@fixture
def init_params():
    return {
        'doctype': 'webserver',
        'hosts': ['localhost']
    }


def test_init(init_params):

    with patch.object(es.connections, 'create_connection'):

        elasticsearch_logger = es.ElasticsearchLogger(**init_params)

        assert issubclass(es.ElasticsearchLogger, PluginBase)
        assert isinstance(elasticsearch_logger, PluginBase)
        assert elasticsearch_logger.doctype == init_params['doctype']

        m = Mock()
        m(hosts=init_params['hosts'])
        assert es.connections.create_connection.mock_calls == m.mock_calls


# class TestEs:

#     def setup_method(self, method):
#         self.EsLog = Mock()
#         es.EsLog = self.EsLog

#     def teardown_method(self, method):
#         self.EsLog.restore()

#     def test_init(self, init_params):
#         elasticsearch_logger = es.ElasticsearchLogger(**init_params)
#         assert issubclass(es.ElasticsearchLogger, PluginBase)
#         assert isinstance(elasticsearch_logger, PluginBase)
#         assert elasticsearch_logger.doc_type == init_params['doc_type']
#         assert es.EsLog.init.call_count == 1
