# 🎥 CCTV Footage Analyzer - Gemini 2.0 Prototype

AI-powered CCTV footage analysis using Google's Gemini 2.0 Flash. This prototype demonstrates automated video analysis, log generation, and event search capabilities.

## 🌟 Features

- **Automated Frame Extraction**: Extract frames at customizable intervals (default: 5 seconds)
- **AI-Powered Analysis**: Gemini 2.0 Flash analyzes each frame and generates detailed descriptions
- **Structured Logging**: Creates timestamped logs in JSON format
- **Text-Based Search**: Find specific events by searching through descriptions
- **Professional UI**: Clean Streamlit interface for demos and presentations
- **Export Functionality**: Download logs as JSON for further processing

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Google AI Studio API key (free tier available)

### 2. Get Your API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key"
4. Copy your API key

### 3. Installation

```bash
# Clone or download this repository
cd cctv_analyzer

# Install dependencies
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 How to Use

### Step 1: Configure
1. Enter your Google AI Studio API key in the sidebar
2. Adjust frame interval if needed (default: 5 seconds)

### Step 2: Upload & Process
1. Go to the "Upload & Process" tab
2. Upload your CCTV video file (MP4, AVI, MOV, MKV)
3. Click "Start Analysis"
4. Wait for processing to complete

### Step 3: Search Events
1. Go to the "Search Logs" tab
2. Enter search queries like:
   - "person entering"
   - "car parking"
   - "door opening"
   - "people walking"
3. View matching frames with timestamps

### Step 4: Export Logs
1. Go to "View All Logs" tab
2. Click "Export JSON" to download structured logs
3. Use logs for further analysis or integration

## 📊 Output Format

Each log entry contains:

```json
{
  "timestamp": "00:00:05",
  "timestamp_seconds": 5.0,
  "frame_number": 150,
  "description": "Two people entering through main entrance. One person wearing blue jacket, another in red shirt. Both walking towards the reception area.",
  "entities": ["person", "door", "activity"],
  "analyzed_at": "2024-10-04T14:23:45.123456"
}
```

## 🎯 Use Cases

- **Security Monitoring**: Search for specific events in hours of footage
- **Incident Investigation**: Find exact timestamps of events
- **Traffic Analysis**: Track vehicle movements
- **Access Control**: Monitor entry/exit events
- **Business Analytics**: Analyze customer behavior

## 🏗️ Architecture

```
Video Upload → Frame Extraction → Gemini 2.0 Analysis → Structured Logs → Search Interface
                (OpenCV)              (AI Studio)         (JSON)           (Text Search)
```

## 🚀 Production Migration Path

This prototype is designed for easy migration to production scale (100-2000 users):

### Current (Prototype)
- **Frontend**: Streamlit
- **Processing**: Local/synchronous
- **Storage**: Local JSON files
- **Search**: Text-based keyword search

### Production Scale
- **Frontend**: React/Angular/Vue web app
- **Backend**: Cloud Run + Cloud Functions
- **Queue**: Cloud Tasks or Pub/Sub for async processing
- **Storage**: 
  - Videos: Cloud Storage
  - Logs: Firestore or BigQuery
- **Search**: Vertex AI Matching Engine (semantic search)
- **Auth**: Firebase Authentication
- **Monitoring**: Cloud Logging + Cloud Monitoring

### Migration Components

The code is structured for easy migration:

```python
# Current: Direct Gemini call
response = self.model.generate_content([prompt, pil_image])

# Production: Would be Cloud Run endpoint
# POST /api/analyze-frame
# Request: {video_id, frame_data}
# Response: {log_entry}
```

## 💰 Cost Estimation (Production)

### Gemini 2.0 Flash Pricing
- Input: ~$0.075 per 1M tokens
- Output: ~$0.30 per 1M tokens

### Example: 24-hour CCTV footage
- Frames at 5-sec interval: 17,280 frames
- Estimated cost: ~$5-10 per 24 hours
- Monthly (30 days): ~$150-300 per camera

### Optimization strategies:
1. Increase frame interval during low-activity periods
2. Use motion detection to trigger analysis
3. Batch processing during off-peak hours
4. Cache similar frames

## 🔧 Customization

### Adjust Frame Interval
Change in UI or modify the default:
```python
frame_interval = st.slider("Frame Interval (seconds)", 1, 10, 5)
```

### Customize Gemini Prompt
Edit the prompt in `analyze_frame()` method:
```python
prompt = """Your custom analysis instructions here..."""
```

### Add More Entity Types
Extend the `extract_entities()` method:
```python
keywords = {
    'person': [...],
    'vehicle': [...],
    'animal': ['dog', 'cat', 'bird'],  # Add new category
    # ... more categories
}
```

## 📝 Sample Queries

Try these search queries:
- "person wearing blue"
- "car entering"
- "multiple people"
- "door opening"
- "parking"
- "running"
- "unusual activity"

## 🐛 Troubleshooting

### Video Won't Upload
- Check file format (MP4, AVI, MOV, MKV)
- Ensure file size < 200MB for smooth processing
- Try converting with FFmpeg if needed

### API Rate Limit Errors
- The app includes 0.5s delay between requests
- Free tier: 1,500 requests/day
- Reduce frame interval for longer videos

### Processing Takes Too Long
- Reduce frame interval (e.g., 10 seconds instead of 5)
- Use shorter video clips for testing
- Check internet connection speed

## 📧 Demo Tips for Google Team

### Preparation
1. Use a 2-5 minute sample CCTV clip
2. Prepare specific search queries beforehand
3. Show the JSON export functionality
4. Explain the production migration path

### Key Points to Highlight
✅ Real-time AI analysis of surveillance footage  
✅ Searchable event logs with timestamps  
✅ Scalable architecture using Google Cloud services  
✅ Cost-effective with Gemini 2.0 Flash  
✅ Easy integration with existing security systems  

### Demo Flow
1. **Introduction** (2 min): Explain the problem and solution
2. **Upload & Process** (3 min): Show video analysis in action
3. **Search Demo** (2 min): Find specific events using text search
4. **Architecture** (3 min): Explain tech stack and scalability
5. **Q&A**: Be ready to discuss production deployment

## 🔗 Useful Links

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Vertex AI](https://cloud.google.com/vertex-ai)
- [Cloud Run](https://cloud.google.com/run)
- [Firestore](https://firebase.google.com/docs/firestore)

## 📄 License

This is a prototype for demonstration purposes.

## 🤝 Contributing

This is a demo project. For production deployment, consider:
- Adding unit tests
- Implementing proper error handling
- Adding authentication
- Setting up CI/CD pipelines
- Monitoring and logging

---

**Built with ❤️ using Google Gemini 2.0 Flash**
