# Production Architecture - Cloud Run API Example
# This shows how the prototype would be structured for production scale

"""
PRODUCTION ARCHITECTURE OVERVIEW
================================

1. USER UPLOADS VIDEO
   ↓
2. CLOUD STORAGE (video stored)
   ↓
3. CLOUD TASKS (queues processing job)
   ↓
4. CLOUD RUN (processes video asynchronously)
   ↓
5. GEMINI 2.0 FLASH (analyzes frames)
   ↓
6. FIRESTORE (stores logs)
   ↓
7. VERTEX AI MATCHING ENGINE (semantic search)
   ↓
8. WEB APP (user searches and views results)
"""

# ==============================================================================
# Example Cloud Run Endpoint (Flask/FastAPI)
# ==============================================================================

from flask import Flask, request, jsonify
from google.cloud import storage, firestore, tasks_v2
import google.generativeai as genai
import cv2
import tempfile
from datetime import datetime

app = Flask(__name__)

# Initialize clients
storage_client = storage.Client()
db = firestore.Client()
tasks_client = tasks_v2.CloudTasksClient()

# Configure Gemini
genai.configure(api_key="YOUR_API_KEY")  # In production: use Secret Manager
model = genai.GenerativeModel('gemini-2.0-flash-exp')

@app.route('/api/upload-video', methods=['POST'])
def upload_video():
    """
    Endpoint: Upload video and queue for processing
    
    Production features:
    - Upload to Cloud Storage
    - Create processing task
    - Return job ID for tracking
    """
    file = request.files['video']
    user_id = request.form.get('user_id')
    
    # Upload to Cloud Storage
    bucket = storage_client.bucket('cctv-videos')
    blob = bucket.blob(f'{user_id}/{datetime.now().isoformat()}/{file.filename}')
    blob.upload_from_file(file)
    
    video_url = blob.public_url
    
    # Create processing task (async)
    task = {
        'video_url': video_url,
        'user_id': user_id,
        'frame_interval': request.form.get('frame_interval', 5)
    }
    
    # Queue processing job
    parent = tasks_client.queue_path('PROJECT_ID', 'LOCATION', 'video-processing-queue')
    task_config = {
        'http_request': {
            'http_method': tasks_v2.HttpMethod.POST,
            'url': 'https://your-cloud-run-url.run.app/api/process-video',
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(task).encode()
        }
    }
    
    response = tasks_client.create_task(request={'parent': parent, 'task': task_config})
    
    return jsonify({
        'job_id': response.name,
        'status': 'queued',
        'video_url': video_url
    }), 202


@app.route('/api/process-video', methods=['POST'])
def process_video():
    """
    Endpoint: Process video (called by Cloud Tasks)
    
    Production features:
    - Downloads video from Cloud Storage
    - Extracts frames
    - Analyzes with Gemini
    - Stores logs in Firestore
    - Updates job status
    """
    data = request.json
    video_url = data['video_url']
    user_id = data['user_id']
    frame_interval = int(data['frame_interval'])
    
    # Download video to temp location
    with tempfile.NamedTemporaryFile(suffix='.mp4') as temp_file:
        blob = storage_client.bucket('cctv-videos').blob(video_url.split('/')[-1])
        blob.download_to_filename(temp_file.name)
        
        # Extract frames
        frames = extract_frames(temp_file.name, frame_interval)
        
        # Analyze each frame
        logs = []
        for frame_data in frames:
            log_entry = analyze_frame_production(frame_data)
            logs.append(log_entry)
            
            # Store in Firestore immediately
            db.collection('users').document(user_id).collection('logs').add(log_entry)
        
        # Update job status
        db.collection('jobs').document(data['job_id']).update({
            'status': 'completed',
            'total_frames': len(frames),
            'completed_at': datetime.now()
        })
    
    return jsonify({'status': 'completed', 'frames_processed': len(logs)}), 200


@app.route('/api/search', methods=['POST'])
def search_logs():
    """
    Endpoint: Search logs using Vertex AI Matching Engine
    
    Production features:
    - Semantic search (not just keyword)
    - Finds similar events even with different wording
    - Fast search across millions of logs
    """
    data = request.json
    query = data['query']
    user_id = data['user_id']
    
    # In production: Use Vertex AI Matching Engine for semantic search
    # This is a simplified version showing Firestore query
    
    logs_ref = db.collection('users').document(user_id).collection('logs')
    
    # Simple text search (in production: use embedding-based search)
    results = []
    docs = logs_ref.stream()
    
    for doc in docs:
        log = doc.to_dict()
        if query.lower() in log['description'].lower():
            results.append(log)
    
    return jsonify({
        'results': results,
        'total': len(results)
    }), 200


@app.route('/api/job-status/<job_id>', methods=['GET'])
def job_status(job_id):
    """
    Endpoint: Check processing job status
    
    Allows frontend to poll for completion
    """
    job_doc = db.collection('jobs').document(job_id).get()
    
    if job_doc.exists:
        return jsonify(job_doc.to_dict()), 200
    else:
        return jsonify({'error': 'Job not found'}), 404


# Helper functions (same as prototype but optimized)
def extract_frames(video_path, frame_interval):
    """Extract frames - same logic as prototype"""
    # Implementation here...
    pass


def analyze_frame_production(frame_data):
    """
    Analyze frame with production optimizations
    
    Production enhancements:
    - Batch processing
    - Retry logic
    - Error handling
    - Rate limiting
    """
    try:
        # Same Gemini call as prototype
        response = model.generate_content([prompt, frame_data['image']])
        
        return {
            'timestamp': frame_data['timestamp'],
            'description': response.text,
            'entities': extract_entities(response.text),
            'analyzed_at': datetime.now().isoformat()
        }
    except Exception as e:
        # Production: Log error, retry, or mark for manual review
        return {
            'timestamp': frame_data['timestamp'],
            'description': f'Error: {str(e)}',
            'status': 'failed'
        }


# ==============================================================================
# Example Firestore Data Structure
# ==============================================================================

"""
FIRESTORE COLLECTIONS:

/users/{user_id}/
    ├── videos/{video_id}
    │   ├── filename: "camera1_20241004.mp4"
    │   ├── uploaded_at: timestamp
    │   ├── duration: 3600
    │   └── status: "processed"
    │
    └── logs/{log_id}
        ├── video_id: "abc123"
        ├── timestamp: "00:05:23"
        ├── timestamp_seconds: 323
        ├── description: "Two people entering..."
        ├── entities: ["person", "door"]
        └── analyzed_at: timestamp

/jobs/{job_id}
    ├── user_id: "user123"
    ├── video_url: "gs://bucket/video.mp4"
    ├── status: "processing" | "completed" | "failed"
    ├── total_frames: 720
    └── created_at: timestamp
"""


# ==============================================================================
# Example React Frontend Component
# ==============================================================================

"""
// Frontend: Video Upload Component (React)

import React, { useState } from 'react';
import axios from 'axios';

function VideoUploader() {
    const [file, setFile] = useState(null);
    const [jobId, setJobId] = useState(null);
    const [status, setStatus] = useState('idle');

    const uploadVideo = async () => {
        const formData = new FormData();
        formData.append('video', file);
        formData.append('user_id', getCurrentUserId());
        formData.append('frame_interval', 5);

        setStatus('uploading');

        try {
            const response = await axios.post('/api/upload-video', formData);
            setJobId(response.data.job_id);
            setStatus('processing');
            
            // Poll for completion
            pollJobStatus(response.data.job_id);
        } catch (error) {
            setStatus('error');
        }
    };

    const pollJobStatus = async (jobId) => {
        const interval = setInterval(async () => {
            const response = await axios.get(`/api/job-status/${jobId}`);
            
            if (response.data.status === 'completed') {
                setStatus('completed');
                clearInterval(interval);
            }
        }, 5000);
    };

    return (
        <div>
            <input type="file" onChange={(e) => setFile(e.target.files[0])} />
            <button onClick={uploadVideo}>Upload & Process</button>
            <p>Status: {status}</p>
        </div>
    );
}
"""


# ==============================================================================
# Cost Optimization Strategies
# ==============================================================================

"""
1. SMART FRAME EXTRACTION
   - Use motion detection to skip static frames
   - Increase interval during night/low-activity periods
   - Example: 5s during day, 30s at night = 70% cost reduction

2. BATCH PROCESSING
   - Process multiple frames in single API call
   - Use Gemini's batch API when available
   - Estimated savings: 20-30%

3. CACHING & DEDUPLICATION
   - Hash similar frames, don't reprocess
   - Cache common scene descriptions
   - Estimated savings: 15-25%

4. TIERED PROCESSING
   - Quick scan (30s intervals) initially
   - Detailed analysis (5s) only for flagged periods
   - Estimated savings: 50-60% for typical footage

EXAMPLE COST FOR 10 CAMERAS (24/7):
- Without optimization: ~$1,500-3,000/month
- With optimizations: ~$450-900/month
"""


# ==============================================================================
# Scaling Configuration
# ==============================================================================

"""
CLOUD RUN CONFIGURATION:

resources:
  limits:
    cpu: '2'
    memory: 4Gi
  
autoscaling:
  minInstances: 1
  maxInstances: 100
  targetConcurrency: 10

# Handles 100-2000 concurrent users
# Scales automatically based on load
# Cost: ~$0.00001 per second of compute

CLOUD TASKS CONFIGURATION:

rate_limits:
  max_dispatches_per_second: 500
  max_concurrent_dispatches: 1000

# Ensures smooth processing
# Prevents API rate limit hits
# Automatic retry on failures
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
