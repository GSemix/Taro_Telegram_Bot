"""
Main functions for '/api_taro/hello' request
"""

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from utils.helper import get_log

def get_hello(request: Request) -> None:
	"""
	Route for '/api_taro/hello' request

	Examination: curl http://127.0.0.1:3100/api_taro/hello

	:param request: Request from user
	:type request: Request
	"""

	response = {}

	try:
		response = {"data": "hello"}
	except Exception as e:
		request.app.logger.error(get_log(s = "-", text = e))
		response = {"error": e}

	return JSONResponse(content=response)

def setup(app: FastAPI) -> None:
	"""
	Func for setup get_hello route
	"""

	app.add_api_route("/api_taro/hello", get_hello, methods=["GET"])