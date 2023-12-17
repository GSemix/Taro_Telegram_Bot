"""
Staffing and launching API
"""

import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from . import app
from . import api_cfg
from . import api_logger
from . import log_stuff

from .events.startup import setup as event_startup_setup
from .events.shutdown import setup as event_shutdown_setup
from .methods.get.hello import setup as method_get_hello_setup
from .methods.get.taro_types import setup as method_get_taro_types_setup

app.middleware("http")(log_stuff)
app.add_middleware(     # Добавляем CORS-мидлвэр для обработки CORS-заголовков
    CORSMiddleware,
    allow_origins=api_cfg.allow_origins.get_secret_value().split(", "),    # Разрешает все источники. Это говорит браузеру, что он может делать запросы с любого домена.
    allow_methods=api_cfg.allow_methods.get_secret_value().split(", "),    # Разрешает все методы.
    allow_headers=api_cfg.allow_headers.get_secret_value().split(", ")     # Разрешает все заголовки.
)

event_startup_setup(app, api_logger)
event_shutdown_setup(app, api_logger)
method_get_hello_setup(app)
method_get_taro_types_setup(app)

uvicorn.run(
    api_cfg.app.get_secret_value(),
    host=api_cfg.host.get_secret_value(),
    port=int(api_cfg.port.get_secret_value()),
    workers=int(api_cfg.workers.get_secret_value())
)



