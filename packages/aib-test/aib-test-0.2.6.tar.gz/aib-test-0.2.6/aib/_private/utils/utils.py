def init_check() -> None:
    import aib._private.client as aib_client
    from aib._private.exceptions import NotInitiated
    try:
        if aib_client.aib_info.IS_INIT:
            pass
        else:
            raise NotInitiated
    except AttributeError:
        raise NotInitiated

