from datetime import datetime, timezone
from typing import Sequence

from sqlalchemy import Column, Integer, String, DateTime, Float, select, update
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.orm import Session

from app.app_config.logging_config import get_logger
from app.database.dbConfig import Base
from app.schemas.diesel_schema import ResponseSchema_DieselReceived_Create, ResponseSchema_DieselIssued_Create, \
    RequestSchema_DieselReceived_Update

logger = get_logger()


class DieselReceived(Base):
    __tablename__ = 'diesel_received'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    invoice_id = Column(String, nullable=False)
    entry_by = Column(String, nullable=False)
    received_date_and_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    price_per_unit = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    project_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return (
            f"<DieselReceived "
            f"id={self.id}, "
            f"invoice_id='{self.invoice_id}', "
            f"project_name='{self.project_name}', "
            f"quantity={self.quantity}, "
            f"price_per_unit={self.price_per_unit}, "
            f"received_date_and_time={self.received_date_and_time}, "
            f"total_price={self.total_price}, "
            f"entry_by='{self.entry_by}'>"
        )


class DieselIssued(Base):
    __tablename__ = 'diesel_issued'
    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, nullable=False)
    issued_to = Column(String, nullable=False)
    issued_by = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    issue_date_and_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    price_per_unit = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<DieselIssued "
            f"id={self.id}, "
            f"project_name='{self.project_name}', "
            f"quantity={self.quantity}, "
            f"issued_to={self.issued_to}, "
            f"issued_by={self.issued_by}, "
            f"price_per_unit={self.price_per_unit},"
            f"total_price={self.total_price}, "
            f"issue_date_and_time='{self.issue_date_and_time}'>"
        )


# Note -  Database operations related to DieselReceived table
def insertInto_DieselReceivedTable(db: Session, entry_data: DieselReceived):
    try:
        db.add(entry_data)
        db.commit()
        db.refresh(entry_data)
    except SQLAlchemyError as e:
        print("ERROR IN insertInto_DieselReceivedTable ==>", e)
        db.rollback()
        raise


def fetchFrom_DieselReceived(db: Session, recordId: str) -> DieselReceived | None:
    query = select(DieselReceived).where(DieselReceived.id == int(recordId))
    record = db.execute(query).scalar_one_or_none()
    return record


def fetchAllFrom_DieselReceived(db: Session) -> Sequence[DieselReceived] | None:
    query = select(DieselReceived)
    records = db.execute(query).scalars().all()
    if not records:
        return None
    return records


def deleteFrom_dieselReceived(recordId: str, db: Session) -> ResponseSchema_DieselReceived_Create:
    try:
        query = select(DieselReceived).where(DieselReceived.id == int(recordId))
        record = db.execute(query).scalar_one()
        data_copy = ResponseSchema_DieselReceived_Create.model_validate(record)
        db.delete(record)
        db.commit()
        return data_copy
    except NoResultFound:
        raise
    except SQLAlchemyError as e:
        logger.exception(
            "DB error during deleting data from DieselReceived table | id=%s",
            recordId,
        )
        db.rollback()
        raise


def updateTo_dieselReceived(recordId: str, db: Session, data: RequestSchema_DieselReceived_Update) -> DieselReceived:
    try:
        query = select(DieselReceived).where(DieselReceived.id == int(recordId))
        record = db.execute(query).scalar_one()

        update_data = data.model_dump(exclude_unset=True)

        FIELD_MAP = {
            "project_name": "project_name",
            "purchase_invoice": "invoice_id",
            "quantity_liters": "quantity",
            "price_per_liter": "price_per_unit",
            "received_date_time": "received_date_and_time",
            "entry_by": "entry_by",
        }

        for field,value in update_data.items():
            setattr(record, FIELD_MAP[field],value)

        record.total_price = round(
            record.quantity * record.price_per_unit, 2
        )
        db.commit()
        db.refresh(record)
        return record
    except NoResultFound:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(
            "DB error during updating data in DieselReceived table | id=%s",
            recordId,
        )
        raise


# Note -  Database operations related to DieselReceived table
def insertInto_DieselIssuedTable(db: Session, entry_data: DieselIssued):
    try:
        db.add(entry_data)
        db.commit()
        db.refresh(entry_data)
    except SQLAlchemyError as e:
        print("ERROR IN insertInto_DieselIssuedTable ==>", e)
        db.rollback()
        raise


def fetchFrom_DieselIssued(db: Session, record_id: str) -> DieselIssued | None:
    query = select(DieselIssued).where(DieselIssued.id == int(record_id))
    record = db.execute(query).scalar_one_or_none()
    return record


def fetchAllFrom_DieselIssued(db: Session) -> Sequence[DieselIssued] | None:
    query = select(DieselIssued)
    records = db.execute(query).scalars().all()
    if not records:
        return None
    return records


def deleteFrom_dieselIssued(recordId: str, db: Session) -> ResponseSchema_DieselIssued_Create:
    try:
        query = select(DieselIssued).where(DieselIssued.id == int(recordId))
        record = db.execute(query).scalar_one()
        data_copy = ResponseSchema_DieselIssued_Create.model_validate(record)
        db.delete(record)
        db.commit()
        return data_copy
    except NoResultFound:
        raise
    except SQLAlchemyError as e:
        logger.exception(
            "DB error during deleting data from DieselIssued table | id=%s",
            recordId,
        )
        db.rollback()
        raise
