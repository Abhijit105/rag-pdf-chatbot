import streamlit as st
import PyPDF2
from sentence_transformers import SentenceTransformer
import faiss
import requests
from dotenv import load_dotenv

# ============== STEP 1: READ PDF FILES =================
def read_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    full_text = ""

    for page in reader.pages:
        full_text += page.extract_text()

    return full_text

# ============== STEP 2: SPLIT TEXT INTO SMALL PIECES =================
def break_text_into_chunks(text):
    words = text.split()
    chunks = []
    chunk_size = 300

    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks

# ============== STEP 3: CONVERT TEXT TO EMBEDDINGS ==================
def convert_to_embeddings(text_chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(text_chunks, show_progress_bar=True)

    return embeddings, model

# ============== STEP 4: CREATE A DATABASE ================
def create_search_database(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index

# ============== STEP 5: FIND RELEVANT INFORMATION ==================
def find_relevant_chunks(question, model, database, all_chunks):
    question_embedding = model.encode([question])
    distances, positions = database.search(question_embedding, 3)
    relevant_chunks = [all_chunks[pos] for pos in positions[0]]

    return relevant_chunks

# STEP 6: ASK GROK AI FOR ANSWER ================
def ask_grok(question, context, api_key):
    url = "https://api.x.ai/v1/chat/completions"

    prompt = f"""
    Here is some information from a document:
    {context}

    Based ONLY on the information above, answer this question:
    {question}

    If the answer is not in the information, say " I don't know based on this document."
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": "grok-3"
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 401:
            return "❌ Error: Invalid API Key. Please check your X.AI API key at https://console.x.ai"
        elif response.status_code == 429:
            return "❌ Error: Rate limit exceeded. Please wait a moment and try again."
        elif response.status_code == 500:
            return "❌ Error: X.AI server error. Please try again in a moment."
        elif response.status_code == 200:
            # Parse the successful response
            result = response.json()
            answer = result['choices'][0]['message']['content']
            return answer
        else:
            return "❌ Error: Something went wrong. Please try again."

    except requests.exceptions.Timeout:
        return "❌ Error: Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return "❌ Error: Could not connect to X.AI. Check your internet connection."
    except KeyError:
        return f"❌ Error: Unexpected response format. Response: {response.text[:200]}"
    except Exception as e:
        return f"❌ Error: {str(e)}\n\nResponse status: {response.status_code if 'response' in locals() else 'No response'}"

load_dotenv()
# def main_function():
    # text = read_pdf("./research-paper-final.pdf")
    # chunks = break_text_into_chunks(text)
    # embeddings, model = convert_to_embeddings(chunks)
    # db = create_search_database(embeddings)
    # relevant_chunks = find_relevant_chunks("What is the purpose of this document", model, db, chunks)
    # result = ask_grok("What is the purpose of this document", relevant_chunks, XAI_API_KEY)
  # print(result)

# main_function()

# Page setup
st.set_page_config(page_title="PDF Chatbot", page_icon="📚", initial_sidebar_state="expanded")
st.title("📚 Simple PDF Question Answering Bot")
st.write("Upload a PDF and ask questions about it!")

# Create storage for our data
if 'text_chunks' not in st.session_state:
    st.session_state.text_chunks = None
if 'search_database' not in st.session_state:
    st.session_state.search_database = None
if 'ai_model' not in st.session_state:
    st.session_state.ai_model = None

st.sidebar.header("Step 1: Setup")

api_key = st.sidebar.text_input("Enter your Grok API key: ", type="password")
st.sidebar.caption("Get it from: https://console,x.ai")
st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader("Upload your PDF: ", type="pdf")

# Process the PDF when button is clicked
if uploaded_file and st.sidebar.button("Process PDF"):

    with st.sidebar:
        with st.spinner("Processing PDF..."):
            st.write("⏳ Reading PDF...")
            # STEP 1: Read the PDF
            pdf_text = read_pdf(uploaded_file)

            st.write("⏳ Breaking into chunks...")
            # STEP 2: Break into chunks
            st.session_state.text_chunks = break_text_into_chunks(pdf_text)

            st.write("⏳ Converting to embeddings...")
            # STEP 3: Convert to embeddings
            embeddings, model = convert_to_embeddings(st.session_state.text_chunks)
            st.session_state.ai_model = model

            st.write("⏳ Creating search database...")
            # STEP 4: Create searchable database
            st.session_state.search_database = create_search_database(embeddings)

            # Mark as processed
            st.session_state.pdf_processed = True
            st.session_state.pdf_name = uploaded_file.name

            st.success(f"✅ Done! Processed {len(st.session_state.text_chunks)} chunks")

# Show processing status
if st.session_state.get('pdf_processed'):
    st.sidebar.success(f"📄 {st.session_state.get('pdf_name', 'PDF')} is loaded!")
    st.sidebar.info(f"Ready with {len(st.session_state.text_chunks)} chunks")

# Main area - Ask questions
st.header("Step 2: Ask Questions")

if st.session_state.text_chunks is None:
    st.info("👈 Please upload a PDF from the sidebar first")
else:
    st.success(f"✅ PDF loaded with {len(st.session_state.text_chunks)} chunks ready!")

    # Input box for question
    question = st.text_input("Ask a question about your PDF:", key="question_input")

    # Create button
    ask_clicked = st.button("Get Answer", key="ask_button", type="primary")

    if ask_clicked:

        if not question:
            st.warning("⚠️ Please enter a question first!")
        elif not api_key:
            st.error("⚠️ Please enter your X.AI API key in the sidebar!")
        else:
            # Process the question
            with st.spinner("Processing your question..."):
                try:
                    st.write("🔍 Searching for relevant information...")

                    # STEP 5: Find relevant chunks
                    relevant_info = find_relevant_chunks(
                        question,
                        st.session_state.ai_model,
                        st.session_state.search_database,
                        st.session_state.text_chunks
                    )

                    if not relevant_info:
                        st.error("❌ Could not find relevant information in the PDF")
                    else:
                        st.success(f"✅ Found {len(relevant_info)} relevant chunks")

                        # Combine relevant chunks into one context
                        context = "\n\n".join(relevant_info)

                        st.write("🤖 Asking X.AI's Grok...")

                        # STEP 6: Get answer from X.AI
                        answer = ask_grok(question, context, api_key)

                        st.success("✅ Got response!")

                        # Store in session state
                        st.session_state.last_answer = answer
                        st.session_state.last_question = question
                        st.session_state.relevant_chunks = relevant_info

                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")

    # Display the answer (either fresh or from session state)
    if st.session_state.get('last_answer'):
        st.markdown("---")
        st.markdown("### 💡 Answer:")
        st.write(st.session_state.last_answer)

        st.markdown(f"**Question:** {st.session_state.last_question}")

        # Show what information was used (optional)
        if st.session_state.get('relevant_chunks'):
            with st.expander("📄 Click to see the relevant text from PDF"):
                for i, chunk in enumerate(st.session_state.relevant_chunks, 1):
                    st.markdown(f"**Piece {i}:**")
                    st.text(chunk[:200] + "..." if len(chunk) > 200 else chunk)
                    st.markdown("---")
