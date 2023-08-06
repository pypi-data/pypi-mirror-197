"""Index query response messages."""

import json

from typing import Dict, List, Union
from logging import getLogger

from httpx import AsyncClient, codes
from pydantic import BaseModel

# from ..types import lang_base, TypeExpression, TypeSorting
from .builtins import TypeDigest
from .fn import SafeEncoder

log = getLogger(__name__)

TypeAnyResult = Union[Dict, List[Dict], None]


class SecureSchema(BaseModel):
    """Secure schema."""

    token: str


class SecureStrictSchema(BaseModel):
    """Secure strict schema."""

    token: str
    version: TypeDigest


class SecureQuerySchema(SecureStrictSchema):
    """Secure query schema."""

    page: int = 1
    limit: int = 25

    lang: str = 'ru'

    expression: Union[Dict, None] = None
    sorting: Union[Dict[str, int]] = None


class TypeStatusCommit(BaseModel):
    """Type status commit."""

    digest: str
    branch: str
    persistent: Dict[str, List[int]]


class StatusResponse(BaseModel):
    """Status response."""

    ready: bool
    version: TypeDigest
    commit: Union[TypeStatusCommit, None]
    aliases: Dict[str, str]


class Messanger:
    """Index messanger."""

    def __init__(
        self,
        url: str,
        token: str,
        version: TypeDigest,
        client: AsyncClient = None,
    ):
        """Init messanger."""

        self.url = url
        self.token = token
        self.version = version
        self.client = client if client else AsyncClient()

    async def status(self) -> Union[StatusResponse, None]:
        """Request status."""

        message = {
            'jsonrpc': '2.0',
            'id': 0,
            'method': 'status',
            'params': {'query': SecureSchema(token=self.token).dict()},
        }

        try:
            response = await self.client.post(
                url=self.url,
                data=json.dumps(message, cls=SafeEncoder),  # noqa
            )
        except Exception as _request_exc:  # noqa
            log.error(f'On status request: {_request_exc}')
            return

        try:
            if response.status_code == codes.OK:
                body = response.json()
                result = body['result']
                return StatusResponse(
                    ready=result.get('ready'),
                    version=result.get('version'),
                    commit=result.get('commit'),
                    aliases={},
                )
        except Exception as _request_exc:
            log.error(f'Invalid status request: {_request_exc}')

    async def query(
        self,
        method: str,
        expression: Dict = None,
        sorting: Dict[str, int] = None,
        lang: str = 'ru',
        page: int = 1,
        limit: int = 25,
    ) -> TypeAnyResult:
        """Request status."""

        message = {
            'jsonrpc': '2.0',
            'id': 0,
            'method': method,
            'params': {
                'query': SecureQuerySchema(
                    version=self.version,
                    token=self.token,
                    page=page,
                    limit=limit,
                    lang=lang,
                    sorting=sorting,
                    expression=expression,
                ).dict(),
            },
        }

        try:
            response = await self.client.post(
                url=self.url,
                data=json.dumps(message, cls=SafeEncoder),  # noqa
            )
        except Exception as _request_exc:  # noqa
            log.error(f'On status request: {_request_exc}')
            return

        try:
            if response.status_code == codes.OK:
                body = response.json()
                return body.get('result', None)
        except Exception as _parse_exc:  # noqa
            log.error(f'Invalid status request: {_parse_exc}')
            return
