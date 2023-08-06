import uuid
from flask import jsonify


class MLModel:

    def __init__(self, model_id=None):

        # Model ID (GUID used to store the entity on backend and the wizatads on the blob storage
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

    def jsonify(self):
        return jsonify({
            "id": str(self.model_id),
            "status": str(self.status),
            "generatedById": str(self.generatedById),
            "input_columns": list(self.input_columns),
            "output_columns": list(self.output_columns),
            "has_anomalies": str(self.has_anomalies),
            "labels_count": str(self.label_counts),
            "has_target_feat": str(self.has_target_feat),
            "needExactColumnNames": str(self.needExactColumnNames),
            "needExactColumnNumbers": str(self.needExactColumnNumbers)
        })

    def load_json(self, json):
        if "id" in json.keys():
            self.model_id = json["id"]
        if "labels_count" in json.keys():
            self.label_counts = int(json["labels_count"])
        if "input_columns" in json.keys():
            self.input_columns = json["input_columns"]
        if "output_columns" in json.keys():
            self.output_columns = json["output_columns"]
        if "has_anomalies" in json.keys():
            self.has_anomalies = json["has_anomalies"]
        if ("has_target_feat" in json.keys()) and (json["has_target_feat"] == 'True'):
            self.has_target_feat = True
        if "needExactColumnNumbers" in json.keys():
            self.needExactColumnNumbers = bool(json["needExactColumnNumbers"] == 'True')
        if "needExactColumnNames" in json.keys():
            self.needExactColumnNames = bool(json["needExactColumnNames"] == 'True')
        if "status" in json.keys():
            self.status = json["status"]

    def get_sample_payload(self):
        pl_columns = {"timestamp": "[timestamp]"}
        for hardwareId in self.input_columns:
            pl_columns[hardwareId] = "[" + hardwareId + "]"
        pl_json = {
            "id": str(self.model_id),
            "dataset": pl_columns
        }
        return pl_json

