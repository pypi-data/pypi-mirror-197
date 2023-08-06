import sys
import os
import requests

import ray
from pydantic import BaseModel, Extra

from .exceptions import *


this = sys.modules[__name__]
os.environ["AIB_IFLOW_SERVER_URL"] = "http://localhost:8090/iflow"
os.environ["SPARK_MASTER"] = "spark://192.168.149.131:7077"
os.environ["PROJECT_ID"] = "TEST"
os.environ["USER"] = "TEST_USER"
os.environ["DATASET"] = "TEST"
os.environ["CLIENT_TYPE"] = "NOTEBOOK"


class AibInformation(BaseModel):
    AIB_IFLOW_SERVER_URL: str
    SPARK_MASTER: str
    USER: str
    PROJECT_ID: str
    DATASET: str
    CLIENT_TYPE: str
    IS_INIT: bool = False

    class Config:
        extra = Extra.forbid


def init():
    try:
        if this.aib_info.IS_INIT:
            print("aibeem client is already inited")
            return
    except AttributeError:
        pass
    except Exception as exc:
        print(exc.__str__())
    try:
        this.aib_info = AibInformation(AIB_IFLOW_SERVER_URL=os.getenv("AIB_IFLOW_SERVER_URL"),
                                       SPARK_MASTER=os.getenv("SPARK_MASTER"),
                                       USER=os.getenv("USER"),
                                       PROJECT_ID=os.getenv("PROJECT_ID"),
                                       DATASET=os.getenv("DATASET"),
                                       CLIENT_TYPE=os.getenv("CLIENT_TYPE"))
    except Exception as exc:
        raise InitError(exc.__str__())
    try:
        res = requests.get(this.aib_info.AIB_IFLOW_SERVER_URL + "/health_check", timeout=10)
    except Exception as exc:
        raise InitError(exc.__str__())
    else:
        if res.status_code == 200:
            code = res.json().get("CODE")
            if code == "SUCCESS":
                if this.aib_info.CLIENT_TYPE == "NOTEBOOK":
                    ray.init(include_dashboard=False)
                this.aib_info.IS_INIT = True
            else:
                raise InitError("aibeem response code is FAIL")
        else:
            raise InitError("response code of aib server is not 200: "+str(res.status_code))






