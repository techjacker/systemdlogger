import os
import json
import datetime


class JournalExporter:
    def __init__(self, unit):
        self.cursor_file_path = os.path.join(
            os.getcwd(),
            'cursor-%s.txt' % unit
        )

    def get_entries(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, 'journal_entry.json')) as f:
            entries = json.load(f)
            for entry in entries:
                # entry['__REALTIME_TIMESTAMP'] = datetime.datetime.strptime(entry['__REALTIME_TIMESTAMP'])
                entry['__REALTIME_TIMESTAMP'] = datetime.datetime(
                    *map(
                        int,
                        entry['__REALTIME_TIMESTAMP'].split(', ')
                    )
                )
            self.cursor_last = entries[-1]['__CURSOR']
            return entries

    def set_cursor(self, entries):
        with open(self.cursor_file_path, 'w') as store:
            store.write(self.cursor_last)
