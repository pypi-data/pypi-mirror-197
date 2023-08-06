import requests
import functools
import types
import codecs
from typing import Literal

import dill

from .component import Component
from .utils import get_input_info, get_output_info, get_func_script
from aib._private.utils.utils import init_check
from aib._private.utils.VO import ImportComponentVO, ExportComponentVO, IsConcatenableVO
import aib._private.client as aib_client


def import_component(name: str) -> Component | None:
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
                del res["CODE"]
                del res["ERROR_MSG"]
                try:
                    imported_component = ImportComponentVO.parse_obj(res)
                    name = imported_component.NAME
                    script = imported_component.SCRIPT
                    component_type = imported_component.TYPE
                    func = dill.loads(codecs.decode(imported_component.TASK.encode(), "base64"))
                except Exception as exc:
                    raise exc
                else:
                    print(f"import component {name} : success")
                    return Component(name=name, func_str=script, func=func, component_type=component_type)
            else:
                print("export fail on aib server error msg: " + res.json().get("ERROR_MSG"))
        else:
            print("export fail. status code: " + str(res.status_code))


def export_component(name: str, func: callable,
                     component_type: Literal["default", "global", "branch"] = "default") -> None:
    try:
        init_check()
    except Exception as exc:
        raise exc
    client_info = aib_client.aib_info
    url = client_info.AIB_IFLOW_SERVER_URL + "/component/export"
    if isinstance(func, (types.FunctionType, types.BuiltinFunctionType, functools.partial)):
        try:
            func_pickle = codecs.encode(dill.dumps(func), "base64").decode()
        except Exception as exc:
            print(exc.__str__())
            raise exc
        func_string = get_func_script(func)
        try:
            output_info = get_output_info(func=func, func_str=func_string)
            input_info = get_input_info(func=func)
            if component_type == "branch":
                if len(output_info) > 1 or output_info[0] != "bool":
                    raise Exception("branch type component must return boolean only")
        except Exception as exc:
            raise exc
        else:
            data = ExportComponentVO(SCRIPT=func_string,
                                     OUTPUT=output_info,
                                     INPUT=input_info,
                                     TASK=func_pickle,
                                     PROJECT_ID=client_info.PROJECT_ID,
                                     USER=client_info.USER,
                                     NAME=name)
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            try:
                res = requests.post(url, data=data.json(), headers=headers, timeout=10)
            except Exception as exc:
                raise exc
            else:
                if res.status_code == 200:
                    if res.json().get("CODE") == "SUCCESS":
                        print("export success")
                    else:
                        print("export fail on aib server error msg: " + res.json().get("ERROR_MSG"))
                else:
                    print("export fail. status code: " + str(res.status_code))
    else:
        raise AttributeError("can't export, is not function")


def update_component(component: Component) -> None:
    try:
        init_check()
    except Exception as exc:
        raise exc
    client_info = aib_client.aib_info
    url = client_info.AIB_IFLOW_SERVER_URL + "/component/update"
    data = ExportComponentVO(SCRIPT=component.func_string,
                             OUTPUT=component.output,
                             INPUT=component.input,
                             TASK=component.pickled_func,
                             TYPE=component.component_type,
                             PROJECT_ID=client_info.PROJECT_ID,
                             USER=client_info.USER,
                             DATASET=client_info.DATASET,
                             NAME=component.name)
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    try:
        res = requests.post(url, data=data.json(), headers=headers, timeout=10)
    except Exception as exc:
        raise exc
    else:
        if res.status_code == 200:
            if res.json().get("CODE") == "SUCCESS":
                print("update success")
            else:
                print("update fail on aib server error msg: " + res.json().get("ERROR_MSG"))
        else:
            print("update fail. status code: " + str(res.status_code))


def delete_component(name: str) -> None:
    try:
        init_check()
    except Exception as exc:
        raise exc
    client_info = aib_client.aib_info
    url = client_info.AIB_IFLOW_SERVER_URL + "/component/" + client_info.PROJECT_ID + "/" + name
    try:
        res = requests.delete(url, timeout=10)
    except Exception as exc:
        raise exc
    else:
        if res.status_code == 200:
            code = res.json().get("CODE")
            if code == "SUCCESS":
                print(f"import component {name} : success")
            else:
                print("delete fail on aib server error msg: " + res.json().get("ERROR_MSG"))
        else:
            print("delete fail. status code: " + str(res.status_code))


def get_component_list():
    try:
        init_check()
    except Exception as exc:
        raise exc
    client_info = aib_client.aib_info
    url = client_info.AIB_IFLOW_SERVER_URL + "/component/" + client_info.PROJECT_ID
    try:
        res = requests.get(url, timeout=10)
    except Exception as exc:
        raise exc
    else:
        if res.status_code == 200:
            code = res.json().get("CODE")
            if code == "SUCCESS":
                res = res.json().get("COMPONENT_LIST")
                return res
            else:
                print("fail to get_component_info : aib server error msg: " + res.json().get("ERROR_MSG"))
                return None
        else:
            raise Exception("fail to get_component_info. status code: " + str(res.status_code))