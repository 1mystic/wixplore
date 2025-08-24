# Wixplore - Cultural Data Intelligence Platform (whiz.it - v2)

[![ALT TEXT](https://img.youtube.com/vi/TfYUGgWR7j4/maxresdefault.jpg)](https://www.youtube.com/watch?v=TfYUGgWR7j4)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Vue.js](https://img.shields.io/badge/Vue.js-3.x-success.svg)
![Node.js](https://img.shields.io/badge/Node.js-18.x-green.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Vercel](https://img.shields.io/badge/Vercel-Ready-black.svg)

**Wixplore** is a modern web application that combines cultural exploration with intelligent data processing. The platform features Vue 3 frontend with Node.js serverless functions and Python AI agents for advanced data analysis.

##  Key Features

- **Cultural Exploration** - Interactive quizzes and cultural content discovery
- **Data Upload & Processing** - Upload datasets for AI-powered analysis
- **Intelligent Agents** - Python-powered data cleaning, profiling, and reasoning
- **Language Extraction** - Advanced text analysis and language detection
- **User Profiles** - Personalized learning experiences and progress tracking
- **Real-time Analytics** - Live data insights and visualizations
- **Serverless Architecture** - Optimized for Vercel deployment
- **Modern UI** - Clean, responsive interface built with Vue 3

##  Architecture

```
/project-root
├── package.json              # Root package for workspace management
├── vercel.json               # Vercel deployment configuration
├── setup.sh                 # Development setup script
├── dev.sh                   # Development runner script
│
├── /frontend                 # Vue 3 Application
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
├── /api                      # Node.js Serverless Functions
│   ├── index.js             # Main Express server
│   ├── upload.js            # File upload handling
│   ├── process-data.js      # Python agent orchestration
│   └── package.json
│
├── /agents                   # Python AI Agents
│   ├── agent_cleaner.py     # Data cleaning agent
│   ├── agent_profiler.py    # Data profiling agent
│   ├── agent_reasoner.py    # Data reasoning agent
│   ├── langextract_agent.py # Language extraction agent
│   └── requirements.txt
│
├── /agent-tester             # Standalone Testing Interface
│   ├── index.html           # Web interface for testing agents
│   ├── script.js            # Frontend functionality
│   └── sample_cultural_data.csv # Test data
│
└── /data                     # Temporary file storage
```

##  Tech Stack

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

## >> Quick Start <<

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Git

### Development Setup

1. **Clone and setup:**
   ```bash
   git clone https://github.com/1mystic/wixplore.git
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
   - **Main App**: http://localhost:3000
   - **API Health**: http://localhost:5000/api/health
   - **Agent Tester**: http://localhost:8081 (after starting `cd agent-tester && python3 -m http.server 8081`)

## API Documentation

### File Upload Endpoints
- `POST /api/upload` - Upload dataset files (CSV, JSON, TXT, XLSX)
- `GET /api/upload/files` - List all uploaded files
- `DELETE /api/upload/files/:filename` - Delete specific file

### AI Agent Endpoints
- `POST /api/agents/run` - Execute Python agents on uploaded data
- `GET /api/agents/list` - Get available agents and their descriptions
- `GET /api/health` - API health check

**Example Agent Request:**
```json
{
  "filename": "dataset.csv",
  "agentType": "cleaner",
  "parameters": {
    "remove_duplicates": true,
    "handle_missing": "drop"
  }
}
```

## Agents

### Data Cleaner (`agent_cleaner.py`)
- Removes duplicates and handles missing values
- Normalizes text data and removes outliers
- Provides comprehensive cleaning statistics

### Data Profiler (`agent_profiler.py`)
- Analyzes data structure and quality metrics
- Generates data quality scores and distributions
- Provides actionable recommendations

### Data Reasoner (`agent_reasoner.py`)
- Provides intelligent insights about data patterns
- Detects anomalies and statistical outliers
- Generates business-oriented recommendations

### Language Extractor (`langextract_agent.py`)
- Detects languages and extracts linguistic features
- Analyzes cultural context and text patterns
- Provides multilingual data insights

## Agent Tester

A standalone web interface for testing AI agents without running the full application:

```bash
cd agent-tester
python3 -m http.server 8081
# Visit: http://localhost:8081
```

Features:
- Drag & drop file upload
- One-click agent testing
- Beautiful results formatting
- Sample multilingual data included

## Configuration

### Environment Variables

Create `.env` file in project root:

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

### Production Deployment

**Deploy to Vercel:**
```bash
npm install -g vercel
vercel --prod
```

The `vercel.json` configuration handles:
- Frontend build from `/frontend`
- API routes as serverless functions
- Proper routing between frontend and API

## Testing

```bash
# Frontend tests
cd frontend && npm test

# API tests
cd api && npm test

# Python agent tests
cd agents && python -m pytest

# End-to-end testing
npm run test:e2e
```

## Screenshots

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

## Performance Features

- **Frontend**: Optimized Vue 3 with Vite for fast Hot Module Replacement
- **API**: Serverless functions with automatic scaling
- **Agents**: Efficient Python data processing with virtual environments
- **Deployment**: Global CDN distribution via Vercel
- **Caching**: Redis-based caching for improved response times

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## Support & Documentation

- **API Documentation**: See `api_documentation.yaml` for complete OpenAPI spec
- **Testing Guide**: Check `API_TESTING_GUIDE.md` for comprehensive testing instructions
- **Postman Collection**: Import `wixplore_postman_collection.json` for API testing
- **Migration Notes**: Review `MIGRATION_SUMMARY.md` for architecture details

## Contact

For questions, feedback, or collaboration:

- **Email**: atharvkhare18@gmail.com
- **Portfolio**: [atharvk.me](https://atharvk.me)
- **GitHub**: [@1mystic](https://github.com/1mystic)

---

**Built with ❤️ for cultural exploration and intelligent data analysis**
