from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_root():
    return {"message": "hello, world!"}

@app.post("/")
def post_root():
    return {"message": "post success!"}

