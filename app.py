from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from llama_cpp import Llama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os
from datetime import datetime
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Global variables for model
qa_system = None

class UniversityQA:
    def __init__(self):
        print("🚀 Initializing DSU MBA QA System...")
        
        # Load Llama model
        print("📥 Loading language model...")
        self.llm = Llama(
            model_path=app.config['MODEL_PATH'],
            n_ctx=app.config['N_CTX'],
            n_threads=app.config['N_THREADS'],
            n_gpu_layers=0,
            verbose=False
        )
        print("✅ Model loaded successfully")
        
        # Load embeddings
        print("📥 Loading embeddings...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        print("✅ Embeddings loaded successfully")
        
        # Load vector database
        print("📥 Loading knowledge base...")
        self.vectordb = Chroma(
            persist_directory=app.config['VECTORDB_PATH'],
            embedding_function=self.embeddings
        )
        print("✅ Knowledge base loaded successfully")
        print("🎉 System ready to answer questions!\n")
    
    def answer_question(self, question):
        try:
            # Retrieve relevant documents
            docs = self.vectordb.similarity_search(
                question, 
                k=app.config['TOP_K_DOCUMENTS']
            )
            
            if not docs:
                return {
                    'success': False,
                    'answer': "I couldn't find relevant information in the MBA department knowledge base.",
                    'sources': [],
                    'confidence': 'low'
                }
            
            # Build context
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Create prompt
            prompt = f"""You are an AI assistant for Dayananda Sagar University's MBA Department. Answer questions accurately based on official MBA department documents.

Context from MBA Department documents:
{context}

Question: {question}

Provide a clear, professional answer based ONLY on the context above. If the information is not in the context, politely say so.

Answer:"""
            
            # Generate response
            response = self.llm(
                prompt,
                max_tokens=app.config['MAX_TOKENS'],
                temperature=app.config['TEMPERATURE'],
                top_p=0.9,
                echo=False,
                stop=["Question:", "\n\nQuestion:", "Context:"]
            )
            
            answer = response['choices'][0]['text'].strip()
            
            # Extract sources
            sources = []
            for doc in docs:
                source = doc.metadata.get('source', 'Unknown')
                source = source.replace('./knowledge_base/', '')
                sources.append(source)
            
            return {
                'success': True,
                'answer': answer,
                'sources': list(set(sources)),
                'confidence': 'high' if len(docs) >= 2 else 'medium',
                'num_sources': len(docs)
            }
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return {
                'success': False,
                'answer': f"An error occurred: {str(e)}",
                'sources': [],
                'confidence': 'low'
            }

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html',
                         university=app.config['UNIVERSITY_NAME'],
                         department=app.config['DEPARTMENT_NAME'])

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """API endpoint to answer questions"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({
                'success': False,
                'error': 'Please provide a question'
            }), 400
        
        # Get answer from QA system
        result = qa_system.answer_question(question)
        result['timestamp'] = datetime.now().isoformat()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'university': app.config['UNIVERSITY_NAME'],
        'department': app.config['DEPARTMENT_NAME'],
        'model_loaded': qa_system is not None
    })

@app.before_request
def initialize_qa():
    """Initialize QA system before first request"""
    global qa_system
    if qa_system is None:
        qa_system = UniversityQA()

if __name__ == '__main__':
    print("\n" + "="*60)
    print(f"🎓 {app.config['UNIVERSITY_NAME']}")
    print(f"📚 {app.config['DEPARTMENT_NAME']} - AI Assistant")
    print("="*60 + "\n")
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
