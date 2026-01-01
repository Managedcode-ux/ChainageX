from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controller.diesel_controller import create_diesel_received_entry, get_diesel_received_entry, \
    get_all_diesel_received_entries, delete_diesel_received_entry, update_diesel_received_entry
from app.database.dbConfig import get_db
from app.schemas.api_schema import APIResponse
from app.schemas.diesel_schema import RequestSchema_DieselReceived_Create, RequestSchema_DieselReceived_Update, \
    ResponseSchema_DieselReceived_Create

router = APIRouter(prefix="/received", tags=["Assets Received"])


@router.post("/diesel", response_model=APIResponse)
async def add_diesel_entry(data: RequestSchema_DieselReceived_Create, db: Session = Depends(get_db)):
    returned_data = await create_diesel_received_entry(db, data)
    response_data = ResponseSchema_DieselReceived_Create.model_validate(returned_data)
    return APIResponse(
        message="Diesel Received data saved to database",
        status="success",
        data=response_data
    )


@router.get("/diesel/{recordId}", response_model=APIResponse)
async def get_diesel_entry(recordId: str, db: Session = Depends(get_db)):
    returned_data = await get_diesel_received_entry(db, recordId)
    if returned_data is None:
        raise HTTPException(404, "Data not found")
    response_data = ResponseSchema_DieselReceived_Create.model_validate(returned_data)
    return APIResponse(
        message="Data found",
        status="success",
        data=response_data
    )


@router.get("/diesel", response_model=APIResponse)
async def get_all_diesel_entry(db: Session = Depends(get_db)):
    returned_data = await get_all_diesel_received_entries(db)

    if returned_data is None:
        raise HTTPException(404, "Data not found")

    response_data = [ResponseSchema_DieselReceived_Create.model_validate(item) for item in returned_data]
    return APIResponse(
        message="Data found",
        status="success",
        data=response_data
    )


@router.delete("/diesel/{recordId}", response_model=APIResponse)
async def delete_diesel_entry(recordId: str, db: Session = Depends(get_db)):
    returned_data = await delete_diesel_received_entry(recordId, db)
    return APIResponse(
        message=f"Data with the id {recordId} was deleted",
        status="success",
        data=returned_data
    )


@router.patch("/diesel/{recordId}", response_model=APIResponse)
async def update_diesel_entry(data: RequestSchema_DieselReceived_Update, recordId: str, db: Session = Depends(get_db)):
    updated_data = await update_diesel_received_entry(recordId, db,data)
    response_data = ResponseSchema_DieselReceived_Create.model_validate(updated_data)
    return APIResponse(
        message=f"Data with the id {recordId} was updated",
        status="success",
        data=response_data
    )
