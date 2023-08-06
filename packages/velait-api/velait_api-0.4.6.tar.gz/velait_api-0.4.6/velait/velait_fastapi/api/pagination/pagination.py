import json
from typing import Iterable

from fastapi import Request
from starlette.datastructures import URL

from velait.velait_fastapi.api.pagination.schemas import Page, PageInfo


def __create_param(page: int, size: int):
    return json.dumps({"page": page, "size": size})


def get_next_page(url: URL, current_page: int, last_page: int, page_size: int):
    if current_page == last_page:
        return None

    return str(url.include_query_params(page=__create_param(page=last_page, size=page_size)))


def get_prev_page(url: URL, current_page: int, page_size: int):
    if current_page == 0:
        url.remove_query_params('page')
        return str(url)

    return str(url.include_query_params(page=__create_param(page=current_page - 1, size=page_size)))


def paginate(
    request: Request,
    page_size: int,
    data: Iterable,
    total_count: int,
) -> Page:
    last_page = total_count // page_size
    current_page = request.path_params.get('page', 0)

    return Page(
        results=list(data),
        pagination=PageInfo(
            total_records=total_count,
            total_pages=1 if total_count < page_size else last_page,
            first=str(request.url.remove_query_params('page')),
            last=str(request.url.include_query_params(page=__create_param(page=last_page, size=page_size))),
            next=get_next_page(
                url=request.url,
                last_page=last_page,
                current_page=current_page,
                page_size=page_size,
            ),
            previous=get_prev_page(
                url=request.url,
                current_page=current_page,
                page_size=page_size,
            ),
        ),
    )


__all__ = [
    'paginate',
]
