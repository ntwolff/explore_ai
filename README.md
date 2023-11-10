# FinTech Assistant Platform

A conversational AI application powered by OpenAI's GPT-3 that provides an interactive front-end user experience for financial services. It uses OpenAI's Assistant API for handling threads and messaging and integrates with external services such as weather APIs.

## Directory Structure
```
/
|-- app.py                                 # Flask backend entry point
|-- services/                              # Backend services
|   |-- openai_assistant_service.py        # Handles interaction with OpenAI Assistant
|   |-- weather_service.py                 # Fetches weather data
|-- interaction/                           # Handles logic between services and user requests
|   |-- interaction_handler.py
|-- utils/                                 # Utility files including service registry
|   |-- service_registry.py
|-- config.py                              # Configuration and global variable manager
|-- tests/                                 # Test cases
|   |-- services/                          # Test cases for services
|   |-- interaction/                       # Test cases for interaction handlers
|-- frontend/                              # React-based front end
|   |-- (React project structure)
|-- assistant_instructions.txt             # Instructions for OpenAI Assistant
|-- requirements.txt                       # Python dependencies
|-- README.md                              # Project documentation
```

## Backend Installation

Ensure you have Python 3.6+ installed on your system. The following steps outline the process to get the backend running:

1. Clone the repository:
```bash
git clone https://github.com/your-repo/fintech-assistant.git
cd fintech-assistant
```

2. Install the backend dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the `.env` file with the required environment variables such as your OpenAI API key:
```env
OPENAI_API_KEY=your_openai_api_key
```

4. Start the Flask app:
```bash
python app.py
```

By default, the app will run on `http://localhost:5000`.

## Frontend Installation

Ensure you have Node.js and npm installed. Follow the steps to start the front-end application:

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install the required node packages:
```bash
npm install
```

3. Update `.env` file with the backend API URL location:
```env
REACT_APP_API_URL=http://localhost:5000
```

4. Start the React development server:
```bash
npm start
```

By default, the React app will run on `http://localhost:3000`.

## Running Tests

Execute the automated tests for this system by running:

```bash
python -m unittest discover -s tests
```

Make sure the `tests` directory contains an `__init__.py` file for discovery.

## API Documentation

We use Swagger for API documentation. Access the documentation at `http://localhost:5000/api/docs` after starting the Flask application.

## Deployment

Before deploying, build the production version of the React app:

```bash
cd frontend
npm run build
```

Follow best practices for deploying Flask and React applications to your favorite cloud platform.
```