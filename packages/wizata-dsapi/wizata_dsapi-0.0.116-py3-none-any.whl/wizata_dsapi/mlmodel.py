import json
import uuid
from flask import jsonify
from .api_dto import ApiDto


class MLModel(ApiDto):

    def __init__(self, model_id=None):
        if model_id is None:
            model_id = uuid.uuid4()
        self.model_id = model_id

        self.generatedById = None
        self.status = 'draft'
        self.needExactColumnNumbers = True
        self.needExactColumnNames = True
        self.input_columns = []
        self.output_columns = []
        self.has_anomalies = False
        self.label_counts = 0
        self.has_target_feat = False

        self.trained_model = None
        self.scaler = None

    def api_id(self) -> str:
        return str(self.model_id).upper()

    def endpoint(self) -> str:
        return "MLModels"

    def to_json(self, api=False):
        obj = {
            "id": str(self.model_id),
            "status": str(self.status),
            "has_anomalies": str(self.has_anomalies),
            "has_target_feat": str(self.has_target_feat),
            "labels_count": str(self.label_counts),
            "needExactColumnNames": str(self.needExactColumnNames),
            "needExactColumnNumbers": str(self.needExactColumnNumbers)
        }
        if self.generatedById is None:
            obj["generatedById"] = str(self.generatedById)
        if self.input_columns is not None:
            if api:
                obj["inputColumns"] = json.dumps(list(self.input_columns))
            else:
                obj["input_columns"] = list(self.input_columns)
        if self.output_columns is not None:
            if api:
                obj["outputColumns"] = json.dumps(list(self.output_columns))
            else:
                obj["output_columns"] = list(self.output_columns)
        return obj

    def from_json(self, json, api=False):
        if "id" in json.keys():
            self.model_id = json["id"]
        if "labels_count" in json.keys():
            self.label_counts = int(json["labels_count"])
        if "input_columns" in json.keys():
            self.input_columns = json["input_columns"]
        if "output_columns" in json.keys():
            self.output_columns = json["output_columns"]
        if "has_anomalies" in json.keys():
            if api:
                self.has_anomalies = bool(json["has_anomalies"])
            else:
                self.has_anomalies = bool(json["has_anomalies"] == 'True')
        if "has_target_feat" in json.keys():
            if api:
                self.has_target_feat = bool(json["has_target_feat"])
            else:
                self.has_target_feat = bool(json["has_target_feat"] == 'True')
        if "needExactColumnNumbers" in json.keys():
            if api:
                self.needExactColumnNumbers = bool(json["needExactColumnNumbers"])
            else:
                self.needExactColumnNumbers = bool(json["needExactColumnNumbers"] == 'True')
        if "needExactColumnNames" in json.keys():
            if api:
                self.needExactColumnNames = bool(json["needExactColumnNames"])
            else:
                self.needExactColumnNames = bool(json["needExactColumnNames"] == 'True')
        if "status" in json.keys():
            self.status = str(json["status"]).lower()

    def get_sample_payload(self):
        pl_columns = {"timestamp": "[timestamp]"}
        for hardwareId in self.input_columns:
            pl_columns[hardwareId] = "[" + hardwareId + "]"
        pl_json = {
            "id": str(self.model_id),
            "dataset": pl_columns
        }
        return pl_json

