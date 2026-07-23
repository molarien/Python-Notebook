import json
import sqlite3
import requests
import numpy as np

# ==========================================
# 1. AYARLAR & YAPILANDIRMA (CONFIG)
# ==========================================
OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "phi3"
DB_NAME = "local_rag.db"

# ==========================================
# 2. FAZ 2: METİN İŞLEME VE VERİ KATMANI
# ==========================================

def chunk_text(text, max_chars=300, overlap=50):
    """
    Metni anlamsal bütünlüğü koruyarak, belirlenen karakter sınırlarına 
    ve overlap (çakışma) miktarına göre cümle bazlı parçalara böler.
    """
    sentences = text.replace('\n', ' ').split('. ')
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if not sentence.strip():
            continue
        sentence = sentence.strip() + "."
    
        if not current_chunk:
            current_chunk = sentence
        elif len(current_chunk) + len(sentence) < max_chars:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk)
            # Bağlam kaybolmasın diye bir önceki parçanın sonunu yeni parçaya ekliyoruz
            overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
            current_chunk = overlap_text + " " + sentence
            
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def get_embedding(text):
    """Ollama API kullanarak yerel embedding (768 boyutlu vektör) üretir."""
    url = f"{OLLAMA_BASE_URL}/api/embeddings"
    payload = {"model": EMBEDDING_MODEL, "prompt": text}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["embedding"]
    except requests.exceptions.RequestException as e:
        print(f"Ollama Embedding Hatası: {e}. Ollama'nın çalıştığından ve '{EMBEDDING_MODEL}' modelinin yüklü olduğundan emin olun.")
        return None

def init_db():
    """SQLite veritabanını ve şemasını hazırlar."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text_content TEXT,
            embedding_json TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(text_content, embedding):
    """Parçalanmış metni ve vektör karşılığını JSON olarak SQLite'a yazar."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO knowledge_base (text_content, embedding_json) VALUES (?, ?)",
        (text_content, json.dumps(embedding))
    )
    conn.commit()
    conn.close()

# ==========================================
# 3. FAZ 3: ARAMA & RETRIEVAL KATMANI
# ==========================================

def retrieve_similar_context(query, top_k=2):
    """
    Kullanıcı sorgusunu vektörleştirir ve SQLite'taki tüm vektörlerle 
    Kosinüs Benzerliği hesaplayarak en yakın top_K parçayı döner.
    """
    query_vector = get_embedding(query)
    if not query_vector:
        return []
        
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT text_content, embedding_json FROM knowledge_base")
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return []
        
    q_vec = np.array(query_vector)
    scored_chunks = []
    
    for text_content, emb_json in rows:
        db_vec = np.array(json.loads(emb_json))
        
        # Kosinüs Benzerliği Formülü: (A . B) / (||A|| * ||B||)
        dot_product = np.dot(q_vec, db_vec)
        norm_q = np.linalg.norm(q_vec)
        norm_db = np.linalg.norm(db_vec)
        
        # Sıfıra bölünme hatasını engelleme güvenlik önlemi
        similarity = dot_product / (norm_q * norm_db) if norm_q * norm_db > 0 else 0
        scored_chunks.append((text_content, similarity))
        
    # En yüksek benzerlik skoruna göre sırala
    scored_chunks.sort(key=lambda x: x[1], reverse=True)
    return scored_chunks[:top_k]

# ==========================================
# 4. FAZ 4: GENERATION (LLM ÜRETİMİ)
# ==========================================

def generate_answer(query, context):
    """Bulunan bağlamı koruyarak yerel LLM üzerinden yanıt üretir."""
    url = f"{OLLAMA_BASE_URL}/api/chat"
    
    system_prompt = (
        "Sen teknik bir eğitim asistanısın. Görevin, sadece sana verilen 'BAĞLAM' (Context) "
        "içindeki bilgileri kullanarak kullanıcının sorusunu yanıtlamaktır.\n"
        "Kurallar:\n"
        "1. Eğer yanıt bağlam içerisinde yoksa, 'Bu bilgi notlarımda bulunmuyor' de ve asla uydurma.\n"
        "2. Tamamen bağlama sadık kal, dışarıdan genel bilgi ekleme."
    )
    
    user_prompt = f"BAĞLAM:\n{context}\n\nSORU:\n{query}"
    
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False,
        "options": {"temperature": 0.1} # Halüsinasyonu engellemek için kararlılık moduna çektik
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Ollama LLM Yanıt Hatası: {e}"

# ==========================================
# 5. BORU HATTI (PIPELINE) KONTROLÜ
# ==========================================

def ingest_sample_data():
    """Eğer veritabanı boşsa sisteme başlangıç için Yapay Sinir Ağları notunu yükler."""
    conn = sqlite3.connect(DB_NAME)
    count = conn.cursor().execute("SELECT COUNT(*) FROM knowledge_base").fetchone()[0]
    conn.close()
    
    if count == 0:
        print("Veritabanı boş algılandı. Örnek Yapay Sinir Ağları notları yükleniyor...")
        sample_notes = (
            "Yapay Sinir Ağları (Artificial Neural Networks), insan beyninin biyolojik yapısını taklit eden algoritmalardır. "
            "Temel yapı taşı yapay nöronlar yani Perceptron'lardır. Bir ağ; girdi katmanı, gizli katmanlar ve çıktı katmanından oluşur. "
            "Katmanlar arasındaki veri akışını ve bağlantı gücünü ağırlıklar (weights) ve sapmalar (biases) belirler. "
            "Eğitim sürecinde, modelin ürettiği hata miktarı hesaplanır ve hata geriye yayılım (backpropagation) algoritması "
            "kullanılarak ağdaki tüm ağırlıklar kademeli olarak güncellenir. Aktivasyon fonksiyonları ise ağa doğrusal olmayan (non-linear) "
            "özellikler katarak karmaşık örüntülerin öğrenilmesini sağlar."
        )
        chunks = chunk_text(sample_notes)
        for chunk in chunks:
            embedding = get_embedding(chunk)
            if embedding:
                save_to_db(chunk, embedding)
        print("Örnek veriler başarıyla indekslendi ve kalıcı SQLite tabanına kaydedildi!\n")

def main():
    init_db()
    ingest_sample_data()
    
    print("YEREL RAG MÜHENDİSLİK ASİSTANINA HOŞ GELDİNİZ ")
    print(f"Aktif Motor: Ollama | Gömme: {EMBEDDING_MODEL} | Üretim: {LLM_MODEL}")
    print("Çıkmak için 'q' veya 'exit' yazabilirsiniz.\n")
    
    while True:
        query = input("\n Sorunuz: ").strip()
        if query.lower() in ['q', 'exit']:
            print("Görüşmek üzere, iyi çalışmalar Emir!")
            break
            
        if not query:
            continue
            
        print("Bilgi tabanında anlamsal arama yapılıyor...")
        matched_results = retrieve_similar_context(query, top_k=2)
        
        if not matched_results:
            print("Veritabanında eşleşen herhangi bir döküman parçası bulunamadı.")
            continue
            
        # Arama sonuçlarını loglayarak arka planda ne döndüğünü mühendis gözüyle inceleyelim
        print(f"\n[RETRIEVAL LOGS]: En yakın {len(matched_results)} parça getirildi:")
        context_parts = []
        for idx, (text, score) in enumerate(matched_results):
            print(f"  -> [{idx+1}] Skor: {score:.4f} | Metin: {text[:60]}...")
            context_parts.append(text)
            
        full_context = "\n\n".join(context_parts)
        
        print("\nYanıt üretiliyor...")
        answer = generate_answer(query, full_context)
        print(f"\n[Cevap]:\n{answer}")
        print("="*60)

if __name__ == "__main__":
    main()