# SAP Enterprise AI Assistant

> Intelligent Decision Support System for Enterprise Stakeholders

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise-grade AI-powered assistant providing intelligent business insights, analytics, and recommendations through a modern web interface.

---

## 🌟 Features

- **🤖 Smart AI Analysis** - Context-aware business insights across multiple domains
- **📊 Multi-Domain Support** - Stock, Sales, KPIs, Customers, Costs, Risk & Compliance
- **🔌 Flexible AI Integration** - Support for OpenAI, Anthropic, or custom models
- **🎨 Modern UI** - Responsive, dark-themed interface with real-time updates
- **🚀 Production Ready** - Auto-reload, error handling, and comprehensive logging
- **📡 RESTful API** - Well-documented endpoints with Swagger UI
- **🔐 Configurable** - Environment-based configuration management

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Git (for version control)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd "SAP AI Assistant"
```

2. **Create virtual environment**
```bash
python -m venv .venv
```

3. **Activate virtual environment**

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Configure environment**
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings (optional for testing)
```

6. **Start the application**

**Option A - Using PowerShell script (Windows):**
```powershell
.\start.ps1
```

**Option B - Using Python:**
```bash
python run_backend.py
```

**Option C - Using uvicorn directly:**
```bash
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

7. **Access the application**

Open your browser and navigate to:
- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 📁 Project Structure

```
SAP-AI-Assistant/
├── backend/                    # Backend application
│   ├── __init__.py
│   ├── app.py                 # FastAPI application & routes
│   ├── config.py              # Configuration management
│   └── services/              # Business logic services
│       ├── __init__.py
│       ├── model_service.py   # AI/ML integration
│       └── db_service.py      # Database operations
│
├── frontend/                   # Frontend web interface
│   ├── index.html             # Main HTML page
│   ├── app.js                 # JavaScript logic
│   └── styles.css             # Styling & layout
│
├── docs/                       # Documentation
│   ├── architecture.md        # System architecture
│   ├── srs.md                 # Software requirements
│   ├── phase1_submission.md   # Phase 1 deliverables
│   ├── literature_analysis.md # Research analysis
│   ├── evaluation_rubrics.md  # Evaluation criteria
│   ├── diagrams/              # System diagrams
│   │   ├── er_diagram.mmd
│   │   └── system_flow.mmd
│   └── wireframes/            # UI wireframes
│       └── wireframes.md
│
├── .env.example               # Environment template
├── .env                       # Environment config (gitignored)
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
├── run_backend.py            # Server startup script
├── start.ps1                 # Windows startup script
├── test_api.py               # API testing suite
├── QUICKSTART.md             # Quick start guide
└── README.md                 # This file
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory (copy from `.env.example`):

```env
# Application Settings
APP_ENV=dev                              # Environment: dev, staging, prod
APP_PORT=8000                            # Server port

# AI Model Configuration
MODEL_API_KEY=your_api_key_here          # OpenAI or Anthropic API key

# Database Configuration (optional for basic usage)
DB_ENGINE=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sap_ai_assistant
DB_USER=your_db_user
DB_PASSWORD=your_db_password
```

### AI Provider Setup (Optional)

The application works out-of-the-box with intelligent mock responses. To enable real AI:

**For OpenAI (GPT-3.5/GPT-4):**
1. Get API key from https://platform.openai.com/api-keys
2. Update `.env`: `MODEL_API_KEY=sk-proj-xxxxxxxxxxxxx`
3. Restart the server

**For Anthropic (Claude):**
1. Get API key from https://console.anthropic.com/
2. Update `.env`: `MODEL_API_KEY=sk-ant-xxxxxxxxxxxxx`
3. Restart the server

The system automatically detects the provider and falls back to mock mode if needed.

---

## 📡 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web interface (HTML) |
| `GET` | `/health` | Health check endpoint |
| `GET` | `/api/model-test` | Test AI connectivity |
| `POST` | `/api/analyze` | Analyze business query |
| `GET` | `/docs` | Swagger UI documentation |
| `GET` | `/redoc` | ReDoc documentation |

### Example Usage

**Health Check:**
```bash
curl http://localhost:8000/health
```

**AI Analysis:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "What are Q4 sales trends?"}'
```

**Response:**
```json
{
  "status": "success",
  "analysis": "📊 Sales Performance Analysis...",
  "query": "What are Q4 sales trends?",
  "model": "mock-ai-v1",
  "mock_mode": true
}
```

---

## 🎯 Usage Examples

### Try These Queries:

**Inventory Management:**
```
Is stock getting reduced?
What's the status of inventory levels?
```

**Sales & Revenue:**
```
What are Q4 sales trends?
Show me profit margins
```

**Performance Metrics:**
```
What are the key performance indicators?
Show me business metrics
```

**Customer Analytics:**
```
What's our customer retention rate?
How many customers are at risk?
```

**Cost Analysis:**
```
Show me budget optimization opportunities
Where can we reduce costs?
```

**Risk & Compliance:**
```
What's our compliance status?
Show me security risks
```

---

## 🧪 Testing

### Run API Tests

```bash
python test_api.py
```

### Manual Testing

1. **Health Check**: http://localhost:8000/health
2. **API Docs**: http://localhost:8000/docs (test endpoints interactively)
3. **Web Interface**: http://localhost:8000 (try various queries)

---

## 🛠️ Development

### Running in Development Mode

```bash
# With auto-reload enabled
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

### Code Structure

**Backend (FastAPI):**
- `app.py` - Application setup, routes, middleware
- `config.py` - Configuration and environment management
- `services/model_service.py` - AI logic and integrations
- `services/db_service.py` - Database operations

**Frontend (Vanilla JS):**
- `index.html` - Structure and layout
- `app.js` - Business logic and API calls
- `styles.css` - Styling and responsive design

---

## 🚢 Deployment

### Using Docker (Recommended)

```dockerfile
# Coming soon - Dockerfile will be added
```

### Manual Deployment

1. Set `APP_ENV=production` in `.env`
2. Use production WSGI server (already using uvicorn)
3. Set up reverse proxy (Nginx/Apache)
4. Configure SSL certificates
5. Set up monitoring and logging

---

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get started in minutes
- **[Architecture](docs/architecture.md)** - System design and architecture
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs (when running)
- **[SRS](docs/srs.md)** - Software requirements specification

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- FastAPI framework for the robust backend
- OpenAI & Anthropic for AI capabilities
- SAP for enterprise requirements and context

---

## 📞 Support

For issues, questions, or contributions:
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Documentation**: [Wiki](https://github.com/your-repo/wiki)

---

## 🎯 Roadmap

- [x] Core AI assistant functionality
- [x] Multi-domain analysis support
- [x] OpenAI & Anthropic integration
- [ ] Database integration
- [ ] User authentication
- [ ] Advanced analytics dashboard
- [ ] Export reports (PDF/Excel)
- [ ] Multi-language support
- [ ] Docker containerization
- [ ] Cloud deployment (AWS/Azure/GCP)

---

**Made with ❤️ for Enterprise Decision Support**
