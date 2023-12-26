"""
Main functions for '/api_taro/get_taro_answer' request
"""

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from utils.file import get_json_data
from utils.helper import get_log

from postgresql import ClientPostgreSQL
from app.utils.postgresql.requests import get_request_by_id

def get_taro_answer(bd: ClientPostgreSQL):
    """
    Route for '/api_taro/get_taro_answer' request

    Examination: curl http://127.0.0.1:3100/api_taro/get_taro_answer/1

    :param bd: An instance of the ClientPotgreSQL class representing the PostgreSQL database.
    :type bd: ClientPostgreSQL
    """

    async def route(request: Request):
        """
        Body of route

        :param request: Request from user
        :type request: Request
        """

        response = {}

        try:
            counter_cards = 0
            id = int(request.path_params['id'])
            item = await get_request_by_id(bd = bd, id = id)

            data = f"""<h1 class="fade-in">Карты</h1>
            <div class="cards">"""

            for name in item['cards']:
                data += f"""
                <div class="card" style="--card-index:{counter_cards}; --start-position:{(-1)**counter_cards*1000}vw;">
                    <img src="{name}" alt="Карта {counter_cards}">
                </div>"""
                counter_cards += 1

            data += f"""
            </div>

            <div class="divider"></div>

            <div class="fade-in">
                <div class="text-background">
                    <h1>Запрос</h1>
                    <p>
                         {item['request']}
                    </p>
                </div>
            </div>

            <div class="divider"></div>

            <div class="fade-in">
                <div class="text-background">
                    <h1>Объяснение</h1>
                    <p>
                    {item['response']}
                    </p>
                </div>
            </div>
        """
            response = {"data": data}
        except Exception as e:
            request.app.logger.error(get_log(s = "-", text = e))
            response = {"error": e}

        return JSONResponse(content=response)
    return route

def setup(app: FastAPI, bd: ClientPostgreSQL):
    """
    Func for setup get_taro_answer route
    """

    app.add_api_route("/api_taro/get_taro_answer/{id}", get_taro_answer(bd), methods=["GET"])