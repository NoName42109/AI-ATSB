# rag_system.py (ĐẶT Ở THƯ MỤC GỐC)
import os
import PyPDF2
import docx
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class PsychologyRAGSystem:
    def __init__(self):
        self.embedder = SentenceTransformer('keepitreal/vietnamese-sbert')
        self.index = None
        self.chunks = []
        self.knowledge_base = {}
        
    def process_uploaded_files(self, uploaded_files):
        """Xử lý files từ Streamlit upload"""
        processed_files = {}
        
        for uploaded_file in uploaded_files:
            # Lưu file tạm
            file_path = f"./temp_{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Đọc nội dung
            content = self._read_document(file_path)
            if content:
                processed_files[uploaded_file.name] = content
            
            # Xóa file tạm
            os.remove(file_path)
        
        # Thêm vào knowledge base
        for filename, content in processed_files.items():
            self._add_to_knowledge_base(content, filename)
        
        # Build index
        self._build_vector_index()
        
    def _read_document(self, file_path):
        """Đọc các loại tài liệu"""
        try:
            if file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            elif file_path.endswith('.pdf'):
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text
            elif file_path.endswith('.docx'):
                doc = docx.Document(file_path)
                return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            print(f"❌ Lỗi đọc file: {e}")
            return None
    
    def _add_to_knowledge_base(self, content, source):
        """Thêm nội dung vào knowledge base"""
        paragraphs = [p.strip() for p in content.split('\n\n') if len(p.strip()) > 50]
        for i, para in enumerate(paragraphs):
            chunk_id = f"{source}_chunk_{i}"
            self.knowledge_base[chunk_id] = para
            self.chunks.append(para)
    
    def _build_vector_index(self):
        """Xây dựng vector index"""
        if not self.chunks:
            return
            
        embeddings = self.embedder.encode(self.chunks)
        embeddings = np.array(embeddings).astype('float32')
        
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        print(f"✅ Đã tạo vector index với {self.index.ntotal} vectors")
    
    def search_similar(self, query, top_k=3):
        """Tìm kiếm thông tin liên quan"""
        if not self.index:
            return []
            
        try:
            query_embedding = self.embedder.encode([query])
            distances, indices = self.index.search(query_embedding, top_k)
            
            results = []
            for i, idx in enumerate(indices[0]):
                if 0 <= idx < len(self.chunks):
                    results.append(self.chunks[idx])
            return results
        except Exception as e:
            print(f"❌ Lỗi tìm kiếm: {e}")
            return []