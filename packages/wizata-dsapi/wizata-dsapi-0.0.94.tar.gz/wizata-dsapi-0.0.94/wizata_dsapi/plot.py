import uuid


class Plot:

    def __init__(self, plot_id=None):
        if plot_id is None:
            self.plot_id = uuid.uuid4()
        else:
            self.plot_id = plot_id
        self.name = None
        self.experiment_id = None
        self.figure = None

    def from_json(self, json):

        if "id" in json.keys():
            self.plot_id = uuid.UUID(json["id"])

        if "name" in json.keys():
            self.name = json["name"]

        if "figure" in json.keys():
            self.figure = json["figure"]

        if "experiment_id" in json.keys():
            self.experiment_id = json["experiment_id"]

    def to_json(self):
        obj = {
            "id": str(self.plot_id)
        }
        if self.name is not None:
            obj["name"] = self.name
        if self.figure is not None:
            obj["figure"] = self.figure
        if self.experiment_id is not None:
            obj["experiment_id"] = self.experiment_id
        return obj
