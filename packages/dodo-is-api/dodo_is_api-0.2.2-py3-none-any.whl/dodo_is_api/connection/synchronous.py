import datetime
from typing import Iterable, Generator
from uuid import UUID

import httpx

from .base import BaseConnection, concatenate_uuids, raise_for_status

__all__ = ('DodoISAPIConnection',)


class DodoISAPIConnection(BaseConnection):
    __slots__ = ('__http_client',)

    def __init__(self, *, http_client: httpx.Client):
        self.__http_client = http_client

    def iter_late_delivery_vouchers(
            self,
            *,
            from_date: datetime.datetime,
            to_date: datetime.datetime,
            units: Iterable[UUID],
            skip: int = 0,
            take: int = 1000,
    ) -> Generator[list[dict], None, None]:
        url = '/delivery/vouchers'
        request_query_params = {
            'from': from_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'to': to_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'units': concatenate_uuids(units),
            'skip': skip,
            'take': take,
        }

        while True:
            response = self.__http_client.get(url, params=request_query_params)
            raise_for_status(response)

            response_data = response.json()
            yield response_data['vouchers']
            if response_data['isEndOfListReached']:
                break
            request_query_params['skip'] += take
