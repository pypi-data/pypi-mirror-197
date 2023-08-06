class ApiDto:

    def api_id(self) -> str:
        """
        return current object id on Web API format.
        """
        pass

    def endpoint(self) -> str:
        """
        return endpoint name in Web API
        """
        pass

    def to_json(self, api=False):
        """
        transform current object into a dumpable dict compatible with JSON format.
        :param api: set to True if desired format is for Web API or by default return .py SDK format.
        :return: dumpable dict.
        """
        pass

    def from_json(self, obj, api=True):
        """
        load the object from a dict originating of a JSON format.
        :param obj: object to load information from.
        :param api: set to True if desired format is from Web API or by default from .py SDK format.
        """
        pass
