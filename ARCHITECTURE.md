# 🏗️ Architecture Diagrams

## Current Prototype Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│                    (Streamlit Web App)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │  Upload  │  │  Search  │  │  Export  │                 │
│  │   Tab    │  │   Tab    │  │   Tab    │                 │
│  └──────────┘  └──────────┘  └──────────┘                 │
└─────────────────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  PROCESSING LAYER                           │
│                (CCTVAnalyzer Class)                         │
│                                                             │
│  ┌─────────────┐    ┌──────────────┐   ┌──────────────┐  │
│  │   Frame     │ →  │   Gemini     │ → │    Log       │  │
│  │ Extraction  │    │  2.0 Flash   │   │  Generation  │  │
│  │  (OpenCV)   │    │   Analysis   │   │   (JSON)     │  │
│  └─────────────┘    └──────────────┘   └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                   STORAGE LAYER                             │
│                                                             │
│  ┌──────────────────┐        ┌──────────────────┐         │
│  │  Session State   │        │  Local JSON      │         │
│  │  (In-Memory)     │        │  Files           │         │
│  │  • Logs          │        │  • Exported Data │         │
│  │  • Status        │        │  • Backups       │         │
│  └──────────────────┘        └──────────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow - Prototype

```
1. VIDEO UPLOAD
   User uploads MP4/AVI/MOV
          ↓
2. FRAME EXTRACTION
   OpenCV extracts frames every 5s
          ↓
3. IMAGE PROCESSING
   Convert to PIL Image
          ↓
4. AI ANALYSIS
   Gemini 2.0 Flash API call
          ↓
5. DESCRIPTION GENERATION
   Natural language output
          ↓
6. ENTITY EXTRACTION
   Keyword extraction
          ↓
7. LOG CREATION
   JSON structure with timestamp
          ↓
8. STORAGE
   Store in session_state
          ↓
9. DISPLAY
   Show in UI / Enable search
          ↓
10. EXPORT
    Download as JSON file
```

---

## Production Architecture (Scalable)

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │  Web App     │  │  Mobile App  │  │  Desktop App │            │
│  │  (React)     │  │  (Flutter)   │  │  (Electron)  │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ↓ HTTPS
┌─────────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                              │
│                     (Cloud Load Balancer)                           │
│  • Authentication (Firebase Auth)                                   │
│  • Rate Limiting                                                    │
│  • SSL/TLS Termination                                             │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                                │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                    Cloud Run Services                         │ │
│  │                                                              │ │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐           │ │
│  │  │   Upload   │  │  Process   │  │   Search   │           │ │
│  │  │   API      │  │    API     │  │    API     │           │ │
│  │  └────────────┘  └────────────┘  └────────────┘           │ │
│  │        │              │                │                   │ │
│  └────────┼──────────────┼────────────────┼───────────────────┘ │
│           │              │                │                     │
└───────────┼──────────────┼────────────────┼─────────────────────┘
            │              │                │
            ↓              ↓                ↓
┌───────────────────────────────────────────────────────────────────┐
│                      QUEUE LAYER                                  │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    Cloud Tasks                              │ │
│  │  • Video Processing Queue                                  │ │
│  │  • Frame Analysis Queue                                    │ │
│  │  • Notification Queue                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
            │
            ↓
┌───────────────────────────────────────────────────────────────────┐
│                    PROCESSING LAYER                               │
│                                                                   │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │   FFmpeg     │     │   Gemini     │     │   Vertex     │    │
│  │   Workers    │ →   │   2.0 Flash  │ →   │   AI Match   │    │
│  │ (Frame Ext)  │     │  (Analysis)  │     │  (Embeddings)│    │
│  └──────────────┘     └──────────────┘     └──────────────┘    │
└───────────────────────────────────────────────────────────────────┘
            │
            ↓
┌───────────────────────────────────────────────────────────────────┐
│                     STORAGE LAYER                                 │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Cloud       │  │  Firestore   │  │  BigQuery    │          │
│  │  Storage     │  │  (Logs DB)   │  │  (Analytics) │          │
│  │  (Videos)    │  │              │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└───────────────────────────────────────────────────────────────────┘
            │
            ↓
┌───────────────────────────────────────────────────────────────────┐
│                  MONITORING & LOGGING                             │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Cloud       │  │  Cloud       │  │  Error       │          │
│  │  Logging     │  │  Monitoring  │  │  Reporting   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└───────────────────────────────────────────────────────────────────┘
```

### Production Data Flow

```
Step 1: VIDEO UPLOAD
   User → Web App → Cloud Run Upload API
                         ↓
                    Cloud Storage
                    (Store video)
                         ↓
                    Cloud Tasks
                    (Queue job)

Step 2: ASYNC PROCESSING
   Cloud Tasks → Cloud Run Process API
                      ↓
                  Download video
                      ↓
                  Extract frames (FFmpeg)
                      ↓
                  For each frame:
                      ↓
                  Gemini 2.0 Flash
                      ↓
                  Generate description
                      ↓
                  Create embedding (Vertex AI)
                      ↓
                  Store in Firestore
                      ↓
                  Update job status

Step 3: SEARCH
   User → Web App → Cloud Run Search API
                         ↓
                    Generate query embedding
                         ↓
                    Vertex AI Matching Engine
                    (Semantic search)
                         ↓
                    Firestore
                    (Get full logs)
                         ↓
                    Return results to user

Step 4: NOTIFICATIONS
   Processing complete → Cloud Tasks
                              ↓
                         Firebase Cloud Messaging
                              ↓
                         User notification
```

---

## Component Details

### 1. Frontend (Production)

```
React/Angular App
├── Components
│   ├── VideoUploader
│   ├── ProcessingStatus
│   ├── SearchInterface
│   ├── ResultsViewer
│   └── ExportTools
│
├── State Management (Redux/Context)
│   ├── User session
│   ├── Video queue
│   ├── Search results
│   └── Notifications
│
└── API Client
    ├── Upload videos
    ├── Check status
    ├── Search logs
    └── Export data
```

### 2. Backend Services (Cloud Run)

```
Service 1: Upload API
├── Endpoint: POST /api/upload
├── Function: Handle video uploads
├── Flow:
│   ├── Validate file
│   ├── Upload to Cloud Storage
│   ├── Create job in Firestore
│   └── Queue processing task
└── Response: job_id, upload_url

Service 2: Process API
├── Endpoint: POST /api/process
├── Function: Process videos (called by Cloud Tasks)
├── Flow:
│   ├── Download video from Cloud Storage
│   ├── Extract frames (FFmpeg)
│   ├── Analyze with Gemini 2.0
│   ├── Generate embeddings
│   ├── Store logs in Firestore
│   └── Update job status
└── Response: processing_complete

Service 3: Search API
├── Endpoint: POST /api/search
├── Function: Search video logs
├── Flow:
│   ├── Receive search query
│   ├── Generate query embedding
│   ├── Search Vertex AI Matching Engine
│   ├── Retrieve full logs from Firestore
│   └── Return ranked results
└── Response: search_results[]

Service 4: Export API
├── Endpoint: GET /api/export
├── Function: Export logs
├── Flow:
│   ├── Query Firestore for user logs
│   ├── Format as JSON/CSV
│   ├── Generate download link
│   └── Return signed URL
└── Response: download_url
```

### 3. Database Schema (Firestore)

```
Collection: users
Document: {user_id}
  ├── email: string
  ├── created_at: timestamp
  └── subscription: object

    Subcollection: videos
    Document: {video_id}
      ├── filename: string
      ├── upload_url: string
      ├── duration: number
      ├── uploaded_at: timestamp
      ├── processed_at: timestamp
      └── status: enum [queued, processing, completed, failed]

        Subcollection: logs
        Document: {log_id}
          ├── video_id: reference
          ├── timestamp: string ("00:05:23")
          ├── timestamp_seconds: number
          ├── frame_number: number
          ├── description: string
          ├── entities: array
          ├── embedding: array (for semantic search)
          ├── confidence: number
          └── analyzed_at: timestamp

Collection: jobs
Document: {job_id}
  ├── user_id: reference
  ├── video_id: reference
  ├── status: enum
  ├── total_frames: number
  ├── processed_frames: number
  ├── created_at: timestamp
  ├── started_at: timestamp
  ├── completed_at: timestamp
  └── error: string (if failed)
```

### 4. Cloud Tasks Configuration

```
Queue: video-processing
  ├── Max concurrent: 100
  ├── Max rate: 500/second
  ├── Retry config:
  │   ├── Max attempts: 3
  │   ├── Min backoff: 10s
  │   └── Max backoff: 300s
  └── Target: Cloud Run Process API

Queue: notifications
  ├── Max concurrent: 1000
  ├── Max rate: 1000/second
  └── Target: Firebase Cloud Messaging
```

---

## Scaling Characteristics

### Prototype (Current)
- **Users**: 1 (local)
- **Concurrent Videos**: 1
- **Processing**: Synchronous
- **Storage**: Local filesystem
- **Cost**: Free (API tier)

### Production (Target)
- **Users**: 100-2000 concurrent
- **Concurrent Videos**: 1000+
- **Processing**: Asynchronous with queue
- **Storage**: Cloud Storage + Firestore
- **Cost**: ~$0.30 per hour of footage

### Auto-Scaling Configuration

```
Cloud Run:
  Min Instances: 1
  Max Instances: 100
  CPU: 2 cores
  Memory: 4GB
  
  Scaling Triggers:
  ├── CPU > 60%
  ├── Memory > 70%
  └── Request rate > 100/second

Firestore:
  Automatic scaling (serverless)
  
Cloud Storage:
  Unlimited storage
  Auto-tiering (lifecycle policies)
```

---

## Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                          │
│                                                             │
│  1. Network Security                                        │
│     ├── Cloud Armor (DDoS protection)                      │
│     ├── SSL/TLS encryption                                 │
│     └── VPC for private networking                         │
│                                                             │
│  2. Authentication & Authorization                          │
│     ├── Firebase Authentication                            │
│     ├── JWT tokens                                         │
│     ├── Role-based access control (RBAC)                   │
│     └── API key management (Secret Manager)                │
│                                                             │
│  3. Data Security                                          │
│     ├── Encryption at rest (Cloud Storage)                 │
│     ├── Encryption in transit (TLS 1.3)                   │
│     ├── Firestore security rules                          │
│     └── Data retention policies                           │
│                                                             │
│  4. Application Security                                    │
│     ├── Input validation                                   │
│     ├── Rate limiting                                      │
│     ├── CORS configuration                                 │
│     └── Error handling (no sensitive data leaks)          │
│                                                             │
│  5. Monitoring & Auditing                                  │
│     ├── Cloud Logging (all API calls)                     │
│     ├── Cloud Monitoring (alerts)                         │
│     ├── Audit logs                                         │
│     └── Anomaly detection                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Cost Structure

### Per Video Hour Processing

```
Component                     Cost/Hour    Notes
─────────────────────────────────────────────────────
Gemini 2.0 Flash              $0.15       720 frames @ 5s
Cloud Run                     $0.05       Processing time
Cloud Storage                 $0.02       Video storage
Firestore                     $0.03       Log writes/reads
Vertex AI Embeddings          $0.02       Optional
Cloud Tasks                   $0.01       Queue operations
─────────────────────────────────────────────────────
TOTAL (optimized)             ~$0.28      

With optimizations:
- Motion detection            -40%        Skip static frames
- Variable intervals          -30%        Adjust by time of day
- Batch processing            -20%        Process in batches
─────────────────────────────────────────────────────
OPTIMIZED TOTAL              ~$0.15-0.20  per hour
```

### Monthly Cost Examples

```
Scenario 1: Small Business (5 cameras, 24/7)
├── Video hours: 3,600/month
├── Processing: $540-720
├── Storage: $50
├── Queries: $20
└── TOTAL: ~$610-790/month

Scenario 2: Medium Business (20 cameras, 24/7)
├── Video hours: 14,400/month
├── Processing: $2,160-2,880
├── Storage: $200
├── Queries: $100
└── TOTAL: ~$2,460-3,180/month

Scenario 3: Large Enterprise (100 cameras, 24/7)
├── Video hours: 72,000/month
├── Processing: $10,800-14,400 (with enterprise discounts)
├── Storage: $1,000
├── Queries: $500
└── TOTAL: ~$12,300-15,900/month
```

---

This architecture ensures:
✅ Scalability (1 to 2000+ users)
✅ Reliability (99.9% uptime)
✅ Security (enterprise-grade)
✅ Performance (< 5s response time)
✅ Cost-effectiveness (pay-as-you-go)
