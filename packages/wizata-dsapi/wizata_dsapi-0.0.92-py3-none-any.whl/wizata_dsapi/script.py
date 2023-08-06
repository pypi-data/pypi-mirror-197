import uuid
import dill


class Script:

    def __init__(self, script_id=None):

        # Id
        if script_id is None:
            script_id = uuid.uuid4()
        self.script_id = script_id

        # Properties
        self.name = None
        self.description = None
        self.canGeneratePlot = False
        self.canGenerateModel = False
        self.canGenerateData = False
        self.status = "draft"
        self.needExactColumnNumbers = False
        self.needExactColumnNames = False
        self.inputColumns = []
        self.outputColumns = []

        # Function properties (code)
        self.function = None

    def to_json(self):
        return {
            "id": str(self.script_id),
            "name": str(self.name),
            "description": str(self.description),
            "canGeneratePlot": str(self.canGeneratePlot),
            "canGenerateModel": str(self.canGenerateModel),
            "canGenerateData": str(self.canGenerateData),
            "status": str(self.status),
            "needExactColumnNumbers": str(self.needExactColumnNumbers),
            "needExactColumnNames": str(self.needExactColumnNames),
            "inputColumns": list(self.inputColumns),
            "outputColumns": list(self.outputColumns)
        }

    def from_json(self, json):
        if "id" in json.keys():
            self.script_id = uuid.UUID(json["id"])
        if "name" in json.keys():
            self.name = json["name"]
        if "description" in json.keys():
            self.description = json["description"]
        if "canGeneratePlot" in json.keys():
            self.canGeneratePlot = bool(json["canGeneratePlot"] == 'True')
        if "canGenerateModel" in json.keys():
            self.canGenerateModel = bool(json["canGenerateModel"] == 'True')
        if "canGenerateData" in json.keys():
            self.canGenerateData = bool(json["canGenerateData"] == 'True')
        if "status" in json.keys():
            self.status = json["status"]
        if "needExactColumnNumbers" in json.keys():
            self.needExactColumnNumbers = bool(json["needExactColumnNumbers"] == 'True')
        if "needExactColumnNames" in json.keys():
            self.needExactColumnNames = bool(json["needExactColumnNames"] == 'True')
        if "inputColumns" in json.keys():
            self.inputColumns = json["inputColumns"]
        if "outputColumns" in json.keys():
            self.outputColumns = json["outputColumns"]

    def copy(self, myfunction):
        self.function = Function()
        self.function.code = myfunction.__code__
        self.function.globals = myfunction.__globals__


class Function:

    def __init__(self):
        self.code = None
        self.globals = None
