from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database.dbConfig import get_db
from app.schemas.diesel_schema import DieselIssuedCreateSchema
from app.database.models.diesel_model import insertInto_DieselIssuedTable

router = APIRouter(prefix="/issued", tags=["Assets Issued"])

@router.post("/issued")
async def add_diesel_entry(data:DieselIssuedCreateSchema,db:Session=Depends(get_db)):
    try:
        insertInto_DieselIssuedTable()
    except SQLAlchemyError as e:
        raise HTTPException(500, "Database error")