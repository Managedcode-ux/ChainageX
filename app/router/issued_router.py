from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controller.diesel_controller import create_diesel_issued_entry
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
