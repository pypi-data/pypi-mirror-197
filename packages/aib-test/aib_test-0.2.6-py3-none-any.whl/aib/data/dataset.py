from dataclasses import dataclass

import numpy
import pandas
import ray.data
import requests
from ray.data import Dataset as RayDataset
import aib._private.client as aib_client
from aib._private.utils.VO import MysqlInfoVO
from .read_api import read_mysql


# Artifact type
# Dataset[pandas]
# Dataset[Numpy]
# Dataset[Ray] (always save as pandas?)
#

class Dataset:
    def __init__(self, name: str = None):
        self.__data: RayDataset | numpy.ndarray | None = None
        self.__dataset_name: str = name

    def to_pandas(self):
        return self.__data.to_pandas()

    def from_pandas(self, df: pandas.DataFrame):
        #  check input type
        # do some
        self.__data = ray.data.from_pandas(df)
        return self

    def show(self):
        # branch with dataset type
        self.__data.show()

    @property
    def name(self):
        return self.__dataset_name


def load_dataset(name: str) -> Dataset:
    dataset_source_info = None
    client_info = aib_client.aib_info
    try:
        url = client_info.AIB_IFLOW_SERVER_URL + "/dataset/" + client_info.PROJECT_ID + "/" + name
        res = requests.get(url, timeout=10)
    except Exception as exc:
        raise exc
    else:
        if res.status_code == 200:
            if res.json().get("CODE") == "SUCCESS":
                dataset_source_info = res.json()
            else:
                print("export fail on aib server error msg: " + res.json().get("ERROR_MSG"))
        else:
            print("export fail. status code: " + str(res.status_code))

    if dataset_source_info is not None:
        if dataset_source_info["DB_TYPE"] == "MYSQL":
            mysql_info = MysqlInfoVO(USER=dataset_source_info["DB_USER"],
                                     PASSWORD=dataset_source_info["PASSWORD"],
                                     IP=dataset_source_info["IP"],
                                     PORT=dataset_source_info["PORT"],
                                     DB=dataset_source_info["DB"])
            ds = read_mysql(mysql_info, dataset_source_info["TABLE"])
            dataset = Dataset(name=name)
            dataset = dataset.from_pandas(ds)
            return dataset


def get_dataset_list() -> dict:
    # make http module
    # check client_type (executor or notebook)
    # make client_type to code? -> how?
    # just init -> crash with ray
    # so split server and notebook api
    # same api but works different by env
    # if notebook skip init ray
    # want to use aib, init() code inside
    #
    try:
        client_info = aib_client.aib_info
        url = client_info.AIB_IFLOW_SERVER_URL + "/dataset/" + client_info.PROJECT_ID
        res = requests.get(url, timeout=10)
    except Exception as exc:
        raise exc
    else:
        if res.status_code == 200:
            if res.json().get("CODE") == "SUCCESS":
                print(res.json())
            else:
                print("export fail on aib server error msg: " + res.json().get("ERROR_MSG"))
        else:
            print("export fail. status code: " + str(res.status_code))


@dataclass
class DATASET_TYPE:
    RAY = "ray_dataset"
    NUMPY = "numpy"
