from fastapi import FastAPI
import uvicorn
from api.interface.controllers.controller import router
from containers import Container

app = FastAPI()
app.container = Container()
app.include_router(router=router)


@app.get("/")
def hello():
    return {"Hello": "FastAPI"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)