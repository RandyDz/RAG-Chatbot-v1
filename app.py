import streamlit as st
import time
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from groq import Groq

st.set_page_config(page_title="DISKOMINFO Chatbot ", layout="centered")
st.title("🤖 Chatbot DISKOMINFO")
st.write("Tanyakan apa saja tentang dokumen DISKOMINFO.")


@st.cache_resource # muat model
def init_pipeline(api_key_pinecone, index_name, model_name):

    class SimpleRetriever:
        def __init__(self, api_key, index, model):
            self.model = SentenceTransformer(model)
            self.pc = Pinecone(api_key=api_key)
            self.index = self.pc.Index(index)
        
        def search(self, query, top_k=3):
            # query encode
            query_vector = self.model.encode(query).tolist()
            # search di pinecone
            return self.index.query(vector=query_vector, top_k=top_k, include_metadata=True)
            
    return SimpleRetriever(api_key_pinecone, index_name, model_name)


try:
    
    PINECONE_KEY = st.secrets["PINECONE_API_KEY"]
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    INDEX_NAME = "rag-v1" 
    MODEL_NAME = 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'
    
    retriever = init_pipeline(PINECONE_KEY, INDEX_NAME, MODEL_NAME)
    
    # Inisialisasi Groq Client
    client = Groq(api_key=GROQ_KEY)

except Exception as e:
    st.error(f"Error konfigurasi: {e}. Pastikan API Key sudah diset di Secrets.")
    st.stop()

# Inisialisasi history chat (jika belum ada)
if "messages" not in st.session_state:
    st.session_state.messages = []

# tampilkan riwayat chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# user input
if prompt := st.chat_input("Apa yang ingin Anda tanyakan?"):
    # save and display pesan dari user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # proses jawab
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # retrieval
        search_results = retriever.search(prompt, top_k=3)
        
        contexts = []
        sources = set()
        for match in search_results['matches']:
            if match['score'] > 0.4: # Filter relevansi
                text = match['metadata']['text']
                source = match['metadata'].get('source', 'Unknown')
                contexts.append(f"Isi: {text}\nSumber: {source}")
                sources.add(source)
        
        context_str = "\n---\n".join(contexts) if contexts else ""
        
        # 2. generate jawaban
        if not context_str:
            full_response = "Maaf, tidak ditemukan informasi relevan di dokumen."
        else:
            sys_prompt = f"""
            Jawab pertanyaan berdasarkan konteks berikut. Bahasa Indonesia formal.
            Jika tidak ada di konteks, bilang tidak tahu.
            
            Konteks:
            {context_str}
            """
            
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.1
                )
                full_response = chat_completion.choices[0].message.content
                
                # info sumber jawaban di bawah
                if sources:
                    full_response += f"\n\n\n*Sumber: {', '.join(sources)}*"
                    
            except Exception as e:
                full_response = f"Terjadi kesalahan pada AI: {str(e)}"

        # show jawaban
        message_placeholder.markdown(full_response)
        
    # save to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})