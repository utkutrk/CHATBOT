# FİNANSAL CHATBOT

Bu proje,finansal anlamda aklınıza takılan soruları cevaplayan merak ettiğiniz terimlerin anlamlarını ve kullanım alanlarını söyleyen bir chatbottur.

![Proje Ekran Görüntüsü](BURAYA_RESİM_URLSİ_GELECEK.png)

## Proje Hakkında

Chatbot'un temel amacı RAG mimarisini kullanarak huggingfaceden veri çeker ve finansal sorularınızı yanıtlar. Kullanıcının sorusuna en uygun bilgi parçacıkları veri tabanından bulunur ve bu bilgiler Gemini modeliyle sentezlenerek tutarlı ve doğru bir cevap üretilir..

## Bu projede kullanılan teknolojiler:

Streamlit: Arayüz tasarımı için
Huggingface: Veri setini çekmek için
SentenceTransformers: Metinleri vektöre çevirmek için
FAISS: Vektör benzerlik araması için
Gemini API: En uygun cevabı üretmek için

## Deploy linki

⬇️Aşağıdaki linkten chatbotu bilgisayarınıza kurmadan direkt tarayıcıdan ulaşabilirsiniz.⬇️

- https://chatbot-ho54eaxtqycwqz4gt3c8k7.streamlit.app/

## Özellikler ve Kullanım Alanları
Veri seti çok kapsamlı bir veri seti değildir bazı terimler mevcut olmayabilir ama çoğu finansal terim mevcuttur.
finans ile ilgili terimler hakkında bilgi alabilir.Yatırım tercihleriniz hakkında yorum soruları sorabilirsiniz.
Örnek sorular ve daha fazla bilgi websitesin sol üst köşesinde mevcuttur.

<img width="300" height="284" alt="Ekran görüntüsü 2025-10-18 15095" src="https://github.com/user-attachments/assets/35b99748-d826-4606-baaf-6d7d44ecf817" />




## Kurulum (Installation) Özellikler ve Kullanım Alanları

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

1.  Repoyu klonlayın:
    ```bash
    git clone [https://github.com/utkutrk/CHATBOT.git](https://github.com/utkutrk/CHATBOT.git)
    ```
2.  Proje klasörüne gidin:
    ```bash
    cd CHATBOT
    ```
3.  Gerekli kütüphaneleri yükleyin (Eğer varsa):
    ```bash
    pip install -r requirements.txt
    ```
4.  Programı çalıştırın:
    ```bash
    python main.py
    ```

## Kullanım

Projeyi çalıştırdıktan sonra, konsol üzerinden chatbot ile sohbet etmeye başlayabilirsiniz.

[Buraya chatbot ile nasıl etkileşime geçileceğine dair kısa bir örnek ekleyin.]
