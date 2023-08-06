"""Shared types."""

from typing import Any, Dict, Type, List, Optional, Union, Tuple

from dataclasses import dataclass
from logging import getLogger
from enum import Enum, IntEnum
from math import ceil

from pydantic import BaseModel

from .schemas.common_types import (  # noqa
    BreadCrumbs,
    VisibleType,
    PersonType,
    DisplayType,
    market_image,
)

from .internals import operators as op  # noqas
from .internals.operators import (  # noqa
    TypeOpEq,
    TypeOpNe,
    TypeOpGt,
    TypeOpGte,
    TypeOpLt,
    TypeOpLte,
    TypeOpRegex,
    TypeOpIn,
    TypeOpNotIn,
    TypeOpAnd,
    TypeOpOr,
    TypeOpSize,
    TypeOpExists,
    TypeExpression,
    Expression,
    ComparisonExpression,
    ComparisonListExpression,
    ConditionalExpression,
    Eq,
    Ne,
    Gt,
    Gte,
    Lt,
    Lte,
    Contains,
    IContains,
    Regex,
    IRegex,
    In,
    NotIn,
    And,
    Or,
    ArrayExists,
)

from .internals.fn import digest_branch, SafeEncoder  # noqa
from .internals.types import Expression, ExpressionError  # noqa
from .internals.messanger import (  # noqa
    Messanger,
    StatusResponse,
    SecureSchema,
    SecureQuerySchema,
    SecureStrictSchema,
)
from .internals.builtins import (  # noqa
    PaginatedResponse,
    TypeSorting,
    TypeDigest,
    TypeLang,
    TypeName,
    TypePK,
    TypeTranslate,
    TypeI18Field,
    TypeDoc,
    IndexOptions,
    Type18nDoc,
    IndexProperties,
    TypeLookup,
    TypeRaw,
    TypeSource,
    Meta,
    ViewMeta,
)

from .schemas import views
from .schemas import sources
from .schemas import raws

log = getLogger(__name__)

lang_base = 'ru'
IndexLanguages = {
    lang_base: 'ru_RU',
    'en': 'en_US',
}

lang_foreign_only = list(IndexLanguages.keys())[1:]
all_languages = [lang_base, *lang_foreign_only]

fallback_digest = '000000'


class IndexName(str, Enum):
    """Index type."""

    category = 'RawCategory'
    chart = 'RawChart'
    tag = 'RawTag'
    market_event = 'RawMarketEvent'
    domain = 'RawDomain'
    place = 'RawPlace'
    person = 'RawPerson'
    layout = 'RawLayout'
    location = 'RawLocation'

    view_category = 'ViewCategory'
    view_event = 'ViewEvent'


_state_meta = {
    IndexName.category: IndexOptions(
        name=IndexName.category,
        model=None,
        properties=IndexProperties(
            read_method='raw_categories',
            write_method='import_categories',
            schema_raw=raws.TypeCategory.schema(),
            model_raw=raws.TypeCategory,
            schema_source=sources.SourceCategory.schema(),
            model_source=sources.SourceCategory,
        ),
    ),
    IndexName.chart: IndexOptions(
        name=IndexName.chart,
        model=None,
        properties=IndexProperties(
            read_method='raw_charts',
            write_method='import_charts',
            schema_raw=raws.TypeChart.schema(),
            model_raw=raws.TypeChart,
            schema_source=sources.SourceChart.schema(),
            model_source=sources.SourceChart,
        ),
    ),
    IndexName.tag: IndexOptions(
        name=IndexName.tag,
        model=None,
        properties=IndexProperties(
            read_method='raw_tags',
            write_method='import_tags',
            schema_raw=raws.TypeTag.schema(),
            model_raw=raws.TypeTag,
            schema_source=sources.SourceTag.schema(),
            model_source=sources.SourceTag,
        ),
    ),
    IndexName.domain: IndexOptions(
        name=IndexName.domain,
        model=None,
        properties=IndexProperties(
            read_method='raw_domains',
            write_method='import_domains',
            schema_raw=raws.TypeDomain.schema(),
            model_raw=raws.TypeDomain,
            schema_source=sources.SourceDomain.schema(),
            model_source=sources.SourceDomain,
        ),
    ),
    IndexName.place: IndexOptions(
        name=IndexName.place,
        model=None,
        properties=IndexProperties(
            read_method='raw_places',
            write_method='import_places',
            schema_raw=raws.TypePlace.schema(),
            model_raw=raws.TypePlace,
            schema_source=sources.SourcePlace.schema(),
            model_source=sources.SourcePlace,
        ),
    ),
    IndexName.person: IndexOptions(
        name=IndexName.person,
        model=None,
        properties=IndexProperties(
            read_method='raw_persons',
            write_method='import_persons',
            schema_raw=raws.TypePerson.schema(),
            model_raw=raws.TypePerson,
            schema_source=sources.SourcePerson.schema(),
            model_source=sources.SourcePerson,
        ),
    ),
    IndexName.market_event: IndexOptions(
        name=IndexName.market_event,
        model=None,
        properties=IndexProperties(
            read_method='raw_market_events',
            write_method='import_market_events',
            schema_raw=raws.TypeMarketEvent.schema(),
            model_raw=raws.TypeMarketEvent,
            schema_source=sources.SourceMarketEvent.schema(),
            model_source=sources.SourceMarketEvent,
        ),
    ),
    IndexName.location: IndexOptions(
        name=IndexName.location,
        model=None,
        properties=IndexProperties(
            read_method='raw_location',
            write_method='import_locations',
            schema_raw=raws.TypeLocation.schema(),
            model_raw=raws.TypeLocation,
            schema_source=sources.SourceLocation.schema(),
            model_source=sources.SourceLocation,
        ),
    ),
    IndexName.layout: IndexOptions(
        name=IndexName.layout,
        model=None,
        properties=IndexProperties(
            read_method='raw_layouts',
            write_method='import_layouts',
            schema_raw=raws.TypeLayout.schema(),
            model_raw=raws.TypeLayout,
            schema_source=sources.SourceLayout.schema(),
            model_source=sources.SourceLayout,
        ),
    ),
    IndexName.view_category: IndexOptions(
        name=IndexName.view_category,
        model=None,
        read_only=True,
        properties=IndexProperties(
            read_method='view_category',
            write_method=None,
            schema_raw=views.ViewCategory.schema(),
            model_raw=views.ViewCategory,
            schema_source=None,
            model_source=None,
        ),
    ),
    IndexName.view_event: IndexOptions(
        name=IndexName.view_event,
        model=None,
        read_only=True,
        properties=IndexProperties(
            read_method='view_event',
            write_method=None,
            schema_raw=views.ViewEvent.schema(),
            model_raw=views.ViewEvent,
            schema_source=None,
            model_source=None,
        ),
    ),
}


@dataclass(frozen=True)
class IndexState:
    """Index state."""

    index: Dict[IndexName, IndexOptions]
    version: TypeDigest

    def index_names(self) -> List[IndexName]:
        """List index names."""

        return [name for name in self.index.keys()]

    def index_models(self) -> List[Any]:
        """List models."""

        return [
            _idx.model
            for _name, _idx in self.index.items()
            if bool(_idx.model)
        ]


digest = digest_branch(languages=all_languages, state=_state_meta)


def state_index(models: Dict[IndexName, Type[BaseModel]]) -> IndexState:
    """Initialize index with models."""

    for name, model in models.items():
        _state_meta[name].model = model

    return IndexState(
        index=_state_meta,
        version=digest,
    )


TypeDomains = Union[None, List[raws.TypeDomain]]
TypeCategories = Union[None, List[raws.TypeCategory]]
TypeCharts = Union[None, List[raws.TypeChart]]
TypeTags = Union[None, List[raws.TypeTag]]
TypePlaces = Union[None, List[raws.TypePlace]]
TypePersons = Union[None, List[raws.TypePerson]]
TypeMarketEvents = Union[None, List[raws.TypeMarketEvent]]
TypeLayouts = Union[None, List[raws.TypeLayout]]

TypeViewCategory = Union[None, List[views.ViewCategory]]
TypeViewEvent = Union[None, List[views.ViewEvent]]


class Results(object):
    """Results."""

    items: List[Any]
    count: int
    total: int

    def is_empty(self) -> bool:
        """Is empty."""

        return not bool(self.items)


@dataclass(frozen=True)  # noqa
class TagResults(Results):
    """Tag results."""

    items: TypeTags
    count: int
    total: int


@dataclass(frozen=True)  # noqa
class MarketEventResults(Results):
    """Tag results."""

    items: TypeMarketEvents
    count: int
    total: int


@dataclass(frozen=True)  # noqa
class DomainResults(Results):
    """Domain results."""

    items: TypeDomains
    count: int
    total: int


@dataclass(frozen=True)  # noqa
class PlaceResults(Results):
    """Place results."""

    items: TypePlaces
    count: int
    total: int


@dataclass(frozen=True)  # noqa
class PersonResults(Results):
    """Person results."""

    items: TypePersons
    count: int
    total: int


@dataclass(frozen=True)  # noqa
class CategoryResults(Results):
    """Category results."""

    items: TypeCategories
    count: int
    total: int


@dataclass(frozen=True)  # noqa
class ChartResults(Results):
    """Chart results."""

    items: TypeCharts
    count: int
    total: int


@dataclass(frozen=True)  # noqa
class LayoutResults(Results):
    """Layout results."""

    items: TypeLayouts
    count: int
    total: int


@dataclass(frozen=True)
class ViewCategoryResults(Results):
    """Category view results."""

    items: TypeViewCategory
    count: int
    total: int


@dataclass(frozen=True)
class ViewEventResults(Results):
    """Event view results."""

    items: TypeViewEvent
    count: int
    total: int


TypeResults = {
    IndexName.category: CategoryResults,
    IndexName.chart: ChartResults,
    IndexName.domain: DomainResults,
    IndexName.tag: TagResults,
    IndexName.place: PlaceResults,
    IndexName.person: PersonResults,
    IndexName.market_event: MarketEventResults,
    IndexName.layout: LayoutResults,
    IndexName.view_category: ViewCategoryResults,
    IndexName.view_event: ViewEventResults,
}

# TypeViewEvent
@dataclass
class Search:
    """Async search."""

    messanger: Messanger

    # Internals ---------------------------------------------------------------

    def clean_params(  # noqa
        self,
        items: Union[List[Any], None],
        total: Union[int, None],
    ):
        """Clean params."""

        exists = bool(items)

        return {
            'items': list() if not exists else items,
            'count': 0 if not exists else len(items),
            'total': 0 if not exists else total,
        }

    def _read_items(self, response: Dict) -> List[Dict]:  # noqa
        """Read items from response."""
        try:
            return response['data']['results']
        except Exception as _any:
            print(f'Error read response items: {_any}')
            return list()

    def _read_count(self, response: Dict) -> int:  # noqa
        """Read count from response."""
        try:
            return int(response['data']['count'])
        except Exception as _any:
            print(f'Error read response count: {_any}')
            return 0

    def _read_total(self, response: Dict) -> int:  # noqa
        """Read total from response."""
        try:
            return int(response['data'].get('total', 0))
        except Exception as _any:
            print(f'Error read response total: {_any}')
            return 0

    def _serialize(   # noqa
        self,
        name: IndexName,
        items: List[Union[BaseModel, Any]],
    ):
        """Serialize items."""

        try:
            raw_class = _state_meta[name].properties.model_raw
            return [raw_class(**item) for item in items]
        except Exception as _any_exc:
            log.error(f'Serialize error: {_any_exc}')
            return list()

    def _get_proxy(  # noqa
        self,
        name: IndexName,
    ) -> IndexOptions:
        """Proxy by name."""

        return _state_meta[name]

    async def _lookup(
        self,
        name: IndexName,
        expression: Expression = None,
        sorting: Dict[str, int] = None,
        lang: str = lang_base,
        limit: int = 25,
        page: int = 1,
    ) -> Results:

        proxy = self._get_proxy(name)

        result = await self.messanger.query(
            method=proxy.properties.read_method,
            expression=expression.eval() if expression else None,
            sorting=sorting,
            lang=lang,
            limit=limit,
            page=page,
        )

        if result:
            total = self._read_total(result)
            items = self._serialize(
                name=name,
                items=self._read_items(result),
            )
        else:
            total, items = 0, list()

        return TypeResults[name](  # noqa
            **self.clean_params(items=items, total=total),
        )

    # Exports -----------------------------------------------------------------

    async def market_events(
        self,
        expression: Expression = None,
        sorting: Dict[str, int] = None,
        lang: str = lang_base,
        limit: int = 25,
        page: int = 1,
    ) -> Union[MarketEventResults, Any]:
        """Wrap query."""

        return await self._lookup(
            name=IndexName.market_event,
            expression=expression,
            sorting=sorting,
            lang=lang,
            limit=limit,
            page=page,
        )

    async def tags(
        self,
        expression: Expression = None,
        sorting: Dict[str, int] = None,
        lang: str = lang_base,
        limit: int = 25,
        page: int = 1,
    ) -> Union[TagResults, Any]:
        """Wrap query."""

        return await self._lookup(
            name=IndexName.tag,
            expression=expression,
            sorting=sorting,
            lang=lang,
            limit=limit,
            page=page,
        )

    async def domains(
        self,
        expression: Expression = None,
        sorting: Dict[str, int] = None,
        lang: str = lang_base,
        limit: int = 25,
        page: int = 1,
    ) -> Union[DomainResults, Any]:
        """Wrap query."""

        return await self._lookup(
            name=IndexName.domain,
            expression=expression,
            sorting=sorting,
            lang=lang,
            limit=limit,
            page=page,
        )

    async def places(
        self,
        expression: Expression = None,
        sorting: Dict[str, int] = None,
        lang: str = lang_base,
        limit: int = 25,
        page: int = 1,
    ) -> Union[PlaceResults, Any]:
        """Wrap query."""

        return await self._lookup(
            name=IndexName.place,
            expression=expression,
            sorting=sorting,
            lang=lang,
            limit=limit,
            page=page,
        )

    async def persons(
        self,
        expression: Expression = None,
        sorting: Dict[str, int] = None,
        lang: str = lang_base,
        limit: int = 25,
        page: int = 1,
    ) -> Union[PersonResults, Any]:
        """Wrap query."""

        return await self._lookup(
            name=IndexName.person,
            expression=expression,
            sorting=sorting,
            lang=lang,
            limit=limit,
            page=page,
        )

    async def categories(
        self,
        expression: Expression = None,
        sorting: Dict[str, int] = None,
        lang: str = lang_base,
        limit: int = 25,
        page: int = 1,
    ) -> Union[CategoryResults, Any]:
        """Wrap query."""

        return await self._lookup(
            name=IndexName.category,
            expression=expression,
            sorting=sorting,
            lang=lang,
            limit=limit,
            page=page,
        )

    async def charts(
        self,
        expression: Expression = None,
        sorting: Dict[str, int] = None,
        lang: str = lang_base,
        limit: int = 25,
        page: int = 1,
    ) -> Union[ChartResults, Any]:
        """Wrap query."""

        return await self._lookup(
            name=IndexName.chart,
            expression=expression,
            sorting=sorting,
            lang=lang,
            limit=limit,
            page=page,
        )

    async def layouts(
        self,
        expression: Expression = None,
        sorting: Dict[str, int] = None,
        lang: str = lang_base,
        limit: int = 25,
        page: int = 1,
    ) -> Union[LayoutResults, Any]:
        """Wrap query."""

        return await self._lookup(
            name=IndexName.layout,
            expression=expression,
            sorting=sorting,
            lang=lang,
            limit=limit,
            page=page,
        )

    async def view_category(
        self,
        expression: Expression = None,
        sorting: Dict[str, int] = None,
        lang: str = lang_base,
        limit: int = 25,
        page: int = 1,
    ) -> Union[ViewCategoryResults, Any]:
        """Wrap query."""

        return await self._lookup(
            name=IndexName.view_category,
            expression=expression,
            sorting=sorting,
            lang=lang,
            limit=limit,
            page=page,
        )

    async def view_event(
        self,
        expression: Expression = None,
        sorting: Dict[str, int] = None,
        lang: str = lang_base,
        limit: int = 25,
        page: int = 1,
    ) -> Union[ViewEventResults, Any]:
        """Wrap query."""

        return await self._lookup(
            name=IndexName.view_event,
            expression=expression,
            sorting=sorting,
            lang=lang,
            limit=limit,
            page=page,
        )


def match_query(
    expressions: List[TypeExpression],
) -> Union[TypeExpression, None]:
    """Match query expression."""

    expr_arr = [_e for _e in expressions if not _e.skip()]

    if not bool(expr_arr) or len(expr_arr) == 0:
        return None
    elif len(expr_arr) == 1:
        return expr_arr[0]
    else:
        return And(expr_arr)


class ViewType(IntEnum):
    """Lookup type view."""

    single = 10
    listing = 20
    paginated = 30


@dataclass(frozen=True)
class Query:
    """Query context."""

    view: ViewType

    limit: int = 25
    page: int = 1
    lang: str = lang_base

    expression: Optional[TypeExpression] = None
    sorting: Optional[Dict[str, int]] = None

    def log_query(self) -> Dict:
        """Query for log extra."""

        expression = self.expression.eval() if self.expression else None
        return {
            'expression': expression,
            'sorting': self.sorting,
            'limit': self.limit,
            'page': self.page,
            'lang': self.lang,
        }

    def create_message(
        self,
        token: str,
        version: str,
        method: str,
    ) -> Dict:
        """Create json message."""

        expression = self.expression.eval() if self.expression else None

        return {
            'jsonrpc': '2.0',
            'id': 0,
            'method': method,
            'params': {
                'query': {
                    'version': version,
                    'token': token,
                    'expression': expression,
                    'sorting': self.sorting,
                    'limit': self.limit,
                    'page': self.page,
                    'lang': self.lang,
                },
            },
        }


Q = Query


class LookupProjection:
    """Lookup projection."""

    name: IndexName

    def __init__(self, search: Search, extra_data: Dict = None):
        """Init lookup."""

        self.search = search
        self.extra_data = extra_data

        assert self.name in IndexName, 'Unknown index name'
        self.index: IndexOptions = _state_meta[self.name]

    @classmethod
    def fallback_paginated(
        cls,
        page: int = 1,
        limit: int = 25,
    ) -> Dict: # noqa
        """Fallback paginated."""

        return {
            'data': {
                'last_page': 0,
                'page': page,
                'limit': limit,
                'total': 0,
                'count': 0,
                'results': [],
            }
        }

    async def prepare_context(  # noqa
        self,
        query: Query,  # noqa
        items: Union[List[Dict], None],  # noqa
        total: int,  # noqa
    ) -> Dict:
        """Prepare context."""

        return dict()

    async def _execute(
        self,
        query: Query,
    ) -> Tuple[Union[List[Dict], None], int]:
        """Execute query."""

        expression = query.expression.eval() if query.expression else None

        reply = await self.search.messanger.query(
            method=self.index.properties.read_method,
            expression=expression,
            sorting=query.sorting,
            lang=query.lang,
            page=query.page,
            limit=query.limit,
        )

        if not reply:
            return None, 0

        try:
            items = reply['data']['results']
            total = reply['data'].get('total', len(items))
            return items, total
        except Exception as _any_parse_exc:
            log.error(f'On parse results: {_any_parse_exc}')
            return None, 0

    def _prepare(  # noqa
        self,
        query: Union[Query, None],
    ) -> Query:  # noqa
        """Default query."""

        if isinstance(query, Query):
            return query

        return Query(
            limit=1,
            page=1,
            lang=lang_base,
            expression=None,
            sorting=None,
            view=ViewType.single,
        )

    async def query(
        self,
        query: Query = None,
    ) -> Union[Dict, List[Dict], None]:
        """Execute query lookup."""

        items, total = await self._execute(query=self._prepare(query))

        if not items:
            return None

        try:
            context = await self.prepare_context(
                query=query,
                items=items,
                total=total,
            )
        except Exception as _context_exc:  # noqa
            log.error(f'On prepare context: {_context_exc}')
            context = dict()

        try:
            return await self._render_response(
                query=query,
                context=context,
                items=items,
                total=total,
            )
        except Exception as _render_response_exc:
            log.error(f'On render response: {_render_response_exc}')

    async def _render_response(
        self,
        query: Query,
        items: List[Dict],
        total: int,
        context: Dict = None,
    ) -> Union[Dict, List[Dict], None]:
        """."""

        response_by_type = {
            ViewType.single: self._view_single,
            ViewType.listing: self._view_listing,
            ViewType.paginated: self._view_paginated,
        }

        return await response_by_type[query.view](  # noqa
            query=query,
            context=context,
            items=items,
            total=total,
        )

    @classmethod
    def render(  # noqa
        cls,
        item: Dict,
        query: Query,
        context: Dict = None,
    ) -> Union[BaseModel, None]:
        """Render item."""

        raise NotImplementedError()

    async def _view_single(
        self,
        items: List[Dict],
        total: int,  # noqa
        query: Query,
        context: Dict = None,
    ) -> Union[Dict, None]:
        """Single doc view."""

        if isinstance(items, list) and len(items) > 0:
            item = items.pop()
            try:
                return self.render(
                    item=item,
                    query=query,
                    context=context,
                ).dict()
            except Exception as _list_result_exc:
                log.error(f'On single result: {_list_result_exc}')
                return None
        return None

    async def _view_listing(
        self,
        query: Query,
        items: List[Dict],
        total: int,  # noqa
        context: Dict = None,
    ) -> Union[List[Dict], None]:
        """List doc view."""

        if items and isinstance(items, list) and len(items) > 0:
            try:
                return [
                    self.render(item=item, query=query, context=context).dict()
                    for item in items
                ]
            except Exception as _list_result_exc:
                log.error(f'On list results: {_list_result_exc}')
                return None
        return None

    async def _view_paginated(
        self,
        query: Query,
        items: List[Dict],
        total: int,
        context: Dict = None,
    ) -> Dict:
        """Paginated doc view."""

        fallback = {
            'total': 0,
            'count': 0,
            'limit': query.limit,
            'page': query.page,
            'last_page': 1,
            'results': list(),
        }

        if isinstance(items, list) and len(items) > 0:
            _total = total or 0
            _response, _count = dict(fallback), len(items)

            try:
                _response.update({
                    'count': _count,
                    'total': _total,
                    'last_page': ceil(_total / query.limit) or 1,
                    'results': [
                        self.render(
                            item=item,
                            query=query,
                            context=context,
                        ).dict() for item in items
                    ],
                })
            except Exception as _paginate_result_exc:
                log.error(f'On paginate results: {_paginate_result_exc}')
                return {'data': fallback}
            return {'data': _response}
        return {'data': fallback}
