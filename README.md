# 🎓 DSU MBA Department AI Assistant

An intelligent question-answering system specifically designed for Dayananda Sagar University's MBA Department. This system uses a small language model (Llama 3.2 1B) with Retrieval Augmented Generation (RAG) to provide accurate answers from the MBA department's knowledge base.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Adding Documents](#adding-documents)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## ✨ Features

- **Specific Knowledge Base**: Trained on DSU MBA department documents
- **RAG-Powered**: Retrieves relevant context before generating answers
- **CPU-Optimized**: Runs on systems without GPU using quantized models
- **Source Attribution**: Cites sources for transparency and verification
- **Modern Web Interface**: Clean, responsive UI for easy interaction
- **REST API**: Easy to integrate with other applications
- **Low Resource Requirements**: Works on 16GB RAM, 300GB SSD

## 🎬 Demo

```
Question: What are the MBA admission requirements?
Answer: Based on the MBA department documents, admission requirements include:
- Bachelor's degree from a recognized university
- Minimum 50% aggregate marks
- Valid entrance exam scores (KMAT/CAT/MAT)
- English language proficiency

📚 Sources: admission-guidelines.pdf, mba-handbook.pdf
```

## 🏗️ Architecture

```
User Query → Web Interface → Flask API → Vector DB (Retrieval)
                                            ↓
                                      Llama 3.2 1B (Generation)
                                            ↓
                                      Answer + Sources
```

**Key Components:**
- **Frontend**: HTML/CSS/JavaScript with modern UI
- **Backend**: Flask REST API
- **Vector Database**: ChromaDB for document embeddings
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **LLM**: Llama 3.2 1B (quantized GGUF format)

## 📦 Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04+ (or any Linux distribution)
- **RAM**: 16GB minimum
- **Storage**: 10GB free space
- **CPU**: Multi-core processor (4+ cores recommended)
- **GPU**: Not required (CPU-only operation)

### Software Requirements
- Python 3.10 or higher
- pip (Python package manager)
- Git

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/dsu-mba-ai-assistant.git
cd dsu-mba-ai-assistant
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Download the Model

```bash
# Create models directory
mkdir -p models

# Download Llama 3.2 1B quantized model
huggingface-cli download TheBloke/Llama-3.2-1B-GGUF llama-3.2-1b.Q4_K_M.gguf --local-dir ./models --local-dir-use-symlinks False
```

**Alternative**: If `huggingface-cli` doesn't work:
```bash
cd models
wget https://huggingface.co/TheBloke/Llama-3.2-1B-GGUF/resolve/main/llama-3.2-1b.Q4_K_M.gguf
cd ..
```

### Step 5: Add Your Documents

```bash
# Create knowledge base directory
mkdir -p knowledge_base

# Add your MBA department documents (PDF, TXT, DOCX)
# Copy files to knowledge_base/ directory
```

### Step 6: Build the Knowledge Base

```bash
python build_knowledge_base.py
```

Expected output:
```
==================================================
Building University Knowledge Base
==================================================

[1/5] Loading documents...
   ✓ Loaded 5 PDF documents
   
[2/5] Splitting documents into chunks...
   ✓ Created 127 text chunks
   
[3/5] Loading embedding model...
   ✓ Embedding model loaded
   
[4/5] Creating vector database...
   
[5/5] Persisting database to disk...

✓ SUCCESS! Vector database created
```

### Step 7: Run the Application

```bash
python app.py
```

The application will be available at: **http://localhost:5000**

## 💻 Usage

### Web Interface

1. Open your browser and navigate to `http://localhost:5000`
2. Type your question in the input box
3. Press Enter or click the send button
4. View the answer with source citations

### API Usage

**Health Check:**
```bash
curl http://localhost:5000/api/health
```

**Ask a Question:**
```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the MBA specializations?"}'
```

**Response Format:**
```json
{
  "success": true,
  "answer": "The MBA program offers specializations in...",
  "sources": ["mba-curriculum.pdf", "specializations.pdf"],
  "confidence": "high",
  "num_sources": 2,
  "timestamp": "2024-10-04T14:30:00"
}
```

## 📁 Project Structure

```
dsu-mba-ai-assistant/
├── app.py                      # Flask application
├── config.py                   # Configuration settings
├── build_knowledge_base.py     # Script to build vector DB
├── qa_system.py                # Core QA logic (optional standalone)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
│
├── models/                     # Language models (not in Git)
│   └── llama-3.2-1b.Q4_K_M.gguf
│
├── knowledge_base/             # Your documents (not in Git)
│   ├── admission-guide.pdf
│   ├── mba-curriculum.pdf
│   └── faculty-info.pdf
│
├── vectordb/                   # Vector database (not in Git)
│   └── chroma.sqlite3
│
├── static/                     # Frontend assets
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│       └── logo.png
│
└── templates/                  # HTML templates
    └── index.html
```

## ⚙️ Configuration

Edit `config.py` to customize settings:

```python
# Model settings
MODEL_PATH = "./models/llama-3.2-1b.Q4_K_M.gguf"
N_CTX = 2048              # Context window size
N_THREADS = 4             # CPU threads
MAX_TOKENS = 256          # Max answer length
TEMPERATURE = 0.3         # Lower = more focused

# Retrieval settings
TOP_K_DOCUMENTS = 3       # Number of documents to retrieve
```

## 📚 Adding Documents

### Supported Formats
- PDF (.pdf)
- Text files (.txt)
- Word documents (.docx) - requires python-docx

### Adding New Documents

1. **Copy documents to knowledge_base/**
```bash
cp ~/Downloads/new-document.pdf knowledge_base/
```

2. **Rebuild the vector database**
```bash
python build_knowledge_base.py
```

3. **Restart the application**
```bash
# Stop the app (Ctrl+C) and restart
python app.py
```

### Organizing Documents

You can organize documents in subdirectories:
```
knowledge_base/
├── admissions/
│   ├── requirements.pdf
│   └── process.pdf
├── curriculum/
│   ├── courses.pdf
│   └── syllabus.pdf
└── policies/
    └── student-handbook.pdf
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Reporting Issues

1. Check if the issue already exists
2. Provide detailed description
3. Include error messages and screenshots
4. Specify your system configuration

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow PEP 8 style guide
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   ```bash
   python build_knowledge_base.py
   python app.py
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Add: Feature description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**

### Development Setup

```bash
# Install development dependencies
pip install pytest black flake8

# Run tests
pytest tests/

# Format code
black *.py

# Check style
flake8 *.py
```

## 🐛 Troubleshooting

### Model Not Loading

**Error**: `ERROR: Model not found`

**Solution**:
```bash
# Check model exists
ls -lh models/llama-3.2-1b.Q4_K_M.gguf

# Re-download if necessary
cd models
wget https://huggingface.co/TheBloke/Llama-3.2-1B-GGUF/resolve/main/llama-3.2-1b.Q4_K_M.gguf
```

### Out of Memory

**Error**: `MemoryError` or system freeze

**Solution**:
- Reduce `N_CTX` in `config.py` (try 1024)
- Reduce `TOP_K_DOCUMENTS` to 2
- Close other applications
- Use a smaller quantized model (Q3 instead of Q4)

### Slow Responses

**Solution**:
- Increase `N_THREADS` to match your CPU cores
- Reduce `MAX_TOKENS`
- Use SSD instead of HDD
- Reduce chunk size in `build_knowledge_base.py`

### No Documents Found

**Error**: `ERROR: No documents loaded`

**Solution**:
```bash
# Check files exist
ls -la knowledge_base/

# Ensure correct format (.pdf or .txt)
file knowledge_base/your-file.pdf

# Check permissions
chmod +r knowledge_base/*.pdf
```

### Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use different port
# Edit app.py: app.run(port=5001)
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - Initial work - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Dayananda Sagar University MBA Department
- Llama model by Meta AI
- LangChain community
- ChromaDB team
- Sentence Transformers

## 📞 Contact

For questions or support:
- **Email**: your.email@example.com
- **GitHub Issues**: [Create an issue](https://github.com/yourusername/dsu-mba-ai-assistant/issues)
- **University**: contact@dsu.edu.in

## 🗺️ Roadmap

- [ ] Add support for more document formats (DOCX, XLSX)
- [ ] Implement conversation history
- [ ] Add user authentication
- [ ] Deploy on cloud (AWS/GCP)
- [ ] Add voice input/output
- [ ] Multi-language support
- [ ] Fine-tuning on specific MBA content
- [ ] Mobile app version

---

**⭐ If you find this project helpful, please give it a star!**

Made with ❤️ for Dayananda Sagar University
