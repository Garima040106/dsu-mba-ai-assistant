from llama_cpp import Llama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

class UniversityQA:
    def __init__(self, model_path, vectordb_path="./vectordb"):
        print("=" * 50)
        print("Initializing University QA System")
        print("=" * 50)
        
        # Check if model exists
        if not os.path.exists(model_path):
            print(f"ERROR: Model not found at {model_path}")
            print("Please download the model first (Step 2)")
            return
        
        # Check if vectordb exists
        if not os.path.exists(vectordb_path):
            print(f"ERROR: Vector database not found at {vectordb_path}")
            print("Please run build_knowledge_base.py first (Step 4)")
            return
        
        print("\n[1/3] Loading Llama model...")
        print(f"   Model: {model_path}")
        # Load Llama model with CPU optimization
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,      # Context window size
            n_threads=4,     # CPU threads (adjust for your system)
            n_gpu_layers=0,  # CPU only
            verbose=False    # Reduce output noise
        )
        print("   ✓ Model loaded")
        
        print("\n[2/3] Loading embeddings...")
        # Load embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        print("   ✓ Embeddings loaded")
        
        print("\n[3/3] Loading vector database...")
        # Load vector database
        self.vectordb = Chroma(
            persist_directory=vectordb_path,
            embedding_function=self.embeddings
        )
        print("   ✓ Vector database loaded")
        
        print("\n" + "=" * 50)
        print("✓ System Ready!")
        print("=" * 50)
    
    def answer_question(self, question, k=3):
        """
        Answer a question using the knowledge base
        
        Args:
            question: The question to answer
            k: Number of relevant documents to retrieve
        """
        print(f"\n🔍 Searching knowledge base for: '{question}'")
        
        # Retrieve relevant documents
        docs = self.vectordb.similarity_search(question, k=k)
        
        if not docs:
            return {
                'answer': "I couldn't find relevant information in the knowledge base.",
                'sources': [],
                'context': ""
            }
        
        print(f"   ✓ Found {len(docs)} relevant document chunks")
        
        # Build context from retrieved documents
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Create prompt for the model
        prompt = f"""You are a helpful assistant answering questions about a specific university based on official documents.

Context from university documents:
{context}

Question: {question}

Provide a clear, accurate answer based ONLY on the context above. If the context doesn't contain enough information, say so.

Answer:"""
        
        print("   ⚙️  Generating answer...")
        
        # Generate answer
        response = self.llm(
            prompt,
            max_tokens=256,        # Maximum length of answer
            temperature=0.3,       # Lower = more focused, higher = more creative
            top_p=0.9,
            echo=False,
            stop=["Question:", "\n\nQuestion:", "Context:"]
        )
        
        answer = response['choices'][0]['text'].strip()
        
        # Extract sources
        sources = []
        for doc in docs:
            source = doc.metadata.get('source', 'Unknown')
            # Clean up the source path
            source = source.replace('./knowledge_base/', '')
            sources.append(source)
        
        return {
            'answer': answer,
            'sources': list(set(sources)),  # Remove duplicates
            'context': context
        }

def main():
    print("\n")
    print("╔══════════════════════════════════════════════════╗")
    print("║   University Knowledge Base QA System           ║")
    print("╚══════════════════════════════════════════════════╝")
    print()
    
    # Initialize system
    qa = UniversityQA(
        model_path="./models/llama-3.2-1b.Q4_K_M.gguf"
    )
    
    print("\n📚 Ready to answer questions about your university!")
    print("💡 Tip: Ask specific questions about your documents")
    print("⌨️  Type 'quit' or 'exit' to stop\n")
    
    while True:
        try:
            question = input("❓ Your Question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not question:
                continue
            
            # Get answer
            result = qa.answer_question(question)
            
            # Display answer
            print("\n" + "─" * 50)
            print(f"💬 Answer:\n{result['answer']}\n")
            
            if result['sources']:
                print(f"📄 Sources:")
                for i, source in enumerate(result['sources'], 1):
                    print(f"   {i}. {source}")
            
            print("─" * 50 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()
