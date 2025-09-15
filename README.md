### AI Flight Agent API Documentation

This project provides a smart AI-powered flight agent with capabilities to **book**, **cancel**, and **re-schedule** flights. It's built using a Django backend with the **Google Gemini** API for AI functionalities and a PostgreSQL database for data storage.

---

### Setup and Running the Application

To get the application up and running, follow these steps:

1.  **Environment Variables:** Create a `.env` file in the project's root directory and populate it with the following environment variables:

    ```
    GOOGLE_API_KEY=your_gemini_api_key
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=your_db_host
    ```

2.  **Ingest Documents:** Create a `data` folder at the root of your project. Place your flight-related markdown documents inside this folder (e.g., `how_to_book_flight.md`). Then, run the following command to ingest them into the database:

    ```bash
    python manage.py runscript document_ingester
    ```

3.  **Start the Server:** Launch the application using the Daphne server, which is recommended for asynchronous Django projects.

    ```bash
    daphne smart_ai_agent.asgi:application
    ```

---

### API Routes

The application provides two main API endpoints for user interaction:

#### 1\. User Access

- **URL:** `http://localhost:8000/api/user/access/`

- **Method:** `POST`

- **Description:** This endpoint handles user authentication. It either creates a new user or retrieves an existing one based on the provided email and full name. Upon success, it returns a unique token for subsequent requests.

- **Request Body:**

  ```json
  {
    "full_name": "John doe",
    "email": "john@doe.com"
  }
  ```

- **Successful Response:**

  ```json
  {
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
  }
  ```

#### 2\. Ask AI Agent

- **URL:** `http://localhost:8000/api/ask/`

- **Method:** `POST`

- **Description:** This is the core endpoint for interacting with the AI agent. You must include the authentication token obtained from the user access route in the request header. The agent will respond to your query based on the ingested documents.

- **Request Body:**

  ```json
  {
    "query": "how to book a flight"
  }
  ```

- **Authentication:**

  - **Header:** `Authorization`
  - **Value:** `Token <your_token>`

  **Note:** Replace `<your_token>` with the actual token you received.

Link to the UI
https://github.com/emekauser/smart_ai_frontend/

Install fmpeg before using voice command
