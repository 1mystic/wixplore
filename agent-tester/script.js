// Configuration
const API_BASE_URL = 'http://localhost:5000';
let uploadedFileName = null;

// DOM Elements
const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const agentButtons = document.querySelectorAll('.agent-btn[data-agent]');
const runAllButton = document.getElementById('runAllAgents');
const clearButton = document.getElementById('clearResults');
const loadingIndicator = document.getElementById('loadingIndicator');
const resultsContainer = document.getElementById('resultsContainer');

// File Upload Handlers
uploadZone.addEventListener('click', () => fileInput.click());
uploadZone.addEventListener('dragover', handleDragOver);
uploadZone.addEventListener('dragleave', handleDragLeave);
uploadZone.addEventListener('drop', handleDrop);
fileInput.addEventListener('change', handleFileSelect);

// Agent Button Handlers
agentButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const agentType = btn.dataset.agent;
        runAgent(agentType);
    });
});

runAllButton.addEventListener('click', runAllAgents);
clearButton.addEventListener('click', clearResults);

// Drag and Drop Functions
function handleDragOver(e) {
    e.preventDefault();
    uploadZone.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadZone.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadZone.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        uploadFile(files[0]);
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        uploadFile(file);
    }
}

// File Upload Function
async function uploadFile(file) {
    // Validate file type
    const allowedTypes = ['text/csv', 'application/json', 'text/plain', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
    const allowedExtensions = ['.csv', '.json', '.txt', '.xlsx'];
    
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
        showAlert('Invalid file type. Please upload CSV, JSON, TXT, or XLSX files.', 'danger');
        return;
    }

    // Validate file size (10MB max)
    if (file.size > 10 * 1024 * 1024) {
        showAlert('File size too large. Maximum size is 10MB.', 'danger');
        return;
    }

    const formData = new FormData();
    formData.append('dataset', file);

    try {
        showLoading(true);
        const response = await fetch(`${API_BASE_URL}/api/upload`, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        
        if (response.ok) {
            uploadedFileName = result.file.filename;
            showFileInfo(file.name, result.file.size);
            enableAgentButtons();
            showAlert('File uploaded successfully!', 'success');
        } else {
            throw new Error(result.error || 'Upload failed');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showAlert(`Upload failed: ${error.message}`, 'danger');
    } finally {
        showLoading(false);
    }
}

// Show File Info
function showFileInfo(originalName, size) {
    fileName.innerHTML = `
        <strong>File:</strong> ${originalName}<br>
        <strong>Size:</strong> ${formatFileSize(size)}<br>
        <strong>Status:</strong> <span class="status-badge bg-success text-white">Ready for processing</span>
    `;
    fileInfo.style.display = 'block';
}

// Format File Size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Enable Agent Buttons
function enableAgentButtons() {
    agentButtons.forEach(btn => {
        btn.disabled = false;
        btn.classList.remove('opacity-50');
    });
    runAllButton.disabled = false;
    runAllButton.classList.remove('opacity-50');
}

// Run Single Agent
async function runAgent(agentType) {
    if (!uploadedFileName) {
        showAlert('Please upload a file first.', 'warning');
        return;
    }

    const agentConfig = {
        cleaner: {
            name: 'Data Cleaner',
            icon: 'fas fa-broom',
            color: 'info',
            parameters: {
                remove_duplicates: true,
                handle_missing: 'drop',
                normalize_text: true
            }
        },
        profiler: {
            name: 'Data Profiler',
            icon: 'fas fa-chart-bar',
            color: 'success',
            parameters: {
                include_correlations: true,
                include_distributions: true,
                sample_size: 1000
            }
        },
        reasoner: {
            name: 'Data Reasoner',
            icon: 'fas fa-brain',
            color: 'warning',
            parameters: {
                include_patterns: true,
                include_anomalies: true,
                max_insights: 10
            }
        },
        langextract: {
            name: 'Language Extractor',
            icon: 'fas fa-language',
            color: 'danger',
            parameters: {
                detect_languages: true,
                extract_keywords: true,
                max_keywords: 50
            }
        }
    };

    const config = agentConfig[agentType];
    if (!config) {
        showAlert('Unknown agent type.', 'danger');
        return;
    }

    try {
        showLoading(true);
        
        const requestBody = {
            filename: uploadedFileName,
            agentType: agentType,
            parameters: config.parameters
        };

        const response = await fetch(`${API_BASE_URL}/api/agents/run`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        const result = await response.json();
        
        if (response.ok) {
            displayResult(config, result, agentType);
        } else {
            throw new Error(result.error || 'Agent execution failed');
        }
    } catch (error) {
        console.error('Agent execution error:', error);
        showAlert(`Agent execution failed: ${error.message}`, 'danger');
        displayError(config, error.message);
    } finally {
        showLoading(false);
    }
}

// Run All Agents
async function runAllAgents() {
    if (!uploadedFileName) {
        showAlert('Please upload a file first.', 'warning');
        return;
    }

    const agents = ['cleaner', 'profiler', 'reasoner', 'langextract'];
    
    for (const agent of agents) {
        await runAgent(agent);
        // Small delay between agents
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
}

// Display Results
function displayResult(config, result, agentType) {
    const resultCard = document.createElement('div');
    resultCard.className = 'result-card';
    
    const timestamp = new Date().toLocaleTimeString();
    const status = result.status === 'success' ? 'success' : 'danger';
    
    resultCard.innerHTML = `
        <div class="d-flex justify-content-between align-items-start mb-3">
            <div class="d-flex align-items-center">
                <div class="agent-icon bg-${config.color}">
                    <i class="${config.icon}"></i>
                </div>
                <div>
                    <h5 class="mb-1">${config.name}</h5>
                    <small class="text-muted">${timestamp}</small>
                </div>
            </div>
            <span class="status-badge bg-${status} text-white">${result.status}</span>
        </div>
        
        <div class="result-content">
            ${formatAgentResult(agentType, result)}
        </div>
        
        <div class="mt-3">
            <button class="btn btn-outline-secondary btn-sm" onclick="toggleRawData(this)">
                <i class="fas fa-code me-1"></i>
                View Raw Data
            </button>
        </div>
        
        <div class="raw-data mt-3" style="display: none;">
            <pre>${JSON.stringify(result, null, 2)}</pre>
        </div>
    `;
    
    // Insert at the beginning of results container
    const existingContent = resultsContainer.innerHTML;
    if (existingContent.includes('Upload a file')) {
        resultsContainer.innerHTML = '';
    }
    resultsContainer.insertBefore(resultCard, resultsContainer.firstChild);
}

// Display Error
function displayError(config, errorMessage) {
    const errorCard = document.createElement('div');
    errorCard.className = 'result-card border-danger';
    
    const timestamp = new Date().toLocaleTimeString();
    
    errorCard.innerHTML = `
        <div class="d-flex justify-content-between align-items-start mb-3">
            <div class="d-flex align-items-center">
                <div class="agent-icon bg-${config.color}">
                    <i class="${config.icon}"></i>
                </div>
                <div>
                    <h5 class="mb-1">${config.name}</h5>
                    <small class="text-muted">${timestamp}</small>
                </div>
            </div>
            <span class="status-badge bg-danger text-white">Error</span>
        </div>
        
        <div class="alert alert-danger mb-0">
            <i class="fas fa-exclamation-triangle me-2"></i>
            <strong>Execution Failed:</strong> ${errorMessage}
        </div>
    `;
    
    const existingContent = resultsContainer.innerHTML;
    if (existingContent.includes('Upload a file')) {
        resultsContainer.innerHTML = '';
    }
    resultsContainer.insertBefore(errorCard, resultsContainer.firstChild);
}

// Format Agent-Specific Results
function formatAgentResult(agentType, result) {
    if (result.status !== 'success') {
        return `<div class="alert alert-danger">
            <i class="fas fa-exclamation-triangle me-2"></i>
            Execution failed: ${result.error || 'Unknown error'}
        </div>`;
    }

    const data = result.result || result;

    switch (agentType) {
        case 'cleaner':
            return formatCleanerResult(data);
        case 'profiler':
            return formatProfilerResult(data);
        case 'reasoner':
            return formatReasonerResult(data);
        case 'langextract':
            return formatLanguageResult(data);
        default:
            return `<pre class="small">${JSON.stringify(data, null, 2)}</pre>`;
    }
}

// Format Cleaner Results
function formatCleanerResult(data) {
    return `
        <div class="row">
            <div class="col-md-6">
                <h6><i class="fas fa-table me-2"></i>Data Shape</h6>
                <p><strong>Original:</strong> ${data.original_shape ? data.original_shape.join(' × ') : 'N/A'}</p>
                <p><strong>Cleaned:</strong> ${data.cleaned_shape ? data.cleaned_shape.join(' × ') : 'N/A'}</p>
                <p><strong>Rows Removed:</strong> ${data.rows_removed || 0}</p>
            </div>
            <div class="col-md-6">
                <h6><i class="fas fa-exclamation-circle me-2"></i>Data Quality</h6>
                <p><strong>Missing Values (Original):</strong> ${data.missing_values_original || 0}</p>
                <p><strong>Missing Values (Cleaned):</strong> ${data.missing_values_cleaned || 0}</p>
                ${data.output_file ? `<p><strong>Output File:</strong> ${data.output_file.split('/').pop()}</p>` : ''}
            </div>
        </div>
        ${data.data_types ? `
        <h6><i class="fas fa-list me-2"></i>Column Types</h6>
        <div class="row">
            ${Object.entries(data.data_types).map(([col, type]) => 
                `<div class="col-md-3"><small><strong>${col}:</strong> ${type}</small></div>`
            ).join('')}
        </div>` : ''}
    `;
}

// Format Profiler Results
function formatProfilerResult(data) {
    const basicInfo = data.basic_info || {};
    const dataQuality = data.data_quality || {};
    
    return `
        <div class="row">
            <div class="col-md-4">
                <h6><i class="fas fa-info-circle me-2"></i>Basic Info</h6>
                <p><strong>Rows:</strong> ${basicInfo.total_rows || 'N/A'}</p>
                <p><strong>Columns:</strong> ${basicInfo.total_columns || 'N/A'}</p>
                <p><strong>Memory:</strong> ${basicInfo.memory_usage_mb ? basicInfo.memory_usage_mb.toFixed(3) + ' MB' : 'N/A'}</p>
            </div>
            <div class="col-md-4">
                <h6><i class="fas fa-check-circle me-2"></i>Data Quality</h6>
                <p><strong>Overall Score:</strong> ${dataQuality.overall_score || 'N/A'}/100</p>
                ${dataQuality.completeness ? `<p><strong>Completeness:</strong> ${dataQuality.completeness.toFixed(1)}%</p>` : ''}
                ${dataQuality.uniqueness ? `<p><strong>Uniqueness:</strong> ${dataQuality.uniqueness.toFixed(1)}%</p>` : ''}
            </div>
            <div class="col-md-4">
                <h6><i class="fas fa-lightbulb me-2"></i>Recommendations</h6>
                ${data.recommendations && data.recommendations.length > 0 ? 
                    data.recommendations.slice(0, 3).map(rec => `<p class="small">• ${rec}</p>`).join('') :
                    '<p class="small text-muted">No specific recommendations</p>'
                }
            </div>
        </div>
    `;
}

// Format Reasoner Results
function formatReasonerResult(data) {
    const insights = data.insights || [];
    const patterns = data.patterns || [];
    const anomalies = data.anomalies || [];
    
    return `
        <div class="row">
            <div class="col-md-4">
                <h6><i class="fas fa-lightbulb me-2"></i>Key Insights</h6>
                ${insights.length > 0 ? 
                    insights.slice(0, 3).map(insight => `<p class="small">• ${insight}</p>`).join('') :
                    '<p class="small text-muted">No insights found</p>'
                }
            </div>
            <div class="col-md-4">
                <h6><i class="fas fa-search me-2"></i>Patterns Detected</h6>
                ${patterns.length > 0 ? 
                    patterns.slice(0, 3).map(pattern => `<p class="small">• ${pattern}</p>`).join('') :
                    '<p class="small text-muted">No patterns detected</p>'
                }
            </div>
            <div class="col-md-4">
                <h6><i class="fas fa-exclamation-triangle me-2"></i>Anomalies</h6>
                ${anomalies.length > 0 ? 
                    anomalies.slice(0, 3).map(anomaly => `<p class="small">• ${anomaly}</p>`).join('') :
                    '<p class="small text-muted">No anomalies detected</p>'
                }
            </div>
        </div>
        ${data.summary ? `
        <div class="mt-3">
            <h6><i class="fas fa-file-alt me-2"></i>Summary</h6>
            <p class="small">${data.summary}</p>
        </div>` : ''}
    `;
}

// Format Language Results
function formatLanguageResult(data) {
    const langSummary = data.language_summary || {};
    const culturalContext = data.cultural_context || {};
    const textColumns = data.text_columns || [];
    
    return `
        <div class="row">
            <div class="col-md-4">
                <h6><i class="fas fa-globe me-2"></i>Language Analysis</h6>
                <p><strong>Primary Language:</strong> ${langSummary.primary_language || 'Unknown'}</p>
                <p><strong>Confidence:</strong> ${langSummary.confidence ? (langSummary.confidence * 100).toFixed(1) + '%' : 'N/A'}</p>
                <p><strong>Text Columns:</strong> ${textColumns.length > 0 ? textColumns.join(', ') : 'None found'}</p>
            </div>
            <div class="col-md-4">
                <h6><i class="fas fa-chart-pie me-2"></i>Language Distribution</h6>
                ${langSummary.language_distribution ? 
                    Object.entries(langSummary.language_distribution)
                        .slice(0, 4)
                        .map(([lang, score]) => `<p class="small">${lang}: ${(score * 100).toFixed(1)}%</p>`)
                        .join('') :
                    '<p class="small text-muted">No distribution data</p>'
                }
            </div>
            <div class="col-md-4">
                <h6><i class="fas fa-culture me-2"></i>Cultural Context</h6>
                ${Object.keys(culturalContext).length > 0 ? 
                    Object.entries(culturalContext)
                        .slice(0, 4)
                        .map(([key, value]) => `<p class="small">${key.replace('_', ' ')}: ${value}</p>`)
                        .join('') :
                    '<p class="small text-muted">No cultural context found</p>'
                }
            </div>
        </div>
        ${data.keywords && data.keywords.length > 0 ? `
        <div class="mt-3">
            <h6><i class="fas fa-tags me-2"></i>Keywords Found</h6>
            <div class="d-flex flex-wrap gap-1">
                ${data.keywords.slice(0, 10).map(keyword => 
                    `<span class="badge bg-secondary">${keyword}</span>`
                ).join('')}
            </div>
        </div>` : ''}
    `;
}

// Toggle Raw Data
function toggleRawData(button) {
    const rawDataDiv = button.parentElement.nextElementSibling;
    if (rawDataDiv.style.display === 'none') {
        rawDataDiv.style.display = 'block';
        button.innerHTML = '<i class="fas fa-eye-slash me-1"></i>Hide Raw Data';
    } else {
        rawDataDiv.style.display = 'none';
        button.innerHTML = '<i class="fas fa-code me-1"></i>View Raw Data';
    }
}

// Clear Results
function clearResults() {
    resultsContainer.innerHTML = `
        <div class="text-center text-muted py-5">
            <i class="fas fa-robot fa-3x mb-3"></i>
            <p>Upload a file and run an AI agent to see results here</p>
        </div>
    `;
}

// Show Loading
function showLoading(show) {
    if (show) {
        loadingIndicator.classList.add('show');
    } else {
        loadingIndicator.classList.remove('show');
    }
}

// Show Alert
function showAlert(message, type) {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert-toast');
    existingAlerts.forEach(alert => alert.remove());
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show alert-toast position-fixed`;
    alert.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alert);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alert.parentElement) {
            alert.remove();
        }
    }, 5000);
}

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    // Initially disable agent buttons
    agentButtons.forEach(btn => {
        btn.disabled = true;
        btn.classList.add('opacity-50');
    });
    runAllButton.disabled = true;
    runAllButton.classList.add('opacity-50');
    
    // Check API connectivity
    fetch(`${API_BASE_URL}/api/health`)
        .then(response => response.json())
        .then(data => {
            showAlert('✅ Connected to API server successfully!', 'success');
        })
        .catch(error => {
            showAlert('❌ Cannot connect to API server. Make sure it\'s running on http://localhost:5000', 'danger');
        });
});
