import uuid
import pandas


class DSDataFrame:

    def __init__(self, df_id=None):
        if df_id is None:
            self.df_id = uuid.uuid4()
        else:
            self.df_id = df_id
        self.generatedById = None
        self.dataframe = None

    def from_json(self, json):
        if "id" in json.keys():
            self.df_id = uuid.UUID(json["id"])

        if "generatedById" in json.keys():
            self.generatedById = json["generatedById"]

    def to_json(self):
        obj = {
            "id": str(self.df_id)
        }
        if self.generatedById is not None:
            obj["generatedById"] = str(self.generatedById)
        return obj

