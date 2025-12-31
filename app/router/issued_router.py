from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controller.diesel_controller import create_diesel_issued_entry, get_diesel_issued_entry, \
    get_all_diesel_issued_entries, delete_diesel_issued_entry
from app.database.dbConfig import get_db
from app.schemas.api_schema import APIResponse
from app.schemas.diesel_schema import RequestSchema_DieselIssued_Create, ResponseSchema_DieselIssued_Create

router = APIRouter(prefix="/issued", tags=["Assets Issued"])


@router.post("/diesel", response_model=APIResponse)
async def add_diesel_entry(data: RequestSchema_DieselIssued_Create, db: Session = Depends(get_db)):
    returned_data = await create_diesel_issued_entry(db, data)
    response_data = ResponseSchema_DieselIssued_Create.model_validate(returned_data)
    return APIResponse(
        message="Diesel Issued data saved to database",
        status="success",
        data=response_data
    )


@router.get("/diesel/{record_id}", response_model=APIResponse)
async def get_diesel_entry(record_id: str, db: Session = Depends(get_db)):
    returned_data = await get_diesel_issued_entry(db, record_id)
    if returned_data is None:
        raise HTTPException(404, detail=f"Diesel Issued data for id {record_id} not found")
    response_data = ResponseSchema_DieselIssued_Create.model_validate(returned_data)
    return APIResponse(
        message="Data found",
        status="success",
        data=response_data
    )


@router.get("/diesel", response_model=APIResponse)
async def get_all_diesel_entries(db: Session = Depends(get_db)):
    returned_data = await get_all_diesel_issued_entries(db)
    if returned_data is None:
        raise HTTPException(404, "Data not found")

    response_data = [ResponseSchema_DieselIssued_Create.model_validate(item) for item in returned_data]

    return APIResponse(
        message="Data found",
        status="success",
        data=response_data
    )

@router.delete("/diesel/{recordId}", response_model=APIResponse)
async def delete_diesel_entry(recordId: str, db: Session = Depends(get_db)):
    returned_data = await delete_diesel_issued_entry(recordId, db)
    return APIResponse(
        message=f"Data with the id {recordId} was deleted",
        status="success",
        data=returned_data
    )
