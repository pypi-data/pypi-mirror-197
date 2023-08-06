import codecs
import dataclasses
import types
import functools
import requests
from typing import Literal

import dill

from .utils import get_func_script, get_output_info, get_input_info
from aib._private.utils.utils import init_check
import aib._private.client as aib_client
from aib._private.utils.VO import ExportComponentVO


class Component(object):
    def __init__(self, name: str, func: callable,
                 component_type: Literal["default", "branch"] = "default",
                 func_str: str = None):
        self.__name: str = name
        self.__component_type: Literal["default", "branch"] = component_type
        self.__func: callable = func  # allow only
        self.__func_string: str = func_str
        self.__pickled_func: str | None = None
        self.__output: list[str, str] | None = None
        self.__input: dict[str, str] | None = None
        self._init()

    def __call__(self, *args, **kwargs):
        return self.__func(*args, **kwargs)

    def _init(self):
        if self.__func_string is None:
            self.__func_string = get_func_script(self.__func)
        self.__pickled_func: str = codecs.encode(dill.dumps(self.__func), "base64").decode()
        input_info = get_input_info(func=self.__func)
        output_info = get_output_info(func=self.__func, func_str=self.__func_string)
        self.__input = input_info
        self.__output = output_info
        if self.__component_type == "branch":
            if len(output_info) > 1 or output_info[0] != "bool":
                raise Exception("branch type component must return boolean only")

    def export(self):
        try:
            init_check()
        except Exception as exc:
            raise exc
        client_info = aib_client.aib_info
        url = client_info.AIB_IFLOW_SERVER_URL + "/component/export"
        if isinstance(self.__func, (types.FunctionType, types.BuiltinFunctionType, functools.partial)):
            data = ExportComponentVO(SCRIPT=self.__func_string,
                                     OUTPUT=self.__output,
                                     INPUT=self.__input,
                                     TASK=self.__pickled_func,
                                     TYPE=self.__component_type,
                                     PROJECT_ID=client_info.PROJECT_ID,
                                     USER=client_info.USER,
                                     NAME=self.__name)
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            try:
                res = requests.post(url, data=data.json(), headers=headers, timeout=10)
                print(res.json())
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

    @property
    def name(self):
        return self.__name

    @property
    def output(self):
        return self.__output

    @property
    def input(self):
        return self.__input

    @property
    def func_string(self):
        return self.__func_string

    @property
    def pickled_func(self):
        return self.__pickled_func

    @property
    def func(self):
        return self.__func

    @property
    def component_type(self):
        return self.__component_type

    @func.setter
    def func(self, func):
        self.__func = func
        self.__func_string = get_func_script(self.__func)
        self._init()

    def reset(self, func: callable):
        self.__func = func
        self.__func_string = get_func_script(self.__func)
        self._init()


@dataclasses.dataclass
class ComponentType:
    DEFAULT: str = "default"
    BRANCH: str = "branch"
