const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs-extra');

const router = express.Router();

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = path.join(__dirname, '../data');
    fs.ensureDirSync(uploadDir);
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({ 
  storage: storage,
  limits: {
    fileSize: 10 * 1024 * 1024 // 10MB limit
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['.csv', '.json', '.txt', '.xlsx'];
    const fileExt = path.extname(file.originalname).toLowerCase();
    
    if (allowedTypes.includes(fileExt)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type. Only CSV, JSON, TXT, and XLSX files are allowed.'));
    }
  }
});

// Handle file upload
router.post('/', upload.single('dataset'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const fileInfo = {
      filename: req.file.filename,
      originalName: req.file.originalname,
      size: req.file.size,
      path: req.file.path,
      mimetype: req.file.mimetype
    };

    // TODO: Add file validation and preprocessing logic here
    console.log('File uploaded:', fileInfo);

    res.json({ 
      status: 'uploaded',
      file: fileInfo,
      message: 'File uploaded successfully'
    });

  } catch (error) {
    console.error('Upload error:', error);
    res.status(500).json({ error: 'Upload failed: ' + error.message });
  }
});

// Get uploaded files list
router.get('/files', async (req, res) => {
  try {
    const dataDir = path.join(__dirname, '../data');
    const files = await fs.readdir(dataDir);
    
    const fileList = await Promise.all(
      files.map(async (filename) => {
        const filePath = path.join(dataDir, filename);
        const stats = await fs.stat(filePath);
        return {
          filename,
          size: stats.size,
          uploadDate: stats.birthtime
        };
      })
    );

    res.json({ files: fileList });
  } catch (error) {
    console.error('Error listing files:', error);
    res.status(500).json({ error: 'Failed to list files' });
  }
});

// Delete uploaded file
router.delete('/files/:filename', async (req, res) => {
  try {
    const filename = req.params.filename;
    const filePath = path.join(__dirname, '../data', filename);
    
    await fs.remove(filePath);
    res.json({ message: 'File deleted successfully' });
  } catch (error) {
    console.error('Error deleting file:', error);
    res.status(500).json({ error: 'Failed to delete file' });
  }
});

module.exports = router;
