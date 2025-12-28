from fastapi import FastAPI

from .database.dbConfig import Base,engine
from .database.models.diesel_model import DieselReceived,DieselIssued
from .router import received_router,issued_router

# diesel_model.Base.metadata.create_all(bind=engine)
# audit_model.Base.metadata.create_all(bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(received_router.router,prefix='/api')
app.include_router(issued_router.router,prefix='/api')
@app.get("/")
async def root():
    return {"Hello": "World"}



#
# @app.post("/zoho/webhook")
# async def zoho_webhook(request: Request):
#     data = await request.json()
#     print("Webhook received ==> \n",data)
#     return {"status": "ok"}