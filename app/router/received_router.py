from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controller.diesel_controller import create_diesel_received_entry
from app.database.dbConfig import get_db
from app.schemas.api_schema import APIResponse
from app.schemas.diesel_schema import RequestSchema_DieselReceived_Create, ResponseSchema_DieselReceived_Create

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
