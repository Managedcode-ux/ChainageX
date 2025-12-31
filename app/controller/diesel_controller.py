from sqlalchemy import Sequence
from sqlalchemy.orm import Session

from app.app_config.logging_config import get_logger
from app.database.models.diesel_model import DieselReceived, DieselIssued, insertInto_DieselReceivedTable, \
    insertInto_DieselIssuedTable, fetchFrom_DieselReceived, fetchAllFrom_DieselReceived, fetchFrom_DieselIssued, \
    fetchAllFrom_DieselIssued
from app.exceptions.external import ExternalServiceError
from app.schemas.diesel_schema import RequestSchema_DieselIssued_Create
from app.schemas.diesel_schema import RequestSchema_DieselReceived_Create
from app.services.tally_service import tallyVoucher_DieselReceived, tallyVoucher_DieselIssued

logger = get_logger()


# Note - Controllers related to diesel received
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


async def get_diesel_received_entry(db: Session, recordIdid: str) -> DieselReceived | None:
    fetched_record = fetchFrom_DieselReceived(db, recordIdid)
    return fetched_record


async def get_all_diesel_received_entries(db: Session) -> Sequence[DieselReceived] | None:
    fetched_records = fetchAllFrom_DieselReceived(db)
    return fetched_records


# Note - Controllers related to diesel issued
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


async def get_diesel_issued_entry(db: Session, recordId: str) -> DieselIssued | None:
    fetched_record = fetchFrom_DieselIssued(db, recordId)
    return fetched_record


async def get_all_diesel_issued_entries(db: Session) -> Sequence[DieselIssued] | None:
    fetched_records = fetchAllFrom_DieselIssued(db)
    return fetched_records
