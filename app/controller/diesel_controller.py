from sqlalchemy.orm import Session

from app.database.models.diesel_model import DieselReceived, DieselIssued, insertInto_DieselReceivedTable, \
    insertInto_DieselIssuedTable
from app.exceptions.external import ExternalServiceError
from app.schemas.diesel_schema import RequestSchema_DieselReceived_Create
from app.services.tally_service import tallyVoucher_DieselReceived, tallyVoucher_DieselIssued
from app.schemas.diesel_schema import RequestSchema_DieselIssued_Create
from app.app_config.logging_config import get_logger

logger = get_logger()

async def create_diesel_received_entry(db: Session, payload: RequestSchema_DieselReceived_Create) -> DieselReceived:
    entry_data = DieselReceived(
        invoice_id=payload.purchase_invoice,
        entry_by=payload.entry_by,
        received_date_and_time=payload.received_date_time,
        price_per_unit=payload.price_per_liter,
        quantity=payload.quantity_liters,
        project_name=payload.project_name,
        total_price=payload.total_price,
    )

    insertInto_DieselReceivedTable(db, entry_data)
    try:
        tallyVoucher_DieselReceived(payload)
    except ExternalServiceError as e:
        logger.warning(
            "Tally failed but DB succeeded | invoice=%s | reason=%s",
            payload.purchase_invoice,
            e,
        )
    return entry_data


async def create_diesel_issued_entry(db: Session, payload: RequestSchema_DieselIssued_Create) -> DieselIssued:
    entry_data = DieselIssued(
        project_name=payload.project_name,
        issued_to=payload.issued_to,
        issued_by=payload.issued_by,
        quantity=payload.quantity,
        issue_date_and_time=payload.issue_date_time,
        price_per_unit=payload.price_per_liter,
        total_price=payload.total_price,
    )

    insertInto_DieselIssuedTable(db, entry_data)
    try:
        tallyVoucher_DieselIssued(payload)
    except ExternalServiceError as e:
        logger.warning(
            "Tally failed but DB succeeded | reason=%s",
            e,
        )
    return entry_data
