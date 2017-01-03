import os
import errno
from systemd import journal


class JournalExporter:
    def __init__(self, unit):
        self.journal = journal.Reader()
        self.journal.this_boot()
        self.journal.add_match(_SYSTEMD_UNIT="%s.service" % unit)
        self.cursor_file_path = os.path.join(
            os.getcwd(),
            'cursor-%s.txt' % unit
        )

    def get_entries(self):
        cursor_first = None
        try:
            with open(self.cursor_file_path, 'r') as store:
                cursor_first = store.read().strip()

                if cursor_first:
                    self.journal.seek_cursor(cursor_first)
                else:
                    raise
        except OSError as e:
            if e.errno == errno.ENOENT:
                self.journal.seek_head()

        self.cursor_last = self.journal[-1]['__CURSOR']
        # entries = [self.create_aws_payload(entry) for entry in self.journal]
        return self.journal[1:] if cursor_first is not None else self.journal

    def set_cursor(self, entries):
        with open(self.cursor_file_path, 'w') as store:
            store.write(self.cursor_last)
