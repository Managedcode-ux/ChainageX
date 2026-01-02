from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.app_config.logging_config import get_logger
from app.database.models.diesel_model import DieselReceived, DieselIssued, insertInto_DieselReceivedTable, \
    insertInto_DieselIssuedTable, fetchFrom_DieselReceived, fetchAllFrom_DieselReceived, fetchFrom_DieselIssued, \
    fetchAllFrom_DieselIssued, deleteFrom_dieselReceived, deleteFrom_dieselIssued, updateTo_dieselReceived
from app.exceptions.external import ExternalServiceError
from app.schemas.diesel_schema import RequestSchema_DieselIssued_Create, ResponseSchema_DieselReceived_Create, \
    RequestSchema_DieselReceived_Update
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


async def get_diesel_received_entry(db: Session, recordId: str) -> DieselReceived | None:
    fetched_record = fetchFrom_DieselReceived(db, recordId)
    return fetched_record


async def get_all_diesel_received_entries(db: Session) -> list[DieselReceived] | None:
    fetched_records = fetchAllFrom_DieselReceived(db)
    if fetched_records is None:
        return None
    return list(fetched_records)


async def delete_diesel_received_entry(recordId: str, db: Session) -> ResponseSchema_DieselReceived_Create:
    try:
        deleted_record = deleteFrom_dieselReceived(recordId, db)
        return deleted_record
    except NoResultFound:
        raise HTTPException(404, "Data not found")


async def update_diesel_received_entry(recordId: str, db: Session, data:RequestSchema_DieselReceived_Update) -> DieselReceived:
    try:
        updated_record = updateTo_dieselReceived(recordId, db, data)
        return updated_record
    except NoResultFound:
        raise HTTPException(404, "Data not found")


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


async def get_all_diesel_issued_entries(db: Session) -> list[DieselIssued] | None:
    fetched_records = fetchAllFrom_DieselIssued(db)
    if fetched_records is None:
        return None
    return list(fetched_records)


async def delete_diesel_issued_entry(recordId: str, db: Session):
    try:
        deleted_record = deleteFrom_dieselIssued(recordId, db)
        return deleted_record
    except NoResultFound:
        raise HTTPException(404, "Data not found")
