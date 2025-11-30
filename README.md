# 🤖 DISKOMINFO RAG Chatbot: A Document Assistant 

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rag-chatbot-v1-vzkrkymusbix9rrugjykwf.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Pinecone](https://img.shields.io/badge/Vector%20DB-Pinecone-green)](https://www.pinecone.io/)
[![Groq](https://img.shields.io/badge/LLM-Llama3%20(Groq)-orange)](https://groq.com/)

Aplikasi Chatbot berbasis **Retrieval-Augmented Generation (RAG)** yang dirancang untuk menjawab pertanyaan berdasarkan dokumen internal dan halaman dari Notion secara akurat, faktual, dan cepat.

Proyek ini dibangun untuk mendemonstrasikan bagaimana **Large Language Model (LLM)** dapat digabungkan dengan **Vector Database** untuk mengurangi jawaban halusinasi dan memberikan jawaban berbasis sumber yang valid.

🔗 **Coba Aplikasi:** [Klik di sini untuk mencoba](https://rag-chatbot-v1-vzkrkymusbix9rrugjykwf.streamlit.app/)

---

# Tanyakan berdasarkan dokumen dan Notion berikut:

🔗 **Source** 

📚[Dokumen](https://drive.google.com/drive/folders/1v8XmlQE9tqfx74-5LUJrotVWxyZIPAYx?usp=sharing)
📦[Notion](https://www.notion.so/TESTING-17677ecfd6c98063a562d3b7f10300de)

---

## ✨ Main Utama

* **🔍 Pencarian Cerdas (Semantic Search):** Menggunakan model embedding `paraphrase-multilingual-mpnet-base-v2` untuk memahami konteks pertanyaan dalam Bahasa Indonesia.
* **⚡ Respons Super Cepat:** Menggunakan **Groq API** dengan model **Llama 3**, menghasilkan jawaban dalam hitungan detik.
* **📚 Referensi Sumber:** Setiap jawaban menyertakan sumber dokumen sehingga user dapat melakukan crosscheck langsung terhadap jawaban yang chatbot berikan.


---

## 🛠️ Tech Stack (Teknologi yang Digunakan)

* **Bahasa Pemrograman:** Python
* **Framework UI:** [Streamlit](https://streamlit.io/)
* **Large Language Model (LLM):** llama-3.3-70b-versatile (via Groq API)
* **Vector Database:** [Pinecone](https://www.pinecone.io/) (Serverless)
* **Embedding Model:** `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` (Dimensi: 768)
