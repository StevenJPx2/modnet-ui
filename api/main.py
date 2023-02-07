import base64
import io
from functools import wraps
from typing import Callable, ParamSpec, TypedDict, TypeVar, cast

import functions_framework
from flask import Request

from .modnet import process_images_from_path, process_single_image

A = ParamSpec("A")  # arguments
R = TypeVar("R", tuple, list, covariant=True)  # return type


def cross_origin(origin: str = "*"):
    def cross_origin_fn(fn: Callable[[Request], R]):
        @wraps(fn)
        def wrapped_fn(request: Request):
            if request.method == "OPTIONS":
                # Allows GET requests from any origin with the Content-Type
                # header and caches preflight response for an 3600s
                headers = {
                    "Access-Control-Allow-Origin": origin,
                    "Access-Control-Allow-Methods": "POST",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Max-Age": "3600",
                }

                return ("", 204, headers)
            headers = {
                "Access-Control-Allow-Methods": "POST",
                "Access-Control-Allow-Origin": origin,
            }
            return (*fn(request), headers)

        return wrapped_fn

    return cross_origin_fn


@functions_framework.http
def process_images_from_folder(request: Request):
    JSON = TypedDict("JSON", {"input_path": str, "output_path": str})

    if (request_json := request.get_json()) is not None:
        request_json = cast(JSON, request_json)
        process_images_from_path(
            request_json["input_path"],
            request_json["output_path"],
        )
    return request_json, 200


@functions_framework.http
@cross_origin()
def process_image(request: Request):
    print(request, request.headers)
    raw_data = io.BytesIO()
    image = process_single_image(request.data)
    image.save(raw_data, request.headers["Content-Type"].split("/")[1])
    raw_data.seek(0)
    return (
        base64.b64encode(raw_data.read()).decode("utf8"),
        200,
    )


@functions_framework.errorhandler(Exception)
def handle_error(e):
    return f"Err: {e}", 500
