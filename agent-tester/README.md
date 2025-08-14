# 🤖 Wixplore AI Agent Tester

A simple, standalone web interface for testing and demonstrating the Wixplore AI agents. This mini-website allows users to upload data files and run AI analysis without needing the full application.

## 🚀 Features

- **Drag & Drop File Upload** - Easy file uploading with visual feedback
- **4 AI Agents Ready** - Data Cleaner, Profiler, Reasoner, and Language Extractor
- **Real-time Results** - Formatted, user-friendly AI analysis results
- **Responsive Design** - Works on desktop, tablet, and mobile
- **No Framework Dependencies** - Pure HTML, CSS, and JavaScript

## 📁 Files

```
agent-tester/
├── index.html      # Main webpage
├── script.js       # JavaScript functionality
└── README.md       # This file
```

## 🎯 Usage

### Quick Start
1. Make sure your API server is running:
   ```bash
   cd ../api && npm run dev
   ```

2. Open `index.html` in any web browser:
   ```bash
   # Option 1: Direct file open
   open index.html
   
   # Option 2: Simple HTTP server
   python -m http.server 8080
   # Then visit: http://localhost:8080
   ```

3. Upload a CSV file and click any AI agent button!

### Sample Test Files

Create these sample files to test the agents:

**basic_data.csv**
```csv
name,age,country,language,description
Alice,25,USA,English,Cultural researcher from New York
Maria,30,Spain,Spanish,Antropóloga especializada en tradiciones
Hans,28,Germany,German,Historiker interessiert an Kulturanalyse
Elena,26,Italy,Italian,Blogger culinario tradizionale
Jean,32,France,French,Chef spécialisé en cuisine traditionnelle
```

**multilingual_reviews.csv**
```csv
product,review,rating,country,language
Traditional Food,"This authentic dish reminds me of my grandmother's cooking",5,USA,English
Comida Tradicional,"Esta receta auténtica me recuerda a mi abuela",5,Mexico,Spanish
Traditionelles Essen,"Dieses authentische Gericht erinnert mich an meine Oma",4,Germany,German
Cibo Tradizionale,"Questa ricetta autentica mi ricorda mia nonna",5,Italy,Italian
Nourriture Traditionnelle,"Ce plat authentique me rappelle ma grand-mère",4,France,French
```

## 🔧 Configuration

### API Endpoint
Change the API URL in `script.js`:
```javascript
const API_BASE_URL = 'http://localhost:5000'; // Change this for production
```

### Styling
The page uses Bootstrap 5 CDN for styling. You can customize colors and layout by modifying the CSS in `index.html`.

## 📊 AI Agent Results

### Data Cleaner
- Shows data shape changes (before/after)
- Reports missing values and duplicates removed
- Displays column data types
- Indicates data quality improvements

### Data Profiler  
- Basic dataset statistics (rows, columns, memory)
- Data quality score out of 100
- Completeness and uniqueness percentages
- Actionable recommendations

### Data Reasoner
- Key insights about the data
- Pattern detection results
- Anomaly identification
- Summary of findings

### Language Extractor
- Primary language detection with confidence
- Language distribution across text
- Cultural context extraction
- Keywords and phrases found

## 🌐 Deployment Options

### Option 1: Local File
Simply open `index.html` in any browser. Works for local testing.

### Option 2: Simple HTTP Server
```bash
# Python
python -m http.server 8080

# Node.js (if you have http-server installed)
npx http-server -p 8080

# PHP
php -S localhost:8080
```

### Option 3: Deploy to Static Hosting
Upload the files to:
- **Netlify**: Drag & drop the folder
- **Vercel**: Connect to your git repository
- **GitHub Pages**: Push to a repository and enable Pages
- **AWS S3**: Upload as static website

## 🔒 Security Notes

- Currently no authentication - suitable for demos only
- File uploads are limited to 10MB
- Only accepts CSV, JSON, TXT, and XLSX files
- For production, add API key authentication

## 🚀 Future Enhancements

### Planned Features
- **Gemini AI Integration** - Natural language insights
- **Result Sharing** - Share analysis via links
- **Batch Processing** - Upload multiple files
- **Export Results** - Download analysis reports
- **Real-time Chat** - Ask questions about your data

### Gemini Integration Preview
```javascript
// Future: Natural language insights
async function generateNaturalInsights(analysisData) {
    const response = await fetch('/api/gemini/insights', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            data: analysisData,
            prompt: "Explain these cultural data insights in simple terms"
        })
    });
    return response.json();
}
```

## 📞 Support

- **Main Project**: See root README.md
- **API Documentation**: See API_TESTING_GUIDE.md
- **Issues**: Report bugs in the main project repository

---

**🎉 Ready to test your AI agents! Upload a file and see the magic happen!**
