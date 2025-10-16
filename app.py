# app.py
import os  #İşletim sistemiyle ilgili işlemler yapmak için kullanılır dosya yollarını birleştirmek gibi
import streamlit as st # Web arayüzünü oluşturmak ve yönetmek için kullanılır 
import faiss #kullanıcının sorusuna en çok benzeyen metinleri bulmak için kullanılır.
import json #Metinler hakkındaki ek bilgileri (metadata) okumak için kullanılır.
import numpy as np #sayısal hesaplamalar için
from sentence_transformers import SentenceTransformer #Metinleri anlamsal olarak temsil eden sayısal vektörlere (embedding) dönüştürmek için kullanılır.
from chat_gemini import GeminiClient #Gemini dil modeliyle iletişim kurmak için

INDEX_DIR = "./index"
INDEX_FILE = os.path.join(INDEX_DIR, "faiss_index.bin")
META_FILE = os.path.join(INDEX_DIR, "metadata.json")
EMB_MODEL_NAME = "all-MiniLM-L6-v2"  #kullanılan embedding modelini seçtiğimiz yer

@st.cache_resource  #Bu fonksiyon, uygulamanın ihtiyaç duyduğu büyük dosyaları ve modelleri hafızaya yükler.böylece her seferinde yeniden yüklenmez, hafızada tutulur. Bu da uygulamanın çok daha hızlı çalışmasını sağlar.
def load_resources():
    if not os.path.exists(INDEX_FILE) or not os.path.exists(META_FILE):
        raise FileNotFoundError("Index veya metadata bulunamadı. Önce data_loader.py çalıştır.")
    idx = faiss.read_index(INDEX_FILE)
    with open(META_FILE, "r", encoding="utf-8") as f:
        meta = json.load(f)
    encoder = SentenceTransformer(EMB_MODEL_NAME)
    gemini = GeminiClient()
    return idx, meta, encoder, gemini

#Bu fonksiyon, RAG mimarisinin "Retrieval" (Getirme) adımını gerçekleştirir.
def retrieve(idx, encoder, texts_meta, query: str, top_k: int = 5):
    q_emb = encoder.encode([query], convert_to_numpy=True)
    D, I = idx.search(np.asarray(q_emb, dtype=np.float32), top_k) #bu komut ile sorgu vektörüne en çok benzeyen top_k adet vektör, faiss indexi içinde bulunur.
    results = []
    for dist, idx_ in zip(D[0], I[0]): #burda bulunan vektörlerin ID'leri (I) ve ne kadar benzediklerini gösteren uzaklık puanları (D) elde edilir.
        if idx_ < 0:
            continue
        results.append({
            "text": texts_meta["texts"][int(idx_)],
            "meta": texts_meta["metas"][int(idx_)],
            "score": float(dist)
        })
    return results

#Bu bölüm, kullanıcının gördüğü web sayfasını oluşturur.
st.set_page_config(page_title="Finansal Chatbot U♥️Ö", layout="wide") #tarayıcı başlığı ve sayfa düzeni

#sayfanın sol tarafındaki menü ayarları burda yapılır.
with st.sidebar:
    st.header("MENÜ")

    with st.expander("Kullanım"):
        st.write("""
        - Ana ekrandaki arama çubuğuna merak ettiğiniz soruları yazıp "Sor" tuşuna basarak veya "Enter" tuşuna basıp arama yapabilirsiniz. 
        - Chatbot cevap üretiğinde en altta çıkan "📚 Kullanılan Kaynaklar" kısmından veri setinden bulup,kullandığı bilgilere erişebilirsiniz.
        """)

    with st.expander("Örnekler"):
        st.write("""
        Chatbota sorulabilecek örnek birkaç soru ⬇️
        - Uzun vadede hangi yatırımlar mantıklı?
        - Türkiye ekonomisi hakkında ne düşünüyorsun?
        - Enflasyon ile nasıl mücadele edilir?
        - Bilanço nedir?
        - Altın mı Dolar mı daha uzun vadeli yatırım?
        """)
    
    with st.expander("Hakkında"):
        st.write("""
        Bu uygulama, RAG mimarisini kullanarak "umarigan/turkiye_finance_qa" veri setinden veri çeker ve finansal sorularınızı yanıtlar. 
        Kullanıcının sorusuna en uygun bilgi parçacıkları veri tabanından bulunur ve bu bilgiler Gemini modeliyle sentezlenerek tutarlı ve doğru bir cevap üretilir.
        """)

    with st.expander("İçerik"):
        st.write("""
        Bu projede kullanılan teknolojiler:
        - **Streamlit:** Arayüz için
        - **Huggingface:** Veri setini çekmek için
        - **SentenceTransformers:** Metinleri vektöre çevirmek için
        - **FAISS:** Vektör benzerlik araması için
        - **Gemini API:** En uygun cevabı üretmek için
        """)



st.title("📉FİNANSAL CHATBOT (Türkçe)")  #Sayfanın ana başlığını yazar

st.markdown("Bu chatbot finans ile ilgili sorularınızı yanıtlamak üzerine tasarlanmıştır.") #sayfanın açıklaması

try:
    idx, texts_meta, encoder, gemini = load_resources()
except Exception as e:
    st.error(f"Yükleme hatası: {e}")
    st.stop()


with st.form(key="search_form"):
    col1, col2 = st.columns([6, 1])
    with col1:
        query = st.text_input("Bir soru yazın:", value="Türkiye ekonomisi hakkında ne düşünüyorsun?", label_visibility="collapsed", placeholder="Bir soru yazın...") #prompt girilen kutucuğun oluşturulduğu yerdir
    with col2:
        
        submitted = st.form_submit_button("Sor")# butona tıklandığında yazılan prompt için arama yapar.


top_k = 5  
model_name = "gemini-2.0-flash"



# form'un gönderilip gönderilmediğini ve input'un boş olmadığını kontrol eden yer.
if submitted and query.strip():
    with st.spinner("Veriler alınıyor..."):  #işlem yapılırken kullanıcıya bir yükleme animasyonu gösterir
        results = retrieve(idx, encoder, texts_meta, query, top_k=top_k)

    context = "\n\n".join([f"Paragraf {i+1}: {r['text']}" for i, r in enumerate(results)]) # fonksiyonundan dönen metinler Geminiye "bağlam" olarak verilebilmek için tek bir metin bloğu haline getirilir.
    # Gemini modeline ne yapması gerektiğini söyleyen bir (prompt) oluşturulur.görev verir.
    prompt = f"""Sen bir finans uzmanısın. Aşağıdaki bağlamı kullanarak soruyu yanıtla. 
Bağlam:
{context}

Soru: {query}
Türkçe ve net bir cevap ver, kaynaklardan yararlandığını belirt."""

    with st.spinner("Gemini cevap oluşturuyor..."):
        try:
            answer = gemini.generate_text(prompt, model=model_name, max_output_tokens=600) #Geminiden bir cevap üretmesi istenir.
        except Exception as e:
            st.error(f"Gemini çağrısında hata: {e}")
            answer = None
# cevabı ekrana yazdırır.
    if answer:
        st.subheader("💬 Gemini Cevabı")
        st.write(answer)
        st.markdown("---")

# prompta göre veri setindeki kullanılan verileri listeler.
    with st.expander("📚 Kullanılan Kaynaklar"):
        for i, r in enumerate(results):
            st.write(f"**{i+1}.** (puan={r['score']:.4f})")
            st.write(r["text"])
            st.write(r["meta"])
            st.markdown("---")
