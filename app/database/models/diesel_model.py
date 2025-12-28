from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
from app.database.dbConfig import Base
from sqlalchemy.orm import Session


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

def insertInto_DieselReceivedTable(db: Session, entry_data: DieselReceived):
    try:
        db.add(entry_data)
        db.commit()
        db.refresh(entry_data)
    except SQLAlchemyError as e:
        print("ERROR IN insertInto_DieselReceivedTable ==>",e)
        db.rollback()
        raise

def insertInto_DieselIssuedTable(db:Session, entry_data: DieselIssued):
    try:
        db.add(entry_data)
        db.commit()
        db.refresh(entry_data)
    except SQLAlchemyError as e:
        print("ERROR IN insertInto_DieselIssuedTable ==>",e)
        db.rollback()
        raise