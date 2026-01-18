# 📚 RAG PDF Chatbot - Beginner Friendly

A simple Retrieval-Augmented Generation (RAG) chatbot that reads PDF documents and answers questions about their content using X.AI's Grok API.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

- 📄 **PDF Text Extraction** - Upload and extract text from any PDF document
- 🔍 **Smart Search** - Uses vector embeddings for intelligent information retrieval
- 🤖 **AI-Powered Answers** - Leverages X.AI's Grok to generate accurate responses
- 💾 **Persistent Sessions** - Maintains conversation state across interactions
- 🎨 **Clean UI** - Simple, intuitive Streamlit interface
- 🔒 **Secure** - API keys stored locally in environment variables

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- X.AI API Key (get it from [console.x.ai](https://console.x.ai))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/rag-pdf-chatbot.git
   cd rag-pdf-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   
   Create a `.env` file in the project root:
   ```bash
   XAI_API_KEY=your_api_key_here
   ```
   
   Or enter it directly in the app's sidebar when running.

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   
   The app will automatically open at `http://localhost:8501`

## 📖 How to Use

### Step 1: Setup
1. Enter your X.AI API key in the sidebar
2. Upload a PDF document (use the sample `research-paper-final.pdf` to test)
3. Click "Process PDF" to index the document

### Step 2: Ask Questions
1. Type your question in the text box
2. Click "Get Answer"
3. View the AI-generated response based on your PDF content

### Example Questions

Try asking questions like:
- "What are the main findings of this paper?"
- "What methodology was used in this research?"
- "Can you summarize the introduction?"
- "What are the key conclusions?"

## 🏗️ How It Works

This chatbot uses **RAG (Retrieval-Augmented Generation)**, a technique that combines:

1. **Text Extraction** - Reads and extracts text from PDF documents
2. **Chunking** - Splits text into manageable 300-word pieces with overlap
3. **Embeddings** - Converts text chunks into numerical vectors using `sentence-transformers`
4. **Vector Storage** - Stores embeddings in a FAISS database for fast similarity search
5. **Retrieval** - Finds the 3 most relevant chunks for each question
6. **Generation** - Sends relevant context to X.AI's Grok to generate accurate answers

```
PDF → Extract Text → Create Chunks → Generate Embeddings → FAISS Index
                                                              ↓
User Question → Find Relevant Chunks → Send to Grok AI → Get Answer
```

## 📁 Project Structure

```
rag-pdf-chatbot/
│
├── app.py                      # Main Streamlit application
├── research-paper-final.pdf    # Sample PDF for testing
├── requirements.txt            # Python dependencies
├── runtime.txt                 # Python version specification
├── .env                        # Environment variables (create this)
├── .gitignore                  # Git ignore file
└── README.md                   # This file
```

## 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[PyPDF2](https://pypdf2.readthedocs.io/)** - PDF text extraction
- **[Sentence Transformers](https://www.sbert.net/)** - Text embeddings (all-MiniLM-L6-v2 model)
- **[FAISS](https://github.com/facebookresearch/faiss)** - Vector similarity search
- **[X.AI Grok API](https://x.ai/)** - Language model for answer generation
- **[NumPy](https://numpy.org/)** - Numerical computations

## 📦 Requirements

```txt
streamlit>=1.28.0
PyPDF2>=3.0.0
sentence-transformers>=2.2.0
faiss-cpu>=1.7.4
requests>=2.31.0
numpy>=1.24.0
python-dotenv>=1.0.0
```

## 🎓 Educational Purpose

This project is designed for **beginners learning AI/ML** with Python. It demonstrates:

- Basic RAG architecture
- Working with PDF documents
- Vector embeddings and similarity search
- API integration
- Streamlit application development
- Session state management

## 🔧 Configuration

### Environment Variables

Create a `.env` file:
```bash
XAI_API_KEY=xai-your-api-key-here
```

### Customization Options

You can modify these parameters in `app.py`:

- **Chunk size**: Change `chunk_size = 300` in `break_text_into_chunks()`
- **Number of retrieved chunks**: Change `3` in `database.search(question_embedding, 3)`
- **Embedding model**: Change `'all-MiniLM-L6-v2'` to another model
- **Temperature**: Change `"temperature": 0` in the API call for more creative responses

## ❓ Troubleshooting

### Common Issues

**Q: Page goes blank after clicking "Get Answer"**
- A: Make sure all dependencies are installed correctly
- A: Check that your API key is valid

**Q: "Invalid API Key" error**
- A: Verify your X.AI API key at [console.x.ai](https://console.x.ai)
- A: Make sure there are no extra spaces in the key

**Q: PDF processing takes too long**
- A: Large PDFs (>100 pages) may take 1-2 minutes to process
- A: Wait for the "✅ Done!" message before asking questions

**Q: "Could not find relevant information" message**
- A: Try rephrasing your question
- A: Make sure your question relates to the PDF content

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) for Claude assistance
- [X.AI](https://x.ai/) for the Grok API
- [Streamlit](https://streamlit.io/) for the amazing framework
- The open-source community for the incredible libraries

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ for AI beginners**

⭐ Star this repo if you find it helpful!