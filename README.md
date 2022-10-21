# B_2216's API server

## How to run server

1. Set the sqlite database file path to `DATABASE_URI` variable in `.env` file. For example, `DATABASE_URI="sqlite:///./app.db"`.
2. Run the following command:

```sh
pip install -r requirements.txt
uvicorn uvicorn src.main:app --reload
```
