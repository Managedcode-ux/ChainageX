from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Optional
from datetime import datetime, timezone


class RequestSchema_DieselReceived_Create(BaseModel):
    project_name: str = Field(..., min_length=1)
    purchase_invoice: str = Field(..., min_length=1)
    quantity_liters: float = Field(..., gt=0)
    price_per_liter: float = Field(..., gt=0)
    received_date_time: datetime
    entry_by: str

    @field_validator("quantity_liters", mode="before")
    @classmethod
    def parse_quantity_liters(cls, v):
        return float(v)

    @field_validator("price_per_liter", mode="before")
    @classmethod
    def parse_price(cls, v):
        return float(v)

    # converting string time into timezone type
    @field_validator("received_date_time", mode="before")
    @classmethod
    def parse_received_date_time(cls, value):
        if isinstance(value, datetime):
            return value.astimezone(timezone.utc)

        try:
            parsed = datetime.strptime(value, "%d-%b-%Y %I:%M %p")
            return parsed.replace(tzinfo=timezone.utc)
        except Exception:
            raise ValueError(
                "received_date_time must be in format 'DD-MMM-YYYY HH:MM AM/PM'"
            )

    # adding a new field total_price
    @computed_field
    @property
    def total_price(self) -> float:
        """
        Total price = total_quantity * price_per_liter
        """
        return round(self.quantity_liters * self.price_per_liter, 2)

    class Config:
        from_attributes = True

class ResponseSchema_DieselReceived_Create(BaseModel):
    id: int
    invoice_id: str
    entry_by: str
    received_date_and_time: datetime
    price_per_unit: float
    total_price: float
    quantity: float
    project_name: str
    created_at: datetime

    class Config:
        from_attributes = True

class RequestSchema_DieselIssued_Create(BaseModel):
    project_name: str = Field(..., min_length=1)
    issued_to: str = Field(..., min_length=1)
    issued_by: str = Field(..., min_length=1)
    quantity: float = Field(..., gt=0)
    issue_date_time: datetime
    price_per_liter: float = Field(..., gt=0)

    @field_validator("price_per_liter", mode="before")
    @classmethod
    def parse_price(cls, v):
        return float(v)

    @field_validator("quantity", mode="before")
    @classmethod
    def parse_quantity(cls, v):
        return float(v)

    @field_validator("issue_date_time", mode="before")
    @classmethod
    def parse_received_date_time(cls, value):
        if isinstance(value, datetime):
            return value.astimezone(timezone.utc)

        try:
            parsed = datetime.strptime(value, "%d-%b-%Y %I:%M %p")
            return parsed.replace(tzinfo=timezone.utc)
        except Exception:
            raise ValueError(
                "received_date_time must be in format 'DD-MMM-YYYY HH:MM AM/PM'"
            )

    @computed_field
    @property
    def total_price(self) -> float:
        """
        Total price = total_quantity * price_per_liter
        """
        return round(self.quantity * self.price_per_liter, 2)

    class Config:
        from_attributes = True


class ResponseSchema_DieselIssued_Create(BaseModel):
    id: int
    project_name: str
    issued_by: str
    issued_to: str
    quantity: float
    issue_date_and_time: datetime
    price_per_unit: float
    total_price: float
    created_at: datetime

    class Config:
        from_attributes = True