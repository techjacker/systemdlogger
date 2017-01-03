from systemdlogger.plugin import PluginBase
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Date, String
from datetime import datetime


class EsLog(DocType):

    timestamp = Date()
    message = String(index='not_analyzed')
    index = 'logs-%s' % datetime.now().strftime('%Y-%m-%d')

    @staticmethod
    def get_index_name_from_date(d):
        # eg logs-2016-08-12
        return 'logs-%s' % d.strftime('%Y-%m-%d')


class ElasticsearchLogger(PluginBase):
    def __init__(
        self,
        doctype,
        hosts
    ):
        try:
            connections.create_connection(hosts=hosts)
        except:
            pass

        self.doctype = doctype

    def create_payload(self, entries):
        return [
            EsLog(
                timestamp=entry['__REALTIME_TIMESTAMP'],
                message=entry['MESSAGE']
            ) for entry in entries]

    def save(self, data):
        results = []
        for es_log in self.create_payload(data):
            es_log.meta.doc_type = self.doctype
            es_log.meta.index = es_log.get_index_name_from_date(
                es_log.timestamp
            )
            results.append(es_log.save())

        # Display cluster health
        # print(connections.get_connection().cluster.health())
        return results
