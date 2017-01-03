import abc


class PluginBase(abc.ABC):

    @abc.abstractmethod
    def create_payload(self, data):
        """Format the list of data objects."""

    @abc.abstractmethod
    def save(self, data):
        """Save the list of data objects to the chosen endpoint."""
