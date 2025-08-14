const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
const allowedOrigins = [
  'http://localhost:3000',    // Main Vue frontend
  'http://localhost:8080',    // Agent tester
  'http://localhost:8081',    // Agent tester alternative
  'http://127.0.0.1:8080',    // Alternative localhost
  'http://127.0.0.1:8081',    // Alternative localhost  
  'http://127.0.0.1:3000',    // Alternative localhost
  'http://0.0.0.0:8080',      // Python server origin
  'http://0.0.0.0:8081',      // Python server origin
  process.env.FRONTEND_ORIGIN // Production origin
].filter(Boolean); // Remove any undefined values

app.use(cors({
  origin: function (origin, callback) {
    // Allow requests with no origin (like mobile apps or curl requests)
    if (!origin) return callback(null, true);
    
    // Allow any localhost/127.0.0.1/0.0.0.0 origin during development
    if (origin.includes('localhost') || origin.includes('127.0.0.1') || origin.includes('0.0.0.0')) {
      return callback(null, true);
    }
    
    if (allowedOrigins.indexOf(origin) !== -1) {
      callback(null, true);
    } else {
      console.log('CORS blocked origin:', origin);
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true
}));
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// Import route handlers
const uploadHandler = require('./upload');
const processDataHandler = require('./process-data');

// Routes
app.use('/api/upload', uploadHandler);
app.use('/api/agents', processDataHandler);

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'API is running', timestamp: new Date().toISOString() });
});

// Quiz endpoints (placeholder - migrate from Flask)
app.get('/api/quiz', (req, res) => {
  res.json({ message: 'Quiz endpoints - to be implemented' });
});

app.post('/api/quiz', (req, res) => {
  res.json({ message: 'Quiz creation - to be implemented' });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// For local development
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
}

// Export for Vercel
module.exports = app;
