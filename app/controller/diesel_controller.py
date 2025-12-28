from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.util import await_only

from app.database.models.diesel_model import DieselReceived, DieselIssued, insertInto_DieselReceivedTable, \
    insertInto_DieselIssuedTable
from app.schemas.diesel_schema import DieselReceivedCreateSchema
from app.services.tally_service import tallyVoucher_DieselReceived
from app.schemas.diesel_schema import DieselIssuedCreateSchema


async def create_diesel_received_entry(db: Session, payload: DieselReceivedCreateSchema) -> DieselReceived:
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
    tallyVoucher_DieselReceived(payload)
    return entry_data


async def create_diesel_issued_entry(db: Session, payload: DieselIssuedCreateSchema) -> DieselIssued:
    entry_data = DieselIssued(
        project_name=payload.project_name,
        issued_to=payload.issued_to,
        issued_by=payload.issued_by,
        quantity=payload.quantity_liters,
        issue_date_and_time=payload.issued_date_time,
        price_per_unit=payload.price_per_liter,
        total_price=payload.total_price,
    )

    insertInto_DieselIssuedTable(db, entry_data)
    return entry_data
