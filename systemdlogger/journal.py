import os
import errno
from systemd import journal


class JournalExporter:
    def __init__(self, unit, cursor_filepath):
        self.journal = journal.Reader()
        self.journal.this_boot()
        self.journal.add_match(_SYSTEMD_UNIT="%s.service" % unit)
        self.cursor_filepath = self.set_cursor_filepath(
            cursor_filepath, unit)

    @staticmethod
    def set_cursor_filepath(filepath, unit):
        return filepath if filepath else os.path.join(
            os.getcwd(),
            'journal-cursor-%s.txt' % unit
        )

    def get_entry(self, entry):
        self.cursor_last = entry['__CURSOR']
        return entry

    def get_entries(self):
        cursor_first = None
        try:
            with open(self.cursor_filepath, 'r') as store:
                cursor_first = store.read().strip()

                if cursor_first:
                    self.journal.seek_cursor(cursor_first)
                else:
                    raise
        except OSError as e:
            if e.errno == errno.ENOENT:
                self.journal.seek_head()

        entries = [self.get_entry(entry) for entry in self.journal]
        return entries[1:] if cursor_first is not None else entries

    def set_cursor(self, entries):
        with open(self.cursor_filepath, 'w') as store:
            store.write(self.cursor_last)
