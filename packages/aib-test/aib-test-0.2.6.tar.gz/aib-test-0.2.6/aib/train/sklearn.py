import uuid
import joblib
import shutil
from pathlib import Path
import requests

import numpy as np
from sklearn.model_selection import learning_curve

import aib._private.client as aib_client
from aib._private.utils.VO import ExportModelVO
from .types import MODEL_TYPE

class sklearnTrainer:
    def __init__(self, model_name, estimator, X, y, export: bool = True):
        self.__estimator = estimator
        self.model_name = model_name
        self.__X = X
        self.__y = y
        self.__export = export
        self.__history = {}

    def fit(self, scoring: str | None = None, cv: int = None):
        train_sizes, train_scores, test_scores, fit_times, _ = \
            learning_curve(self.__estimator, self.__X, self.__y, return_times=True, scoring=scoring, cv=cv)
        self.__estimator.fit(self.__X, self.__y)
        # export only can execute in executor
        if self.__export:
            self.__history["learning_curve"] = [train_sizes, np.mean(train_scores, axis=1)]
            save_path = "./tmp/" + str(uuid.uuid4())
            file_path = save_path + "/" + self.model_name + "/"
            zip_path = save_path + "/" + self.model_name
            Path(file_path).mkdir(parents=True, exist_ok=True)
            joblib.dump(self.__estimator, file_path + self.model_name + ".pkl")
            shutil.make_archive(zip_path, "zip", file_path)

            client_info = aib_client.aib_info
            try:
                url = client_info.AIB_IFLOW_SERVER_URL + "/model/export"
                files = [('files', open(zip_path+".zip", "rb"))]
                export_model = ExportModel(PROJECT_ID=client_info.PROJECT_ID,
                                           MODEL_NAME=self.model_name,
                                           MODEL_TYPE=MODEL_TYPE.SKLEARN)
                payload = export_model.dict()
                res = requests.post(url=url, params=payload, files=files)
            except Exception as exc:
                raise exc
            else:
                if res.status_code == 200:
                    if res.json().get("CODE") == "SUCCESS":
                        print("success")
                    else:
                        print("export fail on aib server error msg: " + res.json().get("ERROR_MSG"))
                else:
                    print("export fail. status code: " + str(res.status_code))
            finally:
                shutil.rmtree(save_path)
        return self.__history

    @property
    def estimator(self):
        return self.__estimator

    @property
    def history(self):
        return self.__history

