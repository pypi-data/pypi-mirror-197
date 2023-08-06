import inspect
import re
import sys
from io import StringIO

from IPython import get_ipython

from .exceptions import *
from .artifacts import ModelType, DatasetType

as_str_artifact = "artifacts."


def get_output_info(func: callable, func_str: str = None) -> list[str]:
    output = []
    try:
        output_type = func.__annotations__["return"]
    except KeyError as exc:
        raise AnnotationNotDefined(exc.__str__())
    if func_str is not None:
        output_str = str(output_type)
        out_tuple_count = output_str.count("tuple")
        if out_tuple_count >= 1:
            output_types = re.search(r'tuple\[(.*)\]', output_str)
            output_types = output_types.group(1)
            an_types = re.findall(r"\[.*?]", output_types)
            type_map = {}
            for idx, an_type in enumerate(an_types):
                output_types = output_types.replace("typing.Annotated" + an_type, str(idx))
                type_map[str(idx)] = an_type
            output_types = output_types.replace(' ', '')
            output_types = output_types.split(',')
            for idx, output_type in enumerate(output_types):
                if output_type in type_map:
                    an_type = type_map[output_type]
                    if "ModelAnnotation" in an_type:
                        for attribute in ModelType.__dict__:
                            if attribute in an_type:
                                output_types[idx] = "Model[" + attribute + "]"
                                break
                        else:
                            UnknownArtifact(an_type)
                    elif "DatasetAnnotation" in an_type:
                        for attribute in DatasetType.__dict__:
                            if attribute in an_type:
                                output_types[idx] = "Dataset[" + attribute + "]"
                                break
                        else:
                            UnknownArtifact(an_type)
                    else:
                        raise UnknownArtifact(an_type)
            return output_types
        else:
            output_type_name = output_type.__name__
            if output_type_name == "Annotated":
                if as_str_artifact in output_str:
                    artifact_type_idx = output_str.index(as_str_artifact) + len(as_str_artifact)
                    artifact_type = output_str[artifact_type_idx:].split(",")[0]
                    if hasattr(ModelType, artifact_type):
                        output.append("Model[" + artifact_type + "]")
                    elif hasattr(DatasetType, artifact_type):
                        output.append("Dataset[" + artifact_type + "]")
                    else:
                        raise UnknownArtifact(artifact_type)
            else:
                output.append(output_type_name)
            return output
    else:
        print("can't capture script, skipping output validation")
        output_type_name = output_type.__name__
        output_str = str(output_type)
        if output_type_name == "Annotated":
            if as_str_artifact in output_str:
                artifact_type_idx = output_str.index(as_str_artifact) + len(as_str_artifact)
                artifact_type = output_str[artifact_type_idx:].split(",")[0]
                if hasattr(ModelType, artifact_type):
                    output.append("Model[" + artifact_type + "]")
                else:
                    raise UnknownArtifact(artifact_type)
        else:
            output.append(output_type_name)
    return output


def get_input_info(func: callable) -> dict[str, str]:
    input_info = {}
    arg_spec = inspect.getfullargspec(func)
    args = arg_spec.args
    annotations = arg_spec.annotations
    if "return" in annotations:
        del annotations["return"]
    if len(args) != len(annotations):
        raise InvalidInputAnnotation(f"component input:{args}, but given input annotation:{annotations}")
    for k, v in annotations.items():
        input_type = v.__name__
        if input_type == "Annotated":
            v = str(v)
            if as_str_artifact in v:
                artifact_type_idx = v.index(as_str_artifact) + len(as_str_artifact)
                artifact_type = v[artifact_type_idx:].split(",")[0]
                if hasattr(ModelType, artifact_type):
                    input_info[k] = "Model[" + artifact_type + "]"
                elif hasattr(DatasetType, artifact_type):
                    input_info[k] = "Dataset[" + artifact_type + "]"
                else:
                    raise UnknownArtifact(artifact_type)
        else:
            input_info[k] = input_type
    return input_info


def get_func_script(func: callable):
    ipython = get_ipython()
    if ipython:
        with Capturing() as output:
            ipython.run_line_magic("pinfo2", func.__name__)
        s_idx = -1
        e_idx = -1
        for idx, line in enumerate(output):
            if "Source" in line:
                s_idx = idx + 1
            elif "File" in line or "Type" in line:
                e_idx = idx - 1
        if s_idx != -1 and e_idx != -1:
            func_string = '\n'.join(output[s_idx:e_idx])
            print(f"component script is: \n {func_string}")
            return func_string
        else:
            raise GetScriptFromMagicError("\n".join(output))
    else:
        try:
            func_string = inspect.getsource(func)
            print(f"component script is: \n {func_string}")
            return func_string
        except Exception as exc:
            raise GetScriptFromInspectionError(exc.__str__())


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout
