from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database.dbConfig import get_db
from app.schemas.diesel_schema import DieselIssuedCreateSchema
from app.controller.diesel_controller import create_diesel_issued_entry

router = APIRouter(prefix="/issued", tags=["Assets Issued"])

@router.post("/diesel")
async def add_diesel_entry(data:DieselIssuedCreateSchema,db:Session=Depends(get_db)):
    try:
        return await create_diesel_issued_entry(db,data)
    except SQLAlchemyError as e:
        raise HTTPException(500, "Database error")