# data_loader.py
import os
import json
from datasets import load_dataset #Hugging Facedeki veri setini kolayca indirmek için kullanılır.
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

#Oluşturulacak index ve metadata dosyalarını kapsayan kod bloğu.
INDEX_DIR = "./index"
INDEX_FILE = os.path.join(INDEX_DIR, "faiss_index.bin")
META_FILE = os.path.join(INDEX_DIR, "metadata.json")
EMB_MODEL_NAME = "all-MiniLM-L6-v2"  # embedding modeli

#Bu fonksiyon index oluşturma işleminin tüm mantığını içerir.
def build_index(rebuild: bool = False, max_rows: int | None = None):
    #rebuild=false eğer dosyalar zaten varsa işlemi atlar.
    #Veri setinin tamamı yerine sadece belirli sayıda satırı işlemek için kullanılır. Test amaçlı.
    os.makedirs(INDEX_DIR, exist_ok=True)

    if os.path.exists(INDEX_FILE) and os.path.exists(META_FILE) and not rebuild:
        print("Index zaten var. Yeniden oluşturmak için rebuild=True kullan.") 
        return

    print("Hugging Face veri seti yükleniyor: umarigan/turkiye_finance_qa") #bilgilendirme amaçlıdır
    ds = load_dataset("umarigan/turkiye_finance_qa") #veri setini indirir ve ds değerine atar

    texts = [] #İşlenmiş metinlerin tutulacağı liste
    metas = []

    # Veri setleri genellikle bölümlere ayrılır.Bu döngü, veri setindeki tüm bölümleri gezer ve her birini tek tek işler.
    for split in ds.keys():
        for i, item in enumerate(ds[split]):

            text = None
            if isinstance(item, dict):
                #veri setinin içeriğidir veri setleri arasında değişiklik gösterir
                instruction = item.get("soru", "") #veri setinde "soru" başlığı varsa değerini, yoksa boş bir string döndürür.
                input_data = item.get("cevap", "")
                
                parts = [instruction, input_data]
                combined_text = " ".join([p.strip() for p in parts if p.strip()]) #Burada "soru" ve "cevap" alanları birleştirilerek tek bir metin oluşturulur.
                
                if combined_text:
                    text = combined_text
                
                #Bu bir yedek mekanizmadır. Eğer yukarıdaki mantık (soru/cevap birleştirilmezse) bir şekilde boş bir metin üretirse
                #bu kod bloğu çalışır ve sözlükteki tüm string türündeki değerleri birleştirerek genel bir metin oluşturur.
                if not text:
                    # Sözlükteki tüm string değerleri birleştir.
                    text = " ".join([str(v) for v in item.values() if isinstance(v, str)])

            else:
                
                text = str(item)

            if not text or text.strip() == "":
                continue
            #çekilen bilginin hangi veri satırından çekildiğini bulmasını sağlar.kontrol amaçlıdır.
            meta = {"split": split, "idx": i}
            texts.append(text)
            metas.append(meta)

            if max_rows and len(texts) >= max_rows:
                break
        if max_rows and len(texts) >= max_rows:
            break

    print(f"{len(texts)} adet metin yüklendi. Embedding oluşturuluyor...")
    encoder = SentenceTransformer(EMB_MODEL_NAME) # texts listesindeki tüm metinleri alır ve her birini bir vektöre dönüştürür
    embeddings = encoder.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim) #FAISS'te bir index oluşturur.arama sorgusu geldiğinde onu indexteki tüm vektörlerle karşılaştırır
    index.add(np.asarray(embeddings, dtype=np.float32))

    faiss.write_index(index, INDEX_FILE) #FAISS indexi kaydeder.
    with open(META_FILE, "w", encoding="utf-8") as f: 
        json.dump({"metas": metas, "texts": texts}, f, ensure_ascii=False)

    print("FAISS index ve metadata kaydedildi.")


#Bu blok, script'in doğrudan komut satırından çalıştırılmasına olanak tanır
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--max", type=int, default=None)
    args = parser.parse_args()
    build_index(rebuild=args.rebuild, max_rows=args.max)
