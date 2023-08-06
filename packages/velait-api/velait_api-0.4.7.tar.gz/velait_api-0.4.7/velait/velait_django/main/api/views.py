import re
from typing import Type

from django.conf import settings
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ModelSerializer

from velait.common.exceptions import VelaitError
from velait.velait_django.main.models import BaseModel
from velait.velait_django.main.api.serializers import BaseSerializer
from velait.velait_django.main.api.responses import APIResponse
from velait.velait_django.main.api.pagination import VelaitPagination, VelaitPaginationInspector
from velait.velait_django.main.services.services import filter_objects
from velait.velait_django.main.services.search import SearchError, DjangoSearch


class SearchView(GenericAPIView):
    model: Type[BaseModel] = None
    serializer_class: Type[ModelSerializer] = None
    search_class: Type[DjangoSearch] = DjangoSearch
    pagination_class = VelaitPagination

    def __init__(self, *args, **kwargs):
        super(SearchView, self).__init__(*args, **kwargs)

        if self.model is None or self.serializer_class is None:
            raise NotImplementedError("Model or Serializer were not supplied to the SearchView")

    def get_search_object(self):
        return self.search_class(
            search_=self.request.GET.get('search'),
            query=self.request.GET.get('query'),
            ordering=self.request.GET.get('ordering'),
            model=self.model,
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="search",
                in_=openapi.IN_QUERY,
                type='string',
                description='Search string',
            ),
            openapi.Parameter(
                name="query",
                in_=openapi.IN_QUERY,
                type='[{ fn: string, op: string, fv: any }]',
                description='Query parameter for search',
            ),
            openapi.Parameter(
                name="ordering",
                in_=openapi.IN_QUERY,
                type='string',
                description='Ordering fields separated by commas. Use - in front of the field to order by desc',
            ),
            openapi.Parameter(
                name="page",
                in_=openapi.IN_QUERY,
                type='{ offset: int, page: int }',
                description='Page parameter for pagination.',
            ),
        ],
        pagination_class=VelaitPagination,
        paginator_inspectors=[VelaitPaginationInspector],
    )
    def get(self, request, *args, **kwargs):
        try:
            search = self.get_search_object()
            paginator = self.pagination_class()
            queryset = paginator.paginate_queryset(queryset=search.search(), request=request, view=self)
            return paginator.get_paginated_response(self.serializer_class(instance=queryset, many=True).data)

        except SearchError as exc:
            return APIResponse(errors=[exc], status=400)


class ModelRefsView(GenericAPIView):
    model: Type[BaseModel]
    serializer_class: Type[BaseSerializer]
    model_objects: str = 'objects'
    UUID_FIELD_NAME: str = 'id'
    pagination_class = VelaitPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="ids",
                in_=openapi.IN_QUERY,
                type='list',
                description="Ids of the models you need to query",
            ),
        ],
        pagination_class=VelaitPagination,
        paginator_inspectors=[VelaitPaginationInspector],
    )
    def get(self, request: Request, *args, **kwargs):
        searched_ids = request.query_params.get('ids')

        if searched_ids is None:
            return APIResponse(errors={
                VelaitError(
                    name="query",
                    description=_("You must provide 'ids' query parameter to use this view"),
                ),
            })
        elif len(searched_ids) > getattr(settings, 'ID_LISTING_MAX_LEN', 40000):
            return APIResponse(errors={
                VelaitError(
                    name="query",
                    description=_("Your 'ids' are too long. Try shortening them"),
                ),
            })

        numerical_ids, uuids = [], []

        for id_ in searched_ids.split(","):
            if re.fullmatch(r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})", id_):
                uuids.append(id_)
            elif re.fullmatch(r'\d+', id_):
                numerical_ids.append(int(id_))
            else:
                return APIResponse(errors={
                    VelaitError(
                        name="query",
                        description=_("Id must be numbers or UUID. Your format is invalid"),
                    ),
                })

        return APIResponse(
            data=self.serializer_class(
                instance=filter_objects(
                    getattr(self.model, self.model_objects),
                    Q(pk__in=numerical_ids) | Q(**{f"{self.UUID_FIELD_NAME}__in": uuids}),
                    limit=getattr(settings, "ID_LISTING_MAX_RESULTS", 300),
                ),
                many=True,
            ).data,
            status=200,
        )


__all__ = [
    'ModelRefsView',
    'SearchView',
]
