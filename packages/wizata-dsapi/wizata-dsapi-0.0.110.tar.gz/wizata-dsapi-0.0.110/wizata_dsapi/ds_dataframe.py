import uuid
import pandas
from .api_dto import ApiDto


class DSDataFrame(ApiDto):

    def __init__(self, df_id=None):
        if df_id is None:
            self.df_id = uuid.uuid4()
        else:
            self.df_id = df_id
        self.generatedById = None
        self.dataframe = None

    def api_id(self) -> str:
        return str(self.df_id).upper()

    def endpoint(self) -> str:
        return "Dataframes"

    def from_json(self, json, api=False):
        if "id" in json.keys():
            self.df_id = uuid.UUID(json["id"])

        if "generatedById" in json.keys():
            self.generatedById = json["generatedById"]

    def to_json(self, api=False):
        obj = {
            "id": str(self.df_id)
        }
        if self.generatedById is not None:
            obj["generatedById"] = str(self.generatedById)
        return obj

