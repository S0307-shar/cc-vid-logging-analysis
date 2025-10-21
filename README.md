# 🎥 CCTV Footage Analyzer - Gemini 2.0 Prototype

AI-powered CCTV footage analysis using Google's Gemini 2.0 Flash. This prototype demonstrates automated video analysis, log generation, and event search capabilities.

Access : https://ccvideologginganalysis.streamlit.app/

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


## 📄 License

This is a prototype for demonstration purposes.

## 🤝 Contributing

This is a demo project. 


