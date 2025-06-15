import streamlit as st
import requests
import os
from dotenv import load_dotenv

# === Constants ===
ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", ".env"))

# === Helper: Read key from specific .env ===
def get_env_key(key_name: str = "GROQ_API_KEY", env_path: str = ENV_PATH) -> str | None:
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.strip().startswith(f"{key_name}="):
                    return line.strip().split("=", 1)[1]
    return None

# === Helper: Write/replace key in specific .env ===
def write_env_key(key_name: str, key_value: str, env_path: str = ENV_PATH):
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()
    with open(env_path, "w") as f:
        for line in lines:
            if not line.strip().startswith(f"{key_name}="):
                f.write(line)
        f.write(f"{key_name}={key_value}\n")

# === Helper: Validate API Key via Dry Run ===
def validate_groq_api_key(api_key: str) -> bool:
    try:
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "user", "content": "SELECT * FROM customers;"}
            ],
            "max_tokens": 10,
            "temperature": 0
        }
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=data, headers=headers, timeout=5)
        return response.status_code == 200
    except Exception:
        return False

# === Load .env from backend folder ===
load_dotenv(ENV_PATH)

# === Check stored key ===
stored_key = (
    st.session_state.get("groq_api_key") or
    os.getenv("GROQ_API_KEY") or
    get_env_key()
)

# === Validate stored key once on startup ===
if stored_key and "valid_api_key" not in st.session_state:
    if validate_groq_api_key(stored_key):
        st.session_state["groq_api_key"] = stored_key
        st.session_state["valid_api_key"] = True
    else:
        st.session_state["valid_api_key"] = False
        st.session_state["groq_api_key"] = None

# === Sidebar ===
st.sidebar.title("🔐 Groq API Configuration")

if "changing_key" not in st.session_state:
    st.session_state["changing_key"] = not st.session_state.get("valid_api_key", False)

if st.session_state["changing_key"]:
    new_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")
    if new_key:
        with st.spinner("Validating API key..."):
            if validate_groq_api_key(new_key):
                write_env_key("GROQ_API_KEY", new_key)
                os.environ["GROQ_API_KEY"] = new_key
                st.session_state["groq_api_key"] = new_key
                st.session_state["valid_api_key"] = True
                st.session_state["changing_key"] = False
                st.sidebar.success("✅ API Key is valid and saved!")
                st.rerun()
            else:
                st.sidebar.error("❌ Invalid API key. Please try again.")
else:
    st.sidebar.success("✅ API key loaded.")
    st.sidebar.write(f"Current key: ****{st.session_state['groq_api_key'][-4:]}")
    if st.sidebar.button("🔁 Change API Key"):
        st.session_state["changing_key"] = True
        st.session_state["valid_api_key"] = False
        st.rerun()

# === Main Interface ===
if st.session_state.get("valid_api_key"):
    st.title("💬 LLM-Powered Customer Query Chatbot")
    query = st.text_input("Ask your question:", placeholder="e.g., Show all female customers from Mumbai")

    if st.button("Submit") and query:
        with st.spinner("Querying..."):
            try:
                response = requests.post("http://localhost:8000/query", json={"query": query})
                data = response.json()
                if data["success"]:
                    st.success("✅ Query executed successfully!")
                    st.code(data["query"], language="sql")
                    st.dataframe(data["result"])
                else:
                    st.error(f"❌ Error: {data['error']}")
            except Exception as e:
                st.error(f"❌ Failed to contact backend: {e}")
else:
    st.warning("⚠️ Please enter a valid Groq API key in the sidebar to use the chatbot.")
