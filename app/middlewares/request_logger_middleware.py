import json
import random
import string
import time

from fastapi.encoders import jsonable_encoder
from loguru import logger

from fastapi import Request
from starlette.concurrency import iterate_in_threadpool


class RequestLoggerMiddleware:
    async def __call__(self, request: Request, call_next):
        idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        start_time = time.time()
        request_body = await request.body()
        request_body = json.loads(request_body.decode()) if request_body else None

        request.state.user = None
        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)
        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        try:
            response_body = json.loads(b"".join(response_body).decode())
        except json.JSONDecodeError:
            response_body = jsonable_encoder(b"".join(response_body).decode())

        logger.bind(
            request_id=idem,
            process_time=formatted_process_time,
            user=request.state.user,
            method=request.method,
            path=request.url.__str__(),
            request_body=request_body,
            response_body=response_body,
            # json.loads(b"".join(response_body).decode()) if response_body else {},
        ).info(f"rid={idem} end request path={request.url.path}")
        return response

    @staticmethod
    def serialize(record):
        subset = {
            "time": record["time"].isoformat(),
            "level": record["level"].name,
            "user": record["extra"]["user"],
            "message": record["message"],
            "request_id": record["extra"]["request_id"],
            "process_time": record["extra"]["process_time"],
            "method": record["extra"]["method"],
            "path": record["extra"]["path"],
            "request_body": record["extra"]["request_body"],
            "response_body": record["extra"]["response_body"],
        }

        if "exception" in record:
            subset["exception"] = record["exception"]

        return json.dumps(subset)

    def formatter(self, record):
        record["extra"]["serialized"] = self.serialize(record)
        return "{extra[serialized]}\n"


logger.add(
    "logs/server.log",
    rotation="1 days",
    retention="7 days",
    level="INFO",
    compression="gz",
    format=RequestLoggerMiddleware().formatter,
)
