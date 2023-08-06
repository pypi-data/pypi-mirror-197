from datetime import datetime
from uuid import UUID

import models

__all__ = (
    'map_late_delivery_voucher_dto',
)


def map_late_delivery_voucher_dto(late_delivery_voucher: dict) -> models.LateDeliveryVoucher:
    if (order_fulfilment_flag_at_local := late_delivery_voucher['orderFulfilmentFlagAtLocal']) is not None:
        order_fulfilment_flag_at_local = datetime.fromisoformat(order_fulfilment_flag_at_local)

    if (courier_staff_id := late_delivery_voucher['courierStaffId']) is not None:
        courier_staff_id = UUID(courier_staff_id)

    return models.LateDeliveryVoucher(
        order_id=UUID(late_delivery_voucher['orderId']),
        order_number=late_delivery_voucher['orderNumber'],
        order_accepted_at_local=datetime.fromisoformat(late_delivery_voucher['orderAcceptedAtLocal']),
        unit_id=UUID(late_delivery_voucher['unitId']),
        predicted_delivery_time_local=datetime.fromisoformat(late_delivery_voucher['predictedDeliveryTimeLocal']),
        order_fulfilment_flag_at_local=order_fulfilment_flag_at_local,
        delivery_deadline_local=datetime.fromisoformat(late_delivery_voucher['deliveryDeadlineLocal']),
        issuer_name=late_delivery_voucher['issuerName'],
        courier_staff_id=courier_staff_id,
    )
