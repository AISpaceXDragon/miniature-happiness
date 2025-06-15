This repository is created for an assignment task given by "Superteams.ai"

# LLM-Powered Customer Query Chatbot with FastAPI and Streamlit

## Setup Instructions

1. Clone this repository in to a new folder on the local machine.
```bash
git clone https://github.com/AISpaceXDragon/miniature-happiness.git
```

2. Then run the following command
```bash
cd miniature-happiness
```

3. Install requirements by running the following command.
```bash
pip install -r requirements.txt
```

4. Then run the following command.
```bash
cd src
```

5. Run the following command for inserting random data into the database.(may not be needed as I have uploaded the customers.db file with random data inserted.)
```bash
python backend/seed_data.py
```

6. Run the following command to start the FastAPI server.
```bash
uvicorn backend.main:app --reload
```

7. After running the command given above open a new terminal window and ensure that you are in the folder where you have cloned the repo and you are inside the "src" folder of the repo. Then run the following command to launch the frontend built using Streamlit library.
```bash
python frontend/streamlit_app.py
```

8. Then enter the API key and ask a query of your choice. You will get answers based on the data in the database/table.
## Example Query
```
Show all female customers from Mumbai
```

