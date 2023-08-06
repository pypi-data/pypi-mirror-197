import pickle
import uuid

from .dataframe_toolkit import DataFrameToolkit
from .mlmodel import MLModel
from .plot import Plot
from .request import Request
from .script import Script


class Execution:

    def __init__(self, execution_id=None):

        # Id
        if execution_id is None:
            execution_id = uuid.uuid4()
        self.execution_id = execution_id

        # Experiment information (required only for queries processed from backend)
        self.experiment_id = None
        self.experiment_type = None

        # Accept "wizard" (frontend legacy), "simulate" (model), "script" (custom function)
        self.execution_type = "wizard"

        # Inputs Properties (load)
        self.script = None
        self.request = None
        self.dataframe = None
        self.ml_model = None
        self.function = None
        self.isAnomalyDetection = False

        # Outputs Properties (save)
        self.models = []
        self.anomalies = []
        self.plots = []
        self.result_dataframe = None
        self.result_ds_dataframe = None

    def append_plot(self, figure, name="Unkwown"):
        plot = Plot()
        plot.name = name
        plot.experiment_id = self.experiment_id
        plot.figure = figure
        self.plots.append(plot)
        return plot

    def append_model(self, trained_model, input_columns, output_columns=None, has_anomalies=False, scaler=None):
        ml_model = MLModel()

        ml_model.trained_model = trained_model
        ml_model.scaler = scaler

        ml_model.input_columns = input_columns
        ml_model.output_columns = output_columns

        ml_model.has_anomalies = has_anomalies

        self.models.append(ml_model)
        return ml_model

    def to_json(self, result=False, for_api=False):
        """
        Convert to a json version of Execution definition.
        By default, use DS API format.
        :param result: if set as True, use format for python client.
        :param for_api: if set as True, use format for backend API.
        """
        obj = {
            "id": str(self.execution_id)
        }
        if self.experiment_id is not None and for_api:
            obj["experiment_id"] = str(self.experiment_id)
        if self.request is not None and not result:
            obj["request"] = self.request.to_json()
        if self.dataframe is not None and not result and not for_api:
            obj["dataframe"] = DataFrameToolkit.convert_to_json(self.dataframe)
        if self.script is not None and not result:
            if for_api:
                obj["script_id"] = str(self.script.script_id)
            else:
                obj["script"] = self.script.to_json()
        if self.ml_model is not None and not result:
            if for_api:
                obj["model_id"] = str(self.ml_model.model_id)
            else:
                obj["ml_model"] = self.ml_model.jsonify()
        if self.function is not None and not result:
            obj["function"] = self.function
        if self.isAnomalyDetection and not result:
            obj["isAnomalyDetection"] = str(True)
        if self.plots is not None and not for_api:
            plots_ids = []
            for plot in self.plots:
                plots_ids.append({"id": str(plot.plot_id), "name": plot.name})
            obj["plots"] = plots_ids
        if self.models is not None and not for_api:
            models_json = []
            for ml_model in self.models:
                models_json.append(ml_model.get_sample_payload())
            obj["models"] = models_json
        if self.anomalies is not None and not for_api:
            obj["anomaliesList"] = self.anomalies
        if self.result_dataframe is not None and not for_api:
            obj["result"] = DataFrameToolkit.convert_to_json(self.result_dataframe)
        if self.result_ds_dataframe is not None and not for_api:
            obj["result_ds_dataframe_id"] = str(self.result_ds_dataframe.df_id)
        return obj

    def from_json(self, obj):
        if "id" in obj.keys():
            self.execution_id = uuid.UUID(obj["id"])
        if "request" in obj.keys():
            self.request = Request()
            self.request.from_json(obj["request"])
        if "dataframe" in obj.keys():
            self.dataframe = DataFrameToolkit.convert_from_json(obj["dataframe"])
        if "script" in obj.keys():
            self.script = Script()
            self.script.from_json(obj["script"])
        if "ml_model" in obj.keys():
            self.ml_model = MLModel()
            self.ml_model.load_json(obj["ml_model"])
        if "function" in obj.keys() and obj:
            self.function = obj["function"]
        if "isAnomalyDetection" in obj.keys() and obj["isAnomalyDetection"] == 'True':
            self.isAnomalyDetection = True

    def to_pickle(self):
        return pickle.dumps(self)