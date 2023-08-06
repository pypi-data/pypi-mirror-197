"""Digest tools."""

from typing import Any, Dict, Sequence, Union

from logging import getLogger
from json import JSONEncoder, dumps
from hashlib import sha1

from pydantic import BaseModel

from .builtins import TypeDigest, IndexOptions

_digest_len = 7

log = getLogger(__name__)


class SafeEncoder(JSONEncoder):
    """Safe type json encode."""

    def default(self, obj):
        """Fallback encode."""
        return str(obj)


def digest(text: str) -> TypeDigest:
    """Text digest."""

    hash_object = sha1(text.encode())
    return hash_object.hexdigest()[0: _digest_len]


def digest_dict(mapping: Dict) -> TypeDigest:
    """Digest mapping."""

    return digest(
        dumps(mapping, sort_keys=True, ensure_ascii=False, cls=SafeEncoder),
    )


def digest_doc(
    doc: Dict[str, Union[BaseModel, Any]],
) -> TypeDigest:
    """Digest doc."""

    return digest_dict({lang: i18n.dict() for lang, i18n in doc.items()})


def digest_gist(gist: IndexOptions) -> TypeDigest:
    """Digest gist."""

    return digest_dict({
        'name': gist.name,
        'raw': gist.properties.schema_raw,
        'src': gist.properties.schema_source,
    })


def digest_branch(
    languages: Sequence[str],
    state: Dict[str, IndexOptions],
) -> TypeDigest:
    """Digest branch."""

    index_meta = {alias: digest_gist(gist) for alias, gist in state.items()}
    return digest_dict({'languages': languages, 'meta': index_meta})


def digest_merge(merge: Dict[int, Any]) -> TypeDigest:
    """Digest merge request."""

    return digest_dict({_: merge.checksum for _, merge in merge.items()})
