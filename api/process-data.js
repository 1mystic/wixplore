const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs-extra');

const router = express.Router();

// Run Python agents workflow
router.post('/run', async (req, res) => {
  try {
    const { filename, agentType, parameters } = req.body;

    if (!filename) {
      return res.status(400).json({ error: 'Filename is required' });
    }

    const filePath = path.join(__dirname, '../data', filename);
    
    // Check if file exists
    if (!(await fs.pathExists(filePath))) {
      return res.status(404).json({ error: 'File not found' });
    }

    // Determine which Python agent to run
    const agentMap = {
      'cleaner': 'agent_cleaner.py',
      'profiler': 'agent_profiler.py', 
      'reasoner': 'agent_reasoner.py',
      'langextract': 'langextract_agent.py'
    };

    const agentScript = agentMap[agentType] || 'agent_cleaner.py';
    const agentPath = path.join(__dirname, '../agents', agentScript);

    // Prepare arguments for Python script
    const pythonArgs = [agentPath, filePath];
    if (parameters) {
      pythonArgs.push(JSON.stringify(parameters));
    }

    // Execute Python agent using the virtual environment
    const pythonVenvPath = path.join(__dirname, '../agents/.venv/bin/python');
    const pythonCommand = require('fs').existsSync(pythonVenvPath) ? pythonVenvPath : 'python3';
    const pythonProcess = spawn(pythonCommand, pythonArgs);
    
    let output = '';
    let errorOutput = '';

    pythonProcess.stdout.on('data', (data) => {
      output += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        try {
          // Try to parse JSON output from Python script
          const result = JSON.parse(output);
          res.json({
            status: 'success',
            agent: agentType,
            result: result
          });
        } catch (parseError) {
          // If output is not JSON, return as text
          res.json({
            status: 'success',
            agent: agentType,
            result: { output: output.trim() }
          });
        }
      } else {
        console.error('Python agent error:', errorOutput);
        res.status(500).json({
          error: 'Agent execution failed',
          details: errorOutput
        });
      }
    });

    pythonProcess.on('error', (error) => {
      console.error('Failed to start Python process:', error);
      res.status(500).json({
        error: 'Failed to start agent process',
        details: error.message
      });
    });

  } catch (error) {
    console.error('Process data error:', error);
    res.status(500).json({ error: 'Processing failed: ' + error.message });
  }
});

// Get available agents
router.get('/list', (req, res) => {
  const agents = [
    {
      id: 'cleaner',
      name: 'Data Cleaner',
      description: 'Cleans and preprocesses data files'
    },
    {
      id: 'profiler',
      name: 'Data Profiler',
      description: 'Analyzes data structure and quality'
    },
    {
      id: 'reasoner',
      name: 'Data Reasoner',
      description: 'Provides insights and reasoning about data'
    },
    {
      id: 'langextract',
      name: 'Language Extractor',
      description: 'Extracts and analyzes language patterns'
    }
  ];

  res.json({ agents });
});

// Get agent execution status/logs
router.get('/status/:jobId', (req, res) => {
  // TODO: Implement job tracking system for long-running agents
  res.json({ 
    message: 'Job tracking not implemented yet',
    jobId: req.params.jobId
  });
});

module.exports = router;
