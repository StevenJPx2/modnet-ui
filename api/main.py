import functions_framework

from .modnet import process_images_from_path


@functions_framework.http
def hello(request):
    return "Hello world!"


@functions_framework.http
def process_image(request):
    request_json = request.get_json()
    process_images_from_path(
        request_json["input_path"],
        request_json["output_path"],
    )
    return request_json, 200
