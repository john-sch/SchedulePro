# SchedulePro

SchedulePro is a scheduling application built with FastAPI and an integrated React dashboard for managing events. It supports creating, updating, retrieving, and deleting scheduled events—including recurring events with conflict detection.

## Features

- Create events with a name, start date, start time, duration, and optional recurring days.
- Conflict detection to ensure no overlapping events on the same day/time.
- RESTful API endpoints for CRUD operations.
- Dockerized for easy deployment.

## Prerequisites

- Docker (if you choose to use the Dockerized version)
- Alternatively, Python 3.8+ and Git if running locally

## Running with Docker
This project uses a multi-stage Dockerfile to build the React frontend and then package the FastAPI backend along with the built static files. Use the following commands to build and run the Docker container:

1. **Build the Docker image**

   \`\`\`bash
   docker build -t schedulepro .
   \`\`\`

2. **Run the Docker container**

   \`\`\`bash
   docker run -p 8000:8000 schedulepro
   \`\`\`

   The API will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
   API: http://127.0.0.1:8000
   Dashboard: http://127.0.0.1:8000/dashboard

3. **Interactive API Documentation**

   - [Swagger UI](http://127.0.0.1:8000/docs)
   - [ReDoc](http://127.0.0.1:8000/redoc)

## Running Locally (Non-Docker)

1. **Clone the Repository**

   \`\`\`bash
   git clone https://github.com/john-sch/SchedulePro.git
   cd SchedulePro
   \`\`\`

2. **Create and Activate a Virtual Environment**

   \`\`\`bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   \`\`\`

3. **Install Dependencies**

   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Run the Application**

   \`\`\`bash
   python run.py
   \`\`\`

## Assumptions

- **Time Zones:** All times are considered local; time zone handling is not implemented.
- **Recurring Events:** Recurring events repeat indefinitely until manually modified or deleted.
- **Conflict Detection:** Overlapping events are detected by checking if time intervals overlap on the same day or recurring day.
- **Persistence:** The application uses SQLite for simplicity. In production, a more robust database (e.g., PostgreSQL) should be used.
- **Data Storage:** Recurring days are stored using SQLAlchemy’s PickleType for simplicity. A normalized approach would be preferable in a production environment.
- **Migrations:** The database schema is created on startup without migrations.
