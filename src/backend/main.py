from fastapi import FastAPI, Request
from backend.db import engine
from backend.groq_api import query_llm
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.post("/query")
async def handle_query(request: Request):
    data = await request.json()
    user_query = data.get("query")

    try:
        sql_query = query_llm(user_query)
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            records = [dict(row._mapping) for row in result]
        return {"success": True, "query": sql_query, "result": records}
    except Exception as e:
        return {"success": False, "error": str(e)}
