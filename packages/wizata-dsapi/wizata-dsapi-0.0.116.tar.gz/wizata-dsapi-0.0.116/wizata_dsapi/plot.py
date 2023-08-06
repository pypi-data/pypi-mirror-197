import uuid
from .api_dto import ApiDto


class Plot(ApiDto):
    """
    A plot is a definition of a Plotly figure that can be stored and shared on Wizata.
    """

    def __init__(self, plot_id=None):
        if plot_id is None:
            self.plot_id = uuid.uuid4()
        else:
            self.plot_id = plot_id
        self.name = None
        self.generatedById = None
        self.figure = None

    def api_id(self) -> str:
        return str(self.plot_id).upper()

    def endpoint(self) -> str:
        return "Plots"

    def from_json(self, obj, api=False):
        if "id" in obj.keys():
            self.plot_id = uuid.UUID(obj["id"])
        if "name" in obj.keys():
            self.name = obj["name"]
        if "figure" in obj.keys():
            self.figure = obj["figure"]
        if "generatedById" in obj.keys():
            self.generatedById = obj["generatedById"]

    def to_json(self, api=False):
        obj = {
            "id": str(self.plot_id)
        }
        if self.name is not None:
            obj["name"] = self.name
        if self.figure is not None and not api:
            obj["figure"] = self.figure
        if self.generatedById is not None:
            obj["generatedById"] = self.generatedById
        return obj
