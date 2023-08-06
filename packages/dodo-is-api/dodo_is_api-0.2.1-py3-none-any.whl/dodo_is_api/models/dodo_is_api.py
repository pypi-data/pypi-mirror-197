import datetime
from dataclasses import dataclass
from uuid import UUID

__all__ = (
    'LateDeliveryVoucher',
)


@dataclass(frozen=True, slots=True)
class LateDeliveryVoucher:
    order_id: UUID
    order_number: str
    order_accepted_at_local: datetime.datetime
    unit_id: UUID
    predicted_delivery_time_local: datetime.datetime
    order_fulfilment_flag_at_local: datetime.datetime | None
    delivery_deadline_local: datetime.datetime
    issuer_name: str | None
    courier_staff_id: UUID | None
