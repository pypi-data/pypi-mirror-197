class AnnotationNotDefined(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return "Annotation Not defined:" + self.msg


class TypeNotMatched(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return "Type not matched:" + self.msg


class InvalidOutputAnnotation(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return "invalid output annotation:" + self.msg


class InvalidInputAnnotation(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return "invalid input annotation:" + self.msg


class NotSupportedType(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return "given type is not supported:" + self.msg


class UnknownArtifact(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return "unknown artifact:" + self.msg


class GetScriptFromMagicError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return "can't get function script from:" + self.msg


class GetScriptFromInspectionError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return "can't get function script from inspection:" + self.msg
