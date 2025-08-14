# 📡 Wixplore API Documentation & Testing Guide

## 🚀 Quick Start

### Import into Postman
1. Download `wixplore_postman_collection.json`
2. Open Postman → Import → Upload Files → Select the JSON file
3. Collection "Wixplore Cultural Data Intelligence API" will appear
4. Set environment variable `baseUrl` to `http://localhost:5000`

### Prerequisites
- API server running on `http://localhost:5000`
- Sample CSV files for testing

---

## 📋 API Endpoints Overview

### Base URL
- **Development**: `http://localhost:5000`
- **Production**: `https://your-vercel-app.vercel.app`

### Authentication
- **Current**: No authentication required
- **Future**: API key authentication for production

---

## 🔧 Endpoints Reference

### 1. Health Check
**GET** `/api/health`

**Response:**
```json
{
  "status": "API is running",
  "timestamp": "2025-08-14T06:31:05.344Z"
}
```

### 2. File Upload
**POST** `/api/upload`

**Content-Type**: `multipart/form-data`

**Body:**
- `dataset` (file): CSV, JSON, XLSX, or TXT file (max 10MB)

**Response:**
```json
{
  "status": "uploaded",
  "file": {
    "filename": "dataset-1755153096115-559268724.csv",
    "originalName": "test_data.csv",
    "size": 138,
    "path": "/data/dataset-1755153096115-559268724.csv",
    "mimetype": "text/csv"
  },
  "message": "File uploaded successfully"
}
```

### 3. List Available Agents
**GET** `/api/agents/list`

**Response:**
```json
{
  "agents": [
    {
      "id": "cleaner",
      "name": "Data Cleaner",
      "description": "Cleans and preprocesses data files"
    },
    {
      "id": "profiler",
      "name": "Data Profiler", 
      "description": "Analyzes data structure and quality"
    },
    {
      "id": "reasoner",
      "name": "Data Reasoner",
      "description": "Provides insights and reasoning about data"
    },
    {
      "id": "langextract",
      "name": "Language Extractor",
      "description": "Extracts and analyzes language patterns"
    }
  ]
}
```

### 4. Execute AI Agent
**POST** `/api/agents/run`

**Content-Type**: `application/json`

**Body:**
```json
{
  "filename": "dataset-1755153096115-559268724.csv",
  "agentType": "cleaner",
  "parameters": {
    "remove_duplicates": true,
    "handle_missing": "drop",
    "normalize_text": true
  }
}
```

**Agent Types & Parameters:**

#### Data Cleaner (`cleaner`)
```json
{
  "remove_duplicates": true,
  "handle_missing": "drop", // "drop", "fill", "interpolate"
  "normalize_text": true,
  "remove_outliers": false
}
```

#### Data Profiler (`profiler`)
```json
{
  "include_correlations": true,
  "include_distributions": true,
  "sample_size": 1000,
  "detect_patterns": true
}
```

#### Data Reasoner (`reasoner`)
```json
{
  "include_patterns": true,
  "include_anomalies": true,
  "include_predictions": false,
  "confidence_threshold": 0.7,
  "max_insights": 10
}
```

#### Language Extractor (`langextract`)
```json
{
  "detect_languages": true,
  "extract_keywords": true,
  "analyze_sentiment": false,
  "min_word_length": 3,
  "max_keywords": 50,
  "include_patterns": true,
  "text_columns": "auto"
}
```

### 5. List Uploaded Files
**GET** `/api/upload/files`

**Response:**
```json
{
  "files": [
    {
      "filename": "dataset-1755153096115-559268724.csv",
      "size": 138,
      "uploadDate": "2025-08-14T06:30:00.000Z"
    }
  ]
}
```

### 6. Delete File
**DELETE** `/api/upload/files/{filename}`

**Response:**
```json
{
  "message": "File deleted successfully"
}
```

---

## 📊 Sample Test Data

### Basic CSV (`test_data.csv`)
```csv
name,age,country,language
Alice,25,USA,English
Bob,30,France,French
Charlie,28,Germany,German
Diana,26,Spain,Spanish
Eva,29,Italy,Italian
```

### Multilingual CSV (`multilingual_data.csv`)
```csv
name,description,review,category
Alice Johnson,"A passionate teacher from New York","This platform is amazing for cultural exploration!",education
Maria García,"Antropóloga cultural española","Excelente plataforma para explorar culturas.",research
Hans Mueller,"Deutscher Historiker","Diese Anwendung ist wunderbar für kulturelle Forschung.",academic
Elena Rossi,"Blogger italiana di cucina","Questa piattaforma è fantastica per tradizioni culinarie!",food
Jean Dubois,"Chef français passionné","Plateforme magnifique pour partager cultures culinaires!",food
```

---

## 🧪 Testing Workflow

### 1. Complete Test Sequence
```bash
# 1. Health Check
curl http://localhost:5000/api/health

# 2. Upload file
curl -X POST -F "dataset=@test_data.csv" http://localhost:5000/api/upload

# 3. List agents
curl http://localhost:5000/api/agents/list

# 4. Run data cleaner (replace filename with actual uploaded filename)
curl -X POST -H "Content-Type: application/json" \
  -d '{"filename":"dataset-XXXXXX.csv","agentType":"cleaner"}' \
  http://localhost:5000/api/agents/run

# 5. Run data profiler
curl -X POST -H "Content-Type: application/json" \
  -d '{"filename":"dataset-XXXXXX.csv","agentType":"profiler"}' \
  http://localhost:5000/api/agents/run

# 6. List uploaded files
curl http://localhost:5000/api/upload/files
```

### 2. Postman Test Sequence
1. **Health Check** - Verify API is running
2. **Upload Sample CSV** - Upload test data (saves filename automatically)
3. **List Available Agents** - See all 4 agents
4. **Data Cleaner Agent** - Clean uploaded data
5. **Data Profiler Agent** - Analyze data quality
6. **Data Reasoner Agent** - Get insights
7. **Language Extractor Agent** - Analyze text (works better with multilingual data)
8. **List Uploaded Files** - See all uploaded files

---

## 📈 Expected Results

### Data Cleaner Results
```json
{
  "status": "success",
  "agent": "cleaner",
  "result": {
    "status": "success",
    "original_shape": [5, 4],
    "cleaned_shape": [5, 4],
    "rows_removed": 0,
    "missing_values_original": 0,
    "missing_values_cleaned": 0,
    "output_file": "/data/cleaned_dataset-XXXX.csv",
    "data_types": {
      "name": "object",
      "age": "int64",
      "country": "object", 
      "language": "object"
    }
  }
}
```

### Data Profiler Results
```json
{
  "status": "success",
  "agent": "profiler",
  "result": {
    "basic_info": {
      "total_rows": 5,
      "total_columns": 4,
      "memory_usage_mb": 0.001
    },
    "data_quality": {
      "overall_score": 100,
      "factors": [...]
    },
    "column_analysis": {...},
    "recommendations": [...]
  }
}
```

### Language Extractor Results (Multilingual Data)
```json
{
  "status": "success",
  "agent": "langextract", 
  "result": {
    "text_columns": ["description", "review"],
    "language_summary": {
      "primary_language": "spanish",
      "confidence": 0.43,
      "language_distribution": {
        "spanish": 0.43,
        "english": 0.23,
        "german": 0.20,
        "italian": 0.14
      }
    },
    "cultural_context": {
      "food_terms": 3,
      "tradition_terms": 2,
      "language_terms": 1
    }
  }
}
```

---

## ❌ Error Handling

### Common Errors

#### 400 Bad Request
```json
{
  "error": "Filename is required"
}
```

#### 404 Not Found
```json
{
  "error": "File not found"
}
```

#### 500 Server Error
```json
{
  "error": "Agent execution failed",
  "details": "Python module not found"
}
```

### File Upload Errors
```json
{
  "error": "Invalid file type. Only CSV, JSON, TXT, and XLSX files are allowed."
}
```

---

## 🔧 Advanced Usage

### Custom Parameters Example
```json
{
  "filename": "large_dataset.csv",
  "agentType": "profiler",
  "parameters": {
    "include_correlations": true,
    "include_distributions": true,
    "sample_size": 5000,
    "detect_patterns": true
  }
}
```

### Batch Processing
```bash
# Upload multiple files and process each
for file in *.csv; do
  echo "Processing $file"
  curl -X POST -F "dataset=@$file" http://localhost:5000/api/upload
  # Extract filename from response and process with agents
done
```

---

## 📝 OpenAPI Specification

Full OpenAPI 3.0 specification available in `api_documentation.yaml`

Import into:
- **Swagger UI**: For interactive documentation
- **Insomnia**: Alternative to Postman
- **API documentation generators**

---

## 🚀 Production Deployment

### Vercel Environment Variables
```bash
VITE_API_URL=https://your-vercel-app.vercel.app/api
PORT=5000
FRONTEND_ORIGIN=https://your-vercel-app.vercel.app
```

### Production URLs
- **API Base**: `https://your-vercel-app.vercel.app`
- **Frontend**: `https://your-vercel-app.vercel.app`

---

## 📞 Support & Contributing

- **Issues**: Create GitHub issue
- **Documentation**: See `README.md`
- **Test Results**: See `TEST_RESULTS.md`
- **Migration Guide**: See `MIGRATION_SUMMARY.md`

---

**Ready for testing! Import the Postman collection and start exploring the AI-powered cultural data intelligence platform! 🎉**
