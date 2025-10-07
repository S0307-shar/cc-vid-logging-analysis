import streamlit as st
import cv2
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import google.generativeai as genai
from PIL import Image
import io
import time

# Page config
st.set_page_config(
    page_title="CCTV Footage Analyzer",
    page_icon="🎥",
    layout="wide"
)

# Initialize session state
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

class CCTVAnalyzer:
    def __init__(self, api_key, frame_interval=5):
        """
        Initialize CCTV Analyzer
        
        Args:
            api_key: Google AI Studio API key
            frame_interval: Extract frames every N seconds
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.frame_interval = frame_interval
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
    def extract_frames(self, video_path, progress_callback=None):
        """Extract frames from video at specified intervals"""
        frames = []
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError("Could not open video file")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps
        
        frame_interval_frames = int(fps * self.frame_interval)
        
        frame_count = 0
        extracted_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % frame_interval_frames == 0:
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                timestamp = frame_count / fps
                
                frames.append({
                    'frame': frame_rgb,
                    'timestamp': timestamp,
                    'frame_number': frame_count
                })
                
                extracted_count += 1
                
                if progress_callback:
                    progress = (frame_count / total_frames) * 100
                    progress_callback(progress, f"Extracted frame at {self.format_timestamp(timestamp)}")
            
            frame_count += 1
        
        cap.release()
        return frames, duration
    
    def format_timestamp(self, seconds):
        """Format seconds to HH:MM:SS"""
        td = timedelta(seconds=seconds)
        hours = td.seconds // 3600
        minutes = (td.seconds % 3600) // 60
        secs = td.seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def analyze_frame(self, frame_data):
        """Analyze a single frame using Gemini 2.0 Flash"""
        try:
            # Fix: Convert numpy array to PIL Image using cv2 encoding
            # This avoids PngImagePlugin issues
            import io
            
            # Encode frame to JPEG in memory
            success, buffer = cv2.imencode('.jpg', frame_data['frame'])
            if not success:
                raise ValueError("Failed to encode frame")
            
            # Convert to PIL Image from bytes
            pil_image = Image.open(io.BytesIO(buffer.tobytes()))
            
            prompt = """You are analyzing CCTV security footage. Describe what's happening in this frame in detail.

Include:
- Number and description of people (clothing, activities, positions)
- Vehicles (type, color, actions like parking/moving)
- Notable objects or activities
- Any unusual or significant events
- Overall scene context

Be concise but specific. Focus on security-relevant details."""

            response = self.model.generate_content([prompt, pil_image])
            description = response.text
            
            # Extract key entities (simple keyword extraction)
            entities = self.extract_entities(description)
            
            return {
                'timestamp': self.format_timestamp(frame_data['timestamp']),
                'timestamp_seconds': frame_data['timestamp'],
                'frame_number': frame_data['frame_number'],
                'description': description,
                'entities': entities,
                'analyzed_at': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error in analyze_frame: {str(e)}")  # Debug logging
            return {
                'timestamp': self.format_timestamp(frame_data['timestamp']),
                'timestamp_seconds': frame_data['timestamp'],
                'frame_number': frame_data['frame_number'],
                'description': f"Error analyzing frame: {str(e)}",
                'entities': [],
                'analyzed_at': datetime.now().isoformat()
            }
    
    def extract_entities(self, description):
        """Simple keyword extraction for entity recognition"""
        # This is a basic implementation - in production, you'd use NLP
        keywords = {
            'person': ['person', 'people', 'man', 'woman', 'individual', 'pedestrian'],
            'vehicle': ['car', 'vehicle', 'truck', 'bike', 'motorcycle', 'van'],
            'door': ['door', 'entrance', 'exit', 'gate'],
            'activity': ['walking', 'running', 'standing', 'sitting', 'entering', 'leaving']
        }
        
        entities = []
        description_lower = description.lower()
        
        for category, words in keywords.items():
            for word in words:
                if word in description_lower:
                    entities.append(category)
                    break
        
        return list(set(entities))
    
    def process_video(self, video_path, progress_callback=None):
        """Complete pipeline: extract frames and analyze"""
        logs = []
        
        # Extract frames
        if progress_callback:
            progress_callback(0, "Starting frame extraction...")
        
        frames, duration = self.extract_frames(video_path, progress_callback)
        
        total_frames = len(frames)
        
        # Analyze each frame
        for idx, frame_data in enumerate(frames):
            if progress_callback:
                progress = ((idx + 1) / total_frames) * 100
                progress_callback(progress, f"Analyzing frame {idx + 1}/{total_frames} at {self.format_timestamp(frame_data['timestamp'])}")
            
            log_entry = self.analyze_frame(frame_data)
            logs.append(log_entry)
            
            # Small delay to respect API rate limits
            time.sleep(0.5)
        
        # Save logs
        self.save_logs(logs)
        
        return logs
    
    def save_logs(self, logs):
        """Save logs to JSON file"""
        log_file = self.output_dir / f"logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        return log_file
    
    def search_logs(self, logs, query):
        """Search logs by text query"""
        query_lower = query.lower()
        results = []
        
        for log in logs:
            # Search in description
            if query_lower in log['description'].lower():
                results.append(log)
            # Search in entities
            elif any(query_lower in entity.lower() for entity in log.get('entities', [])):
                results.append(log)
        
        return results


# Streamlit UI
def main():
    st.title("🎥 CCTV Footage Analyzer")
    st.markdown("### AI-Powered Video Analysis with Gemini 2.0 Flash")
    
    st.markdown("""
    This prototype demonstrates how to analyze CCTV footage using Google's Gemini 2.0 Flash:
    - Extract frames every 5 seconds
    - Generate detailed descriptions using AI
    - Create searchable logs with timestamps
    - Find specific events instantly
    """)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        api_key = st.text_input(
            "Google AI Studio API Key",
            value=st.session_state.api_key,
            type="password",
            help="Get your free API key from https://aistudio.google.com/"
        )
        # Update session state
        st.session_state.api_key = api_key
        
        frame_interval = st.slider(
            "Frame Interval (seconds)",
            min_value=1,
            max_value=10,
            value=5,
            help="Extract and analyze frames every N seconds"
        )
        
        st.markdown("---")
        st.markdown("### 📊 Processing Stats")
        if st.session_state.logs:
            st.metric("Total Frames Analyzed", len(st.session_state.logs))
            st.metric("Total Duration", 
                     f"{max([log['timestamp_seconds'] for log in st.session_state.logs]):.1f}s")
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📹 Upload & Process", "🔍 Search Logs", "📄 View All Logs"])
    
    with tab1:
        st.header("Upload CCTV Footage")
        
        uploaded_file = st.file_uploader(
            "Choose a video file",
            type=['mp4', 'avi', 'mov', 'mkv'],
            help="Upload your CCTV footage for analysis"
        )
        
        if uploaded_file and api_key:
            # Save uploaded file temporarily
            temp_video_path = Path("temp_video.mp4")
            with open(temp_video_path, "wb") as f:
                f.write(uploaded_file.read())
            
            st.success(f"✅ Video uploaded: {uploaded_file.name}")
            
            if st.button("🚀 Start Analysis", type="primary"):
                try:
                    analyzer = CCTVAnalyzer(api_key, frame_interval)
                    
                    # Progress tracking
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    def update_progress(progress, message):
                        progress_bar.progress(int(progress))
                        status_text.text(message)
                    
                    # Process video
                    with st.spinner("Processing video..."):
                        logs = analyzer.process_video(str(temp_video_path), update_progress)
                    
                    st.session_state.logs = logs
                    st.session_state.processing_complete = True
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Processing complete!")
                    
                    st.success(f"🎉 Successfully analyzed {len(logs)} frames!")
                    
                    # Show sample results
                    st.subheader("Sample Results")
                    for i, log in enumerate(logs[:3]):
                        with st.expander(f"Frame at {log['timestamp']}"):
                            st.write(f"**Description:** {log['description']}")
                            st.write(f"**Entities:** {', '.join(log['entities']) if log['entities'] else 'None detected'}")
                    
                    # Cleanup
                    temp_video_path.unlink()
                    
                except Exception as e:
                    st.error(f"❌ Error processing video: {str(e)}")
                    if temp_video_path.exists():
                        temp_video_path.unlink()
        
        elif uploaded_file and not api_key:
            st.warning("⚠️ Please enter your Google AI Studio API key in the sidebar")
    
    with tab2:
        st.header("Search Logs")
        
        if not st.session_state.logs:
            st.info("👆 Process a video first to enable search functionality")
        else:
            search_query = st.text_input(
                "🔍 Search for events",
                placeholder="e.g., 'person entering', 'car parking', 'door opening'",
                help="Search through video descriptions and entities"
            )
            
            if search_query:
                analyzer = CCTVAnalyzer(api_key or "dummy", frame_interval)
                results = analyzer.search_logs(st.session_state.logs, search_query)
                
                st.subheader(f"Found {len(results)} matching frames")
                
                if results:
                    for result in results:
                        with st.expander(f"⏰ {result['timestamp']} - Frame #{result['frame_number']}"):
                            st.write(f"**Description:**")
                            st.write(result['description'])
                            st.write(f"**Entities:** {', '.join(result['entities']) if result['entities'] else 'None'}")
                            st.write(f"**Timestamp (seconds):** {result['timestamp_seconds']:.2f}s")
                else:
                    st.warning("No matching results found. Try a different query.")
    
    with tab3:
        st.header("All Logs")
        
        if not st.session_state.logs:
            st.info("👆 Process a video first to view logs")
        else:
            # Export option
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("📥 Export JSON"):
                    json_str = json.dumps(st.session_state.logs, indent=2)
                    st.download_button(
                        label="Download logs.json",
                        data=json_str,
                        file_name=f"cctv_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            
            # Display all logs
            for i, log in enumerate(st.session_state.logs):
                with st.expander(f"Frame {i+1}: {log['timestamp']}"):
                    st.write(f"**Timestamp:** {log['timestamp']} ({log['timestamp_seconds']:.2f}s)")
                    st.write(f"**Frame Number:** {log['frame_number']}")
                    st.write(f"**Description:**")
                    st.write(log['description'])
                    st.write(f"**Entities:** {', '.join(log['entities']) if log['entities'] else 'None'}")
                    st.write(f"**Analyzed at:** {log['analyzed_at']}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    ### 🚀 Production Migration Path
    This prototype demonstrates the core concept. For production with 100-2000 users:
    - **Backend**: Migrate to Cloud Run + Cloud Tasks for async processing
    - **Storage**: Use Firestore for logs, Cloud Storage for videos
    - **Search**: Implement Vertex AI Matching Engine for semantic search
    - **Frontend**: Build with React/Angular for better performance
    - **Auth**: Add Firebase Authentication
    """)

if __name__ == "__main__":
    main()