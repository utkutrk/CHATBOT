# FİNANSAL CHATBOT

Bu proje,finansal anlamda aklınıza takılan soruları cevaplayan merak ettiğiniz terimlerin anlamlarını ve kullanım alanlarını söyleyen bir chatbottur.

## Proje Hakkında

Chatbot'un temel amacı RAG mimarisini kullanarak huggingfaceden veri çeker ve finansal sorularınızı yanıtlar. Kullanıcının sorusuna en uygun bilgi parçacıkları veri tabanından bulunur ve bu bilgiler Gemini modeliyle sentezlenerek tutarlı ve doğru bir cevap üretilir.

## Bu projede kullanılan teknolojiler:

- Streamlit: Arayüz tasarımı için
- Huggingface: Veri setini çekmek için 
- SentenceTransformers: Metinleri vektöre çevirmek için
- FAISS: Vektör benzerlik araması için
- Gemini API: En uygun cevabı üretmek için (gemini-2.0-flash)

## Deploy linki

⬇️Aşağıdaki linkten chatbotu bilgisayarınıza kurmadan direkt tarayıcıdan ulaşabilirsiniz.⬇️

- https://chatbot-ho54eaxtqycwqz4gt3c8k7.streamlit.app/

## Özellikler ve Kullanım Alanları

- Veri seti çok kapsamlı bir veri seti değildir bazı terimler mevcut olmayabilir ama çoğu finansal terim mevcuttur.
- Finans ile ilgili terimler hakkında bilgi alabilir.Yatırım tercihleriniz hakkında yorum soruları sorabilirsiniz.
- Örnek sorular ve daha fazla bilgi websitenin sol üst köşesinde mevcuttur.
- Sorulan soruların, veri setinin hangi kısmından alındığı bilgisi chatbotun yanıtının altında bulunmaktadır.(sayfanın en altında)

https://github.com/user-attachments/assets/6304cb60-0513-452b-bd50-19161b16c81b

## Kurulum

- Projeyi 2 farklı şekilde çalıştırabilirsiniz:
- 1️⃣Deploy linki başlığı altındaki linkten kurulumsuz çalıştırabilirsiniz.
- 2️⃣Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

1.  Repoyu klonlayın:
    ```bash
    git clone https://github.com/utkutrk/CHATBOT.git
    cd CHATBOT
    ```
2.  Sanal ortam oluşturma ve çalıştırma:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```
3.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```
4.  Bir .env dosyası oluşturun ve Google API anahtarınızı ekleyin:
    ```bash
    GEMINI_API_KEY=your_api_key
    ```
4.  Programı çalıştırın:
    ```bash
    python data_loader.py 
    streamlit run app.py
    ```
## İletişim

- E-mail: utku.trkk@gmail.com
- GitHub: https://github.com/utkutrk
- LinkedIn: https://linkedin.com/in/utkutrk

## Proje yapısı

    CHATBOT/                
    ├── index/                 
    │   ├── faiss_index.bin           
    │   └── metadata.json  
    ├── app.py
    ├── chat_gemini.py                
    ├── data_loader.py             
    ├── requirements.txt       
    └── README.md              

