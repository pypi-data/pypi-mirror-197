from pydantic import BaseModel, Extra


class ExportComponentVO(BaseModel):
    SCRIPT: str
    TYPE: str
    OUTPUT: list[str]
    INPUT: dict[str, str]
    TASK: str
    PROJECT_ID: str
    USER: str
    NAME: str

    class Config:
        extra = Extra.forbid


class ImportComponentVO(BaseModel):
    OUTPUT: str
    SCRIPT: str
    INPUT: str
    TYPE: str
    TASK: str
    NAME: str

    class Config:
        extra = Extra.forbid


class ComponentInfoVO(BaseModel):
    OUTPUT: str
    SCRIPT: str
    INPUT: str
    TYPE: str
    NAME: str

    class Config:
        extra = Extra.forbid


class ComponentTypeVO(BaseModel):
    TYPE: str
    NAME: str

    class Config:
        extra = Extra.forbid


class IsConcatenableVO(BaseModel):
    CMPNT_FROM: str
    CMPNT_TO: str
    PROJECT_ID: str

    class Config:
        extra = Extra.forbid


class ExportPipelineVO(BaseModel):
    PROJECT_ID: str
    USER: str
    NAME: str
    DEF: str
    ROOT_IDX: int

    class Config:
        extra = Extra.forbid


class MysqlInfoVO(BaseModel):
    USER: str
    PASSWORD: str
    IP: str
    PORT: str
    DB: str

    class Config:
        extra = Extra.forbid


class ExportModelVO(BaseModel):
    PROJECT_ID: str
    MODEL_NAME: str
    MODEL_TYPE: str

    class Config:
        extra = Extra.forbid


class BaseComponentVO(BaseModel):
    PROJECT_ID: str
    NAME: str

    class Config:
        extra = Extra.forbid


class ComponentLinkCheckVO(BaseModel):
    PROJECT_ID: str
    COMPONENT_FROM: str
    COMPONENT_TO:  str

    class Config:
        extra = Extra.forbid
