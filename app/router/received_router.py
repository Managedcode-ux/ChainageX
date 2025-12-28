from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.diesel_schema import DieselReceivedCreateSchema
from app.controller.diesel_controller import create_diesel_received_entry
from app.database.dbConfig import get_db
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

router = APIRouter(prefix="/received", tags=["Assets Received"])


@router.post("/diesel")
async def add_diesel_entry(data: DieselReceivedCreateSchema, db: Session = Depends(get_db)):
    try:
        return await create_diesel_received_entry(db, data)
    except SQLAlchemyError as e:
        raise HTTPException(500, "Database error")
