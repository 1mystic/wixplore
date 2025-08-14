# Wixplore - Cultural Data Intelligence Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Vue.js](https://img.shields.io/badge/Vue.js-3.x-success.svg)
![Node.js](https://img.shields.io/badge/Node.js-18.x-green.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Vercel](https://img.shields.io/badge/Vercel-Ready-black.svg)

**Wixplore** is a modern web application that combines cultural exploration with intelligent data processing. The platform features Vue 3 frontend with Node.js serverless functions and Python AI agents for advanced data analysis.

## ✨ Key Features

* **Cultural Exploration:** Interactive quizzes and cultural content
* **Data Upload & Processing:** Upload datasets for AI-powered analysis
* **Intelligent Agents:** Python-powered data cleaning, profiling, and reasoning
* **Language Extraction:** Advanced text analysis and language detection
* **User Profiles:** Personalized learning experiences
* **Real-time Analytics:** Live data insights and visualizations
* **Serverless Architecture:** Optimized for Vercel deployment
* **Modern UI:** Clean, responsive interface built with Vue 3

## 🏗️ Architecture

```
/project-root
│── package.json              # Root package for workspace management
│── vercel.json               # Vercel deployment configuration
│── setup.sh                 # Development setup script
│── dev.sh                   # Development runner script
│
│── /frontend                 # Vue 3 Application
│   ├── package.json
│   ├── vite.config.js
│   ├── src/
│   │   ├── components/       # Vue components
│   │   ├── views/           # Page components
│   │   ├── router/          # Vue Router configuration
│   │   ├── store/           # Vuex store
│   │   └── services/        # API services
│   └── public/              # Static assets
│
│── /api                      # Node.js Serverless Functions
│   ├── index.js             # Main Express server
│   ├── upload.js            # File upload handling
│   ├── process-data.js      # Python agent orchestration
│   └── package.json
│
│── /agents                   # Python AI Agents
│   ├── agent_cleaner.py     # Data cleaning agent
│   ├── agent_profiler.py    # Data profiling agent
│   ├── agent_reasoner.py    # Data reasoning agent
│   ├── langextract_agent.py # Language extraction agent
│   └── requirements.txt
│
└── /data                     # Temporary file storage
```

## 🛠️ Tech Stack

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vue Router 4** - Official router for Vue.js
- **Vuex 4** - State management pattern
- **Vite** - Fast build tool and dev server
- **Bootstrap 5** - CSS framework
- **Chart.js** - Data visualization

### Backend
- **Node.js** - JavaScript runtime
- **Express** - Web application framework
- **Multer** - File upload middleware
- **Axios** - HTTP client library

### AI Agents
- **Python 3** - Programming language
- **Pandas** - Data manipulation library
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning library

### Deployment
- **Vercel** - Serverless hosting platform
- **Git** - Version control

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Git

### Development Setup

1. **Clone and setup:**
   ```bash
   git clone <your-repo-url>
   cd wixplore
   chmod +x setup.sh dev.sh
   ./setup.sh
   ```

2. **Start development servers:**
   ```bash
   ./dev.sh
   ```

   Or manually:
   ```bash
   # Terminal 1: Frontend (port 3000)
   npm run dev:frontend
   
   # Terminal 2: API (port 5000) 
   npm run dev:api
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - API: http://localhost:5000/api/health

### Production Deployment

**Deploy to Vercel:**
```bash
npm install -g vercel
vercel --prod
```

The application will be deployed with:
- Frontend served as static site
- API endpoints as serverless functions
- Automatic CI/CD from Git repository

## 📡 API Endpoints

### File Upload
- `POST /api/upload` - Upload dataset files
- `GET /api/upload/files` - List uploaded files
- `DELETE /api/upload/files/:filename` - Delete file

### AI Agents
- `POST /api/agents/run` - Execute Python agents
- `GET /api/agents/list` - Get available agents
- `GET /api/agents/status/:jobId` - Check processing status

### Health & Info
- `GET /api/health` - API health check

## 🤖 AI Agents

### Data Cleaner (`agent_cleaner.py`)
- Removes duplicates and handles missing values
- Normalizes text data
- Provides cleaning statistics

### Data Profiler (`agent_profiler.py`)
- Analyzes data structure and quality
- Generates comprehensive data profiles
- Calculates data quality scores

### Data Reasoner (`agent_reasoner.py`)
- Provides intelligent insights about data
- Detects patterns and anomalies
- Generates business recommendations

### Language Extractor (`langextract_agent.py`)
- Extracts text features and patterns
- Detects languages and cultural context
- Analyzes linguistic characteristics

## 🔧 Configuration

### Environment Variables

Create `.env` file (use `.env.example` as template):

```bash
# Frontend
VITE_API_URL=http://localhost:5000/api

# API
PORT=5000
FRONTEND_ORIGIN=http://localhost:3000

# Python Agents
PYTHON_PATH=python3
MAX_FILE_SIZE=10485760
UPLOAD_DIR=./data
```

### Vercel Configuration

The `vercel.json` file configures:
- Frontend build from `/frontend`
- API routes as serverless functions
- Proper routing between frontend and API

## 📁 File Structure Details

### Frontend Structure
```
frontend/src/
├── components/           # Reusable Vue components
│   ├── CulturalContext.vue
│   └── DataLab/
├── views/               # Page components
│   ├── admin/           # Admin interface
│   └── user/            # User interface
├── router/              # Vue Router setup
├── store/               # Vuex state management
└── services/            # API interaction layer
```

### API Structure
```
api/
├── index.js             # Express app setup and routing
├── upload.js            # File upload handling with multer
├── process-data.js      # Python agent execution
└── package.json         # Node.js dependencies
```

## 🧪 Testing

```bash
# Frontend tests
cd frontend && npm test

# API tests
cd api && npm test

# Python agent tests
cd agents && python -m pytest
```

## 📈 Performance

- **Frontend:** Optimized Vue 3 with Vite for fast HMR
- **API:** Serverless functions with automatic scaling
- **Agents:** Efficient Python data processing
- **Deployment:** Global CDN via Vercel

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation in `/docs`
- Review the API documentation in `api_docs.yaml`

---

**Built with ❤️ for cultural exploration and data intelligence**
    * [Python](https://www.python.org/)
    * [Flask](https://flask.palletsprojects.com/) - A microframework for Python based on Werkzeug, Jinja 2 and good intentions.
    * [Celery](https://docs.celeryq.dev/) - A distributed task queue.
    * [Celery Beat](https://docs.celeryq.dev/en/stable/schedule.html) - A scheduler for Celery tasks.
    * [Redis](https://redis.io/) - An in-memory data structure store, used for caching and as a message broker.
    * [Flask-Mailman](https://flask-mailman.readthedocs.io/en/stable/) - A Flask extension for sending emails.
    * [Google Generative AI](https://ai.google.dev/) - For providing intelligent feedback on quiz answers.
* **Frontend:**
    * [Vue.js](https://v3.vuejs.org/) - A progressive JavaScript framework.
    * [Vue 3 Options API](https://vuejs.org/guide/introduction.html#options-api) - The Options API for structuring Vue components.

## 🚀 Getting Started

To get Whiz.it up and running on your local machine, follow these steps:

### Prerequisites

* Python 3.x
* Node.js and npm (or yarn)
* Redis server installed and running
* Google Cloud Project with the Generative AI API enabled and API key configured
* Email service credentials for Flask-Mailman
### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd whiz.it
    ```

2.  **Set up the backend (ServerA):**
    ```bash
    cd serverA
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Configure environment variables for the backend:**
    Create a `.env` file in the `root` directory and configure the following environment variables:
    ```
    GOOGLE_API_KEY = ''
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quizmdb.db'

    # JWT
    JWT_SECRET_KEY = ''

    # Redis and Celery
    REDIS_URL = 'redis://localhost:6379/0'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    # Caching
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = 'redis://localhost:6379/0'
    CACHE_DEFAULT_TIMEOUT = 300

    # Mail
    MAIL_SERVER = 'your_mail_server.com' 
    MAIL_PORT = 587                     
    MAIL_USE_TLS = True                 
    MAIL_USERNAME = 'your_email@example.com'   
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = 'Whiz.it <noreply@example.com>' 
    ```
    **Note:** Make sure to replace the placeholder values (e.g., `your_mail_server.com`, email addresses, passwords, JWT secret key, and Google API key) with your actual configuration.

    

4.  **Run the Redis server:**
    Ensure your Redis server is running. You might need to start it in a separate terminal if it's not already running as a service.

    ```bash
    redis-server
    ```

5.  **Run the Celery worker and beat (from `serverA`):**
    Open two separate terminal windows in the `serverA` directory:
    ```bash
    celery -A run.celery worker -l info
    celery -A run.celery beat -l info
    ```
    *(Assuming you have initialized your Celery app instance as `celery` in your `run.py` file.)*

6.  **Run the Flask development server (from `serverA`):**
    ```bash
    python run.py
    ```
    The backend API will likely be accessible at `http://localhost:5000`.



7.  **Configure frontend environment variables:**
    Create a `.env` file in the `frontend` directory (if needed) to configure API endpoints (e.g., pointing to `http://localhost:5000`) or other environment-specific settings.



## ⚙️ Usage

Once the application is running, users can:

* **Browse Quizzes:** Explore available quizzes by subject and chapter.
* **Attempt Quizzes:** Select a quiz and answer the questions.
* **Receive AI Feedback:** Get instant explanations and insights on their answers.
* **Manage Bookmarks:** Add and review challenging questions later.
* **View Scores:** Check past quiz results and track their progress.
* **Access Profile:** See their leaderboard ranking and manage their account.
* **Explore Summary:** Get a quick overview of their quiz activity.
* **Download/Email Reports:** Generate and share their performance reports.
* **Receive Notifications:** Get daily quiz reminders and monthly activity summaries via email.
* **Utilize AI Analysis:** Gain deeper insights into their learning patterns and areas for improvement.

Administrators can access the admin panel (usually at a specific route like `/admin`) to manage users, quizzes, subjects, chapters, and other platform configurations based on their assigned roles.

## 🖼️ Screenshots

Here are some screenshots of the application:

### User Dashboard
![User Dashboard](screenshots/userdash.png)

### AI Report
![AI Report](screenshots/aireport.png)

### Landing Page
![Landing Page](screenshots/land.png)

### Login Page
![Login Page](screenshots/login.png)

### User Profile
![User Profile](screenshots/profile.png)

### Quiz Page
![Quiz Page](screenshots/quiz.png)

### Summary Page
![Summary Page](screenshots/summary.png)

### AI Feedback
![AI Feedback](screenshots/feedback.png)

### Admin Dashboard
![Admin Dashboard](screenshots/admindash.png)

### Admin Panel
![Admin Panel](screenshots/adminp.png)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

## 🙏 Acknowledgements

* Thanks to the developers of Flask, Vue.js, Celery, Redis, Flask-Mailman, and Google Generative AI for their amazing tools and libraries.
* *Also I am grateful to the IITM BS Modern Application Dedvelopmet team for their continued support throughout*

## 📬 Contact
*atharvkhare18@gmail.com*
*(atharvk4u.vercel.app)*