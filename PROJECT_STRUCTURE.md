# 📁 Project Structure

```
cctv_analyzer/
│
├── 📄 app.py                          # Main Streamlit application
│   └── Core features:
│       ├── Video upload interface
│       ├── Frame extraction (OpenCV)
│       ├── Gemini 2.0 Flash integration
│       ├── Log generation & storage
│       └── Search functionality
│
├── 📄 requirements.txt                # Python dependencies
│   ├── streamlit==1.31.0
│   ├── opencv-python==4.9.0.80
│   ├── google-generativeai==0.3.2
│   ├── pillow==10.2.0
│   └── numpy==1.26.3
│
├── 📄 README.md                       # Complete documentation
│   ├── Features overview
│   ├── Installation guide
│   ├── Usage instructions
│   ├── Production migration path
│   ├── Cost estimation
│   └── Troubleshooting
│
├── 📄 DEMO_GUIDE.md                   # Presentation guide
│   ├── Demo script (15 min)
│   ├── Key talking points
│   ├── Q&A preparation
│   ├── Metrics to highlight
│   └── Follow-up strategy
│
├── 📄 production_architecture.py      # Production code examples
│   ├── Cloud Run API endpoints
│   ├── Firestore data structure
│   ├── React frontend examples
│   ├── Cost optimization strategies
│   └── Scaling configurations
│
├── 🔧 setup.sh                        # Linux/Mac setup script
│   ├── Python version check
│   ├── Virtual environment creation
│   ├── Dependency installation
│   └── Auto-launch option
│
├── 🔧 setup.bat                       # Windows setup script
│   └── Same features as setup.sh
│
└── 📁 output/                         # Generated files (created at runtime)
    ├── logs_YYYYMMDD_HHMMSS.json     # Exported log files
    └── frames/                        # Temporary frame storage
```

## 🎯 Quick Start

### For Linux/Mac:
```bash
chmod +x setup.sh
./setup.sh
```

### For Windows:
```cmd
setup.bat
```

### Manual Setup:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📚 Documentation Overview

### 1. README.md
- **Audience**: Developers & technical users
- **Purpose**: Complete setup and usage guide
- **Key Sections**:
  - Quick start guide
  - Feature descriptions
  - API key setup
  - Production migration path
  - Cost analysis
  - Troubleshooting tips

### 2. DEMO_GUIDE.md
- **Audience**: You (for presentation)
- **Purpose**: Step-by-step demo script
- **Key Sections**:
  - 15-minute demo flow
  - Talking points
  - Q&A preparation
  - Metrics to highlight
  - Follow-up strategy

### 3. production_architecture.py
- **Audience**: Google team & engineers
- **Purpose**: Show production scalability
- **Key Sections**:
  - Cloud Run API examples
  - Database schema
  - Frontend code samples
  - Cost optimization
  - Scaling strategies

## 🔑 Key Files Explained

### app.py
The heart of the application. Contains:

**CCTVAnalyzer Class:**
- `extract_frames()` - Extracts video frames at intervals
- `analyze_frame()` - Sends frames to Gemini 2.0 Flash
- `extract_entities()` - Extracts keywords from descriptions
- `process_video()` - Complete pipeline orchestration
- `save_logs()` - Exports logs to JSON
- `search_logs()` - Text-based search functionality

**Streamlit UI:**
- Upload & Process tab - Video upload and analysis
- Search Logs tab - Event search interface
- View All Logs tab - Complete log viewer with export

### requirements.txt
Minimal dependencies for the prototype:
- **streamlit**: Web interface framework
- **opencv-python**: Video processing and frame extraction
- **google-generativeai**: Gemini 2.0 Flash API client
- **pillow**: Image processing
- **numpy**: Array operations

## 🚀 Usage Flow

```
1. User starts app
   └── streamlit run app.py
   
2. User configures settings
   ├── Enter API key
   └── Set frame interval
   
3. User uploads video
   └── Supported: MP4, AVI, MOV, MKV
   
4. System processes video
   ├── Extract frames (OpenCV)
   ├── Analyze frames (Gemini 2.0)
   ├── Generate logs (JSON)
   └── Display results (Streamlit)
   
5. User searches logs
   ├── Enter search query
   ├── View matching frames
   └── Get timestamps
   
6. User exports data
   └── Download JSON logs
```

## 📊 Data Flow

```
Video File
    ↓
Frame Extraction (every 5 seconds)
    ↓
PIL Image Conversion
    ↓
Gemini 2.0 Flash API
    ↓
Text Description + Entity Extraction
    ↓
Structured Log Entry (JSON)
    ↓
In-Memory Storage (session_state)
    ↓
Search Interface / Export
```

## 🎨 UI Structure

```
Sidebar:
├── API Key Input
├── Frame Interval Slider
└── Processing Stats

Main Area:
├── Tab 1: Upload & Process
│   ├── File Uploader
│   ├── Start Analysis Button
│   ├── Progress Bar
│   └── Sample Results
│
├── Tab 2: Search Logs
│   ├── Search Input
│   ├── Results Display
│   └── Timestamp Links
│
└── Tab 3: View All Logs
    ├── Export Button
    └── Complete Log List
```

## 🔧 Customization Points

### Change Frame Interval
```python
# In app.py, line ~50
frame_interval = st.slider("Frame Interval", 1, 10, 5)
```

### Modify Gemini Prompt
```python
# In app.py, analyze_frame() method
prompt = """Your custom prompt here..."""
```

### Add Entity Categories
```python
# In app.py, extract_entities() method
keywords = {
    'person': [...],
    'vehicle': [...],
    'your_category': ['keyword1', 'keyword2']
}
```

### Change Output Directory
```python
# In app.py, CCTVAnalyzer.__init__()
self.output_dir = Path("your_custom_path")
```

## 📦 Dependencies Explained

### Core Dependencies
- **streamlit**: Powers the web interface
  - Why: Fast prototyping, built-in components
  - Alternative for production: React/Angular

- **opencv-python**: Video processing
  - Why: Industry standard, robust
  - Used for: Frame extraction, video metadata

- **google-generativeai**: Gemini API client
  - Why: Official Google SDK
  - Used for: All AI analysis

- **pillow**: Image manipulation
  - Why: Required for Gemini image input
  - Used for: Format conversion

- **numpy**: Numerical operations
  - Why: OpenCV dependency
  - Used for: Array operations

### No Additional Dependencies Needed
The project intentionally uses minimal dependencies to:
- ✅ Reduce installation complexity
- ✅ Minimize version conflicts
- ✅ Keep the prototype lightweight
- ✅ Ensure cross-platform compatibility

## 🎓 Learning Resources

### To Understand the Code
1. **Streamlit Docs**: https://docs.streamlit.io/
2. **OpenCV Tutorial**: https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
3. **Gemini API Docs**: https://ai.google.dev/docs
4. **Python PIL Guide**: https://pillow.readthedocs.io/

### To Extend the Project
1. **Cloud Run Tutorial**: https://cloud.google.com/run/docs
2. **Firestore Guide**: https://firebase.google.com/docs/firestore
3. **React Basics**: https://react.dev/learn
4. **Vertex AI Docs**: https://cloud.google.com/vertex-ai/docs

## 🐛 Common Issues & Solutions

### Issue: "ModuleNotFoundError"
**Solution**: 
```bash
pip install -r requirements.txt
```

### Issue: "API Key Invalid"
**Solution**: 
1. Get new key from https://aistudio.google.com/
2. Make sure no extra spaces in the input

### Issue: "Video Won't Upload"
**Solution**:
1. Check file format (MP4, AVI, MOV, MKV)
2. Reduce file size (< 200MB recommended)
3. Try converting with FFmpeg

### Issue: "Slow Processing"
**Solution**:
1. Increase frame interval (10s instead of 5s)
2. Use shorter video clips for testing
3. Check internet speed

## 📈 Next Steps

### Phase 1: Prototype (Current)
✅ Working Streamlit app
✅ Gemini 2.0 Flash integration
✅ Basic search functionality
✅ JSON export

### Phase 2: Enhanced Prototype (1-2 weeks)
- [ ] Add semantic search (embeddings)
- [ ] Implement confidence scoring
- [ ] Add video preview in results
- [ ] Multi-video support
- [ ] User authentication

### Phase 3: Production MVP (1-2 months)
- [ ] Cloud Run deployment
- [ ] Firestore integration
- [ ] React frontend
- [ ] Async processing
- [ ] Real-time updates
- [ ] Admin dashboard

### Phase 4: Full Production (3-6 months)
- [ ] Multi-tenant support
- [ ] Advanced analytics
- [ ] Custom event detection
- [ ] Mobile apps
- [ ] Enterprise features
- [ ] SOC2 compliance

## 💡 Tips for Demo

1. **Practice First**: Run through the demo 3-5 times
2. **Prepare Backups**: Have multiple sample videos ready
3. **Check Internet**: Ensure stable connection for API calls
4. **Time Management**: Keep to 15 minutes max
5. **Be Enthusiastic**: Show your passion for the solution
6. **Focus on Value**: Emphasize business benefits, not just tech
7. **Handle Questions Well**: It's okay to say "I'll look into that"
8. **Follow Up**: Send materials within 24 hours

## 📞 Support

For questions or issues:
1. Check README.md troubleshooting section
2. Review DEMO_GUIDE.md for presentation tips
3. Examine production_architecture.py for scaling questions
4. Refer to Google AI Studio documentation

Good luck with your demo! 🚀
