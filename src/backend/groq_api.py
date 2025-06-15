import requests
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def query_llm(natural_language_query: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", 
             "content": ("You are a SQL assistant. "
                        "Only return a valid SQL query using this schema:\n\n"
                        "Table: customers (customer_id INTEGER PRIMARY KEY, name TEXT, gender TEXT, location TEXT)\n\n"
                        "The values of gender are either 'Male', 'Female', 'Transgender'. The values of gender are not 'M' or 'F' or 'TG'. The location is only a city name.\n\n"
                        "Given this user's request/natural language query, generate a single SQL query for SQLite. "
                        "Do not add explanations, do not add anything else. Do not add any prefix like 'SQL:' or any other prefix/postfix to the SQL query. Only output the SQL query, only output the SQL query:\n\n"
                        f"{natural_language_query}"
                    )}
        ]
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=data, headers=headers)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']
