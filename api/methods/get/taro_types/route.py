"""
Main functions for '/api_taro/get_types_taro' request
"""

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from utils.file import get_json_data
from utils.helper import get_log

def get_taro_types(request: Request):
    """
    Route for '/api_taro/get_types_taro' request

    Examination: curl http://127.0.0.1:3100/api_taro/get_types_taro

    :param request: Request from user
    :type request: Request
    """

    response = {}

    try:
        types = get_json_data(file_name = "data/types_taro.json")
        data = ""

        for key, value in types.items():
            data += f"""
<div class="card" id="{key}" onclick="choise_type_taro('{key}');">
    <span class="card-description">{value}</span>
</div>
<style type="text/css">
    #{key} {{
        background: linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.75), rgba(0,0,0,0.25))");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
        border: 2px solid #000000;
    }}
</style>
"""
        response = {"data": data}
    except Exception as e:
        request.app.logger.error(get_log(s = "-", text = e))
        response = {"error": e}

    return JSONResponse(content=response)

def setup(app: FastAPI):
    """
    Func for setup get_taro_types route
    """

    app.add_api_route("/api_taro/get_types_taro", get_taro_types, methods=["GET"])