import argparse
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_root():
    return {"message": "hello, world!"}

@app.post("/")
def post_root():
    return {"message": "post success!"}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8080)

    args = parser.parse_args()

    uvicorn.run(app, host=args.host, port=args.port)