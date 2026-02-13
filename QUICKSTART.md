# 🚀 Quick Start Guide - SAP AI Assistant

Get your SAP Enterprise AI Assistant running in **5 minutes**!

---

## ⚡ Super Quick Start

### Windows Users (Easiest):
```powershell
.\start.ps1
```

That's it! Open http://localhost:8000

---

## 📋 Step-by-Step Installation

### 1. Prerequisites
- ✅ Python 3.12+ installed
- ✅ pip package manager
- ✅ Terminal/PowerShell access

### 2. Setup Virtual Environment

**Windows PowerShell:**
```powershell
# Create virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure (Optional for Testing)

```bash
# Copy example config
cp .env.example .env

# Edit if needed (works without changes for testing)
# nano .env  # or use your favorite editor
```

### 4. Start the Server

**Option A - Automated (Windows):**
```powershell
.\start.ps1
```

**Option B - Python Script:**
```bash
python run_backend.py
```

**Option C - Direct Uvicorn:**
```bash
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access the Application

🌐 **Open your browser:**
- **Main App**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

---

## 🎯 Try It Out!

### Sample Queries to Test:

1. **Stock Analysis**
   ```
   Is stock getting reduced?
   ```

2. **Sales Insights**
   ```
   What are Q4 sales trends?
   ```

3. **KPI Dashboard**
   ```
   Show me key performance indicators
   ```

4. **Customer Analytics**
   ```
   What's our customer retention rate?
   ```

5. **Cost Optimization**
   ```
   Where can we reduce costs?
   ```

---

## 👥 Collaborative Features (New!)

1. **Login**: Use the **Login** button to access the platform.
   - **Business Login**: `alice@sap.com` / `password123` (Manager)
   - **User Login**: `charlie@sap.com` / `password123` (Analyst)

2. **Team Feed**: Click the **Conversations** tab to see analysis sessions shared by your team.

3. **Discussion**: Click any conversation card to view the insight and **add comments** to collaborate with your team.

---

## 🔧 Configuration Options

### Environment Variables (.env)

```env
# Application
APP_ENV=dev                    # dev, staging, or prod
APP_PORT=8000                  # Server port

# AI Model (optional - works in mock mode without this)
MODEL_API_KEY=your_key_here    # OpenAI or Anthropic API key

# Database (optional for basic usage)
DB_ENGINE=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sap_ai_assistant
DB_USER=your_username
DB_PASSWORD=your_password
```

---

## 🤖 Upgrade to Real AI (Optional)

### Using OpenAI:

1. Get API key: https://platform.openai.com/api-keys
2. Update `.env`:
   ```env
   MODEL_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
   ```
3. Restart server

### Using Anthropic (Claude):

1. Get API key: https://console.anthropic.com/
2. Update `.env`:
   ```env
   MODEL_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
   ```
3. Restart server

**Note**: Works great in **free mock mode** without any API key!

---

## 🧪 Testing

### Run API Tests:
```bash
python test_api.py
```

Expected output:
```
Testing SAP AI Assistant API...

1. Health Check:
   ✅ Status: 200
   ✅ Response: {'status': 'ok', 'environment': 'dev'}

2. Model Test:
   ✅ Status: 200
   ...

============================================================
✅ All tests passed! Your AI Assistant is working!
============================================================
```

---

## 🛑 Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

---

## 🐛 Troubleshooting

### Port Already in Use?
```powershell
# Use a different port
uvicorn backend.app:app --port 8001
```

### Module Not Found?
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend Not Loading?
- Ensure backend is running
- Check http://localhost:8000/health returns `{"status":"ok"}`
- Clear browser cache (Ctrl+Shift+R)
- Check browser console for errors (F12)

### Virtual Environment Issues?
```bash
# Delete and recreate
rm -rf .venv  # or rmdir /s .venv on Windows
python -m venv .venv
# Then activate and install again
```

---

## 📁 Project Structure

```
SAP-AI-Assistant/
├── backend/           # FastAPI backend
│   ├── app.py        # Main application
│   ├── config.py     # Configuration
│   └── services/     # Business logic
├── frontend/         # Web interface
│   ├── index.html   # UI
│   ├── app.js       # Logic
│   └── styles.css   # Styles
├── .env             # Config (create from .env.example)
├── requirements.txt # Dependencies
├── run_backend.py   # Startup script
└── start.ps1        # Windows launcher
```

---

## 🚀 Next Steps

1. ✅ **Application Running** - You're here!
2. 📖 **Read Full Documentation** - Check [README.md](README.md)
3. 🎨 **Customize UI** - Edit `frontend/` files
4. 🤖 **Add Real AI** - Configure OpenAI/Anthropic
5. 🗄️ **Add Database** - Configure DB settings
6. 🚢 **Deploy** - See deployment section in README

---

## 📚 More Information

- **Full Documentation**: [README.md](README.md)
- **Architecture**: [docs/architecture.md](docs/architecture.md)
- **API Reference**: http://localhost:8000/docs (when running)
- **Requirements**: [docs/srs.md](docs/srs.md)

---

## 💡 Tips

- **Auto-reload**: Server restarts when you edit code
- **API Docs**: Interactive testing at `/docs`
- **Mock Mode**: Works perfectly without AI API keys
- **Fast**: Response time < 1 second
- **Secure**: Environment-based configuration

---

**🎉 You're all set! Enjoy using SAP AI Assistant!**

Need help? Check the troubleshooting section or open an issue on GitHub.
