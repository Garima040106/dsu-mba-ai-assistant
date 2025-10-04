import os
from langchain.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def build_vector_db():
    print("=" * 50)
    print("Building University Knowledge Base")
    print("=" * 50)
    
    # Check if knowledge_base directory exists
    if not os.path.exists('knowledge_base'):
        print("ERROR: knowledge_base/ directory not found!")
        print("Please create it and add your documents.")
        return
    
    print("\n[1/5] Loading documents...")
    
    documents = []
    
    # Load PDF files
    try:
        pdf_loader = DirectoryLoader(
            'knowledge_base/', 
            glob="**/*.pdf",  # This means "all PDFs in all subdirectories"
            loader_cls=PyPDFLoader,
            show_progress=True
        )
        pdf_docs = pdf_loader.load()
        documents.extend(pdf_docs)
        print(f"   ✓ Loaded {len(pdf_docs)} PDF documents")
    except Exception as e:
        print(f"   ⚠ No PDFs found or error loading PDFs: {e}")
    
    # Load text files
    try:
        txt_loader = DirectoryLoader(
            'knowledge_base/', 
            glob="**/*.txt",
            loader_cls=TextLoader,
            show_progress=True
        )
        txt_docs = txt_loader.load()
        documents.extend(txt_docs)
        print(f"   ✓ Loaded {len(txt_docs)} text documents")
    except Exception as e:
        print(f"   ⚠ No text files found or error loading: {e}")
    
    if len(documents) == 0:
        print("\nERROR: No documents loaded!")
        print("Make sure you have PDF or TXT files in knowledge_base/")
        return
    
    print(f"\n   Total documents loaded: {len(documents)}")
    
    # Split documents into chunks
    print("\n[2/5] Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      # Each chunk is ~500 characters
        chunk_overlap=50,    # 50 character overlap between chunks
        length_function=len,
    )
    texts = text_splitter.split_documents(documents)
    print(f"   ✓ Created {len(texts)} text chunks")
    
    # Create embeddings
    print("\n[3/5] Loading embedding model...")
    print("   (This downloads ~100MB on first run)")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    print("   ✓ Embedding model loaded")
    
    # Create vector database
    print("\n[4/5] Creating vector database...")
    print("   (This may take a few minutes)")
    
    # Remove old database if it exists
    if os.path.exists('./vectordb'):
        import shutil
        shutil.rmtree('./vectordb')
        print("   ✓ Removed old database")
    
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory="./vectordb"
    )
    
    print("\n[5/5] Persisting database to disk...")
    vectordb.persist()
    
    print("\n" + "=" * 50)
    print("✓ SUCCESS! Vector database created")
    print("=" * 50)
    print(f"Location: ./vectordb/")
    print(f"Documents processed: {len(documents)}")
    print(f"Text chunks: {len(texts)}")
    print("\nYou can now run qa_system.py to ask questions!")

if __name__ == "__main__":
    build_vector_db()
