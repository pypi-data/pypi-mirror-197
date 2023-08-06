import requests
import json
from queue import Queue

from aib._private.utils.VO import ComponentInfoVO, ExportPipelineVO, BaseComponentVO, ComponentLinkCheckVO, ComponentTypeVO
import aib._private.client as aib_client
from aib._private.utils.utils import init_check
from .component import ComponentType


class Pipeline(object):
    def __init__(self, name: str):
        try:
            init_check()
        except Exception as exc:
            raise exc
        self.__name = name
        self.__client_info = aib_client.aib_info
        self.__pipeline_l: list[dict] = []
        self.__pipeline: dict = {}
        self.__node_idx: int = 0
        self.__root_idx: int | None = None

    def link(self, f_node_idx: int, t_node_idx: int):
        if f_node_idx in self.__pipeline and t_node_idx in self.__pipeline:
            if f_node_idx == t_node_idx:
                raise Exception("can't make link with same node")
            f_node = self.__pipeline[f_node_idx]
            if t_node_idx in f_node["child"]:
                raise Exception("already linked")
            if not is_linkable(self.__pipeline[f_node_idx]["name"], self.__pipeline[t_node_idx]["name"]):
                raise Exception("input didn't matched with output")

            is_loop = False
            que = Queue()
            que.put(self.__pipeline[t_node_idx]["child"])
            while True:
                if que.empty():
                    break
                child_list = que.get()
                if f_node_idx in child_list:
                    if self.__pipeline[f_node_idx]["type"] != ComponentType.BRANCH:
                        is_loop = True
                        break
                for child in child_list:
                    que.put(self.__pipeline[child]["child"])
            if is_loop:
                raise Exception("looped")
            f_node["child"].append(t_node_idx)
        else:
            raise Exception("node not exist")

    def remove_link(self, f_node_idx: int, t_node_idx: int):
        if f_node_idx in self.__pipeline and t_node_idx in self.__pipeline:
            f_node = self.__pipeline[f_node_idx]
            idx = f_node["child"].index(t_node_idx)
            del f_node["child"][idx]
        else:
            raise Exception("node not exist")

    def set_root(self, node_idx: int):
        self.__root_idx = node_idx

    def append_node(self, name: str):
        component_type = get_component_type(name)
        if component_type is None:
            raise Exception("can't load component")
        node = {"name": name, "type": component_type.TYPE, "child": []}
        self.__pipeline[self.__node_idx] = node
        self.__node_idx += 1

    def remove_node(self, node_idx: int):
        for key, value in self.__pipeline.items():
            for idx, child in enumerate(value["child"]):
                if child == node_idx:
                    del child[idx]
        del self.__pipeline[node_idx]

    def show_pipeline(self):
        print(json.dumps(self.__pipeline, indent=4))

    def export(self):
        if self.__root_idx is None:
            raise Exception("root node is not defined")
        client_info = aib_client.aib_info
        url = client_info.AIB_IFLOW_SERVER_URL + "/pipeline/export"
        data = ExportPipelineVO(PROJECT_ID=client_info.PROJECT_ID,
                                USER=client_info.USER,
                                NAME=self.__name,
                                DEF=str(self.__pipeline),
                                ROOT_IDX=self.__root_idx)
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        try:
            res = requests.post(url, data=data.json(), headers=headers, timeout=10)
        except Exception as exc:
            raise exc
        else:
            if res.status_code == 200:
                res_j = res.json()
                code = res_j.get("CODE")
                if code == "SUCCESS":
                    print("success to export pipeline")
                else:
                    print("request export_pipeline fail on aib server error msg: " + res.json().get("ERROR_MSG"))
            else:
                print("request export_pipeline fail. status code: " + str(res.status_code))


def get_component_type(name: str) -> ComponentTypeVO | None:
    try:
        init_check()
    except Exception as exc:
        raise exc
    client_info = aib_client.aib_info
    url = client_info.AIB_IFLOW_SERVER_URL + "/component/type/" + client_info.PROJECT_ID + "/" + name
    try:
        res = requests.get(url, timeout=10)
    except Exception as exc:
        raise exc
    else:
        if res.status_code == 200:
            code = res.json().get("CODE")
            if code == "SUCCESS":
                res = res.json()
                component_type = ComponentTypeVO.parse_obj({"TYPE": res["TYPE"], "NAME": res["NAME"]})
                return component_type
            else:
                print("fail to get_component_info : aib server error msg: " + res.json().get("ERROR_MSG"))
                return None
        else:
            raise Exception("fail to get_component_info. status code: " + str(res.status_code))


def get_component_info(name: str) -> ComponentInfoVO | None:
    try:
        init_check()
    except Exception as exc:
        raise exc
    client_info = aib_client.aib_info
    url = client_info.AIB_IFLOW_SERVER_URL + "/component/" + client_info.PROJECT_ID + "/" + name
    try:
        res = requests.get(url, timeout=10)
    except Exception as exc:
        raise exc
    else:
        if res.status_code == 200:
            code = res.json().get("CODE")
            if code == "SUCCESS":
                res = res.json()
                component_info = ComponentInfoVO.parse_obj(res)
                return component_info
            else:
                print("fail to get_component_info : aib server error msg: " + res.json().get("ERROR_MSG"))
                return None
        else:
            raise Exception("fail to get_component_info. status code: " + str(res.status_code))


def is_component_exist(name: str) -> bool:
    try:
        init_check()
    except Exception as exc:
        raise exc
    client_info = aib_client.aib_info
    url = client_info.AIB_IFLOW_SERVER_URL + "/component/is_exist"
    data = BaseComponentVO(PROJECT_ID=client_info.PROJECT_ID,
                           NAME=name)
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    try:
        res = requests.post(url, data=data.json(), headers=headers, timeout=10)
    except Exception as exc:
        raise exc
    else:
        if res.status_code == 200:
            code = res.json().get("CODE")
            if code == "SUCCESS":
                return True
            else:
                return False
        else:
            raise Exception("fail to is_component_exist. status code: " + str(res.status_code))


def is_linkable(f_name: str, t_name: str) -> bool:
    try:
        init_check()
    except Exception as exc:
        raise exc
    client_info = aib_client.aib_info
    url = client_info.AIB_IFLOW_SERVER_URL + "/component/is_linkable"
    data = ComponentLinkCheckVO(PROJECT_ID=client_info.PROJECT_ID,
                                COMPONENT_FROM=f_name,
                                COMPONENT_TO=t_name)
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    try:
        res = requests.post(url, data=data.json(), headers=headers, timeout=10)
    except Exception as exc:
        raise exc
    else:
        if res.status_code == 200:
            code = res.json().get("CODE")
            if code == "SUCCESS":
                res = res.json()
                if res["LINK_YN"] == "Y":
                    return True
                else:
                    return False
            else:
                raise Exception("fail to is_linkable : aib server error msg: " + res.json().get("ERROR_MSG"))
        else:
            raise Exception("fail to is_component_exist. status code: " + str(res.status_code))
