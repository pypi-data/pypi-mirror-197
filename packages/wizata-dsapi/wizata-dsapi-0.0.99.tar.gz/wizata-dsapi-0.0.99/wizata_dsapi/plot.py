import uuid


class Plot:

    def __init__(self, plot_id=None):
        if plot_id is None:
            self.plot_id = uuid.uuid4()
        else:
            self.plot_id = plot_id
        self.name = None
        self.generatedById = None
        self.figure = None

    def from_json(self, json):
        if "id" in json.keys():
            self.plot_id = uuid.UUID(json["id"])
        if "name" in json.keys():
            self.name = json["name"]
        if "figure" in json.keys():
            self.figure = json["figure"]
        if "generatedById" in json.keys():
            self.generatedById = json["generatedById"]

    def to_json(self):
        obj = {
            "id": str(self.plot_id)
        }
        if self.name is not None:
            obj["name"] = self.name
        if self.figure is not None:
            obj["figure"] = self.figure
        if self.generatedById is not None:
            obj["generatedById"] = self.generatedById
        return obj
