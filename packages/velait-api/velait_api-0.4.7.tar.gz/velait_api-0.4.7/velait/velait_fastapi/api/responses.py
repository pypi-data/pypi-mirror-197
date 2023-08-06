from typing import Iterable

from fastapi.responses import JSONResponse

from velait.velait_fastapi.api.schemas import BaseSchema


class APIResponse(JSONResponse):
    def __init__(
        self,
        content=None,
        status_code=200,
        headers=None,
        errors: Iterable['ResponseErrorItem'] = None,
        **kwargs
    ):
        add_pagination = False

        if errors is not None:
            content = {
                "pagination": {
                    "total_records": None,
                    "total_pages": None,
                    "first": None,
                    "last": None,
                    "next": None,
                    "previous": None,
                },
                "results": None,
                "errors": [error.dict() for error in errors],
            }
        elif isinstance(content, dict):
            add_pagination = content.get('pagination') is None
        else:
            add_pagination = True

        if add_pagination:
            content = {
                "pagination": {
                    "total_records": 1,
                    "total_pages": 1,
                    "first": None,
                    "last": None,
                    "next": None,
                    "previous": None,
                },
                "results": content,
                "errors": [],
            }

        super(APIResponse, self).__init__(
            content=content,
            status_code=status_code,
            headers=headers,
            **kwargs,
        )


class ResponseErrorItem(BaseSchema):
    name: str
    description: str


__all__ = [
    'APIResponse',
    'ResponseErrorItem',
]
