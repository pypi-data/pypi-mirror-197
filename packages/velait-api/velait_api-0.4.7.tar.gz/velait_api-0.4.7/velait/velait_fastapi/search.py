from typing import Optional, Any

from fastapi import Query
from assimilator.core.database import Repository

from velait.common.services.exceptions import PaginationLimitsError
from velait.common.services.pagination import get_page_limits
from velait.common.services.search import Search, SearchError, SearchOperator


class AlchemyRepositorySearch(Search):
    def __init__(
        self,
        repository: Repository,
        search_: Optional[str] = None,
        query: str = Query(default=None),
        ordering: Optional[str] = None,
        page: Optional[Any] = None,
        default_pagination_size: int = 10,
    ):
        self.repository = repository
        self._page = self._parse_json(page, key_name='page') if (page is not None) else None
        self.default_pagination_size = default_pagination_size
        super(AlchemyRepositorySearch, self).__init__(
            search=search_,
            query=query,
            ordering=ordering,
            model=repository.model,
        )

    def validate(self):
        super(AlchemyRepositorySearch, self).validate()

        if self._page is None:
            self._page = {
                "offset": 1,
                "size": self.default_pagination_size,
            }
            return

        if not isinstance(self._page, dict):
            raise SearchError(
                name="page",
                description="Invalid structure of 'page'",
            )

        if self._page.get('offset', 0) <= 0:
            self._page['offset'] = 1

        if self._page.get('size', 0) <= 0:
            self._page['size'] = self.default_pagination_size

    def _parse_ordering(self): return self._ordering

    def search(self):
        try:
            filter_spec = self.repository.specifications.filter(*self.parse_query_filters())

            offset, limit = get_page_limits(
                page=self._page['offset'] - 1,
                page_size=self._page['size'],
            )
            pagination_spec = self.repository.specifications.paginate(offset=offset, limit=limit)

            if self._ordering:
                return self.repository.filter(
                    filter_spec,
                    pagination_spec,
                    self.repository.specifications.order(*self._parse_ordering()),
                    lazy=True,
                )

            return self.repository.filter(filter_spec, pagination_spec, lazy=True)

        except PaginationLimitsError:
            raise SearchError(
                name='page',
                description="'page' parameter contains invalid values",
            )
        except Exception:
            raise SearchError(
                name="search",
                description="Search could not be conducted",
            )

    def _parse_operator(self, field_name: str, operator: str, field_value: str):
        """
        Creates an expression object if all input operators are valid.
        If they are not, raises op an exception
        """

        if operator == "equals":
            return getattr(self.repository.model, field_name) == field_value
        elif operator == "lessOrEqual":
            return getattr(self.repository.model, field_name) <= field_value
        elif operator == "greaterOrEqual":
            return getattr(self.repository.model, field_name) >= field_value
        elif operator == "greater":
            return getattr(self.repository.model, field_name) > field_value
        elif operator == "less":
            return getattr(self.repository.model, field_name) < field_value
        elif operator == "contains":
            return getattr(self.repository.model, field_name).in_(field_value)
        else:
            raise SearchError(
                name="query",
                description=f"Operation '{operator}' is unknown",
            )


__all__ = [
    'SearchError',
    'SearchOperator',
    'AlchemyRepositorySearch',
]
