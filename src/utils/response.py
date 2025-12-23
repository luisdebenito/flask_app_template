from typing import Any, List


def error(msg: str, code: int, http_code: int):
    return __response(http_code, None, {"code": code, "message": msg})


def success(data: List[Any] | dict = None):
    return __response(200, data, None)


def __response(
    http_code: int,
    data: List[Any] | dict | None = None,
    error: dict | None = None,
):
    return (
        {"data": data, "error": error},
        http_code,
        {"Content-Type": "application/json"},
    )
