# chat_gemini.py
import os
from dotenv import load_dotenv
import google.generativeai as genai  #APİ ile etkileşim kurmak için gerekli kütüphanedir.

def ensure_api_key():  #api anahtarını kontrol eden bölüm
    """
    .env dosyasından API anahtarını yükler ve kontrol eder.
    """
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY ortam değişkeni bulunamadı. Lütfen .env dosyasını kontrol edin.")
    return api_key

class GeminiClient:  #API ile etkileşime giren tüm mantığı bir araya toplayan ana yapıdır.
    def __init__(self):
        """
        API anahtarını yükler ve Google Generative AI'ı yapılandırır.
        """
        try:
            self.api_key = ensure_api_key()
            genai.configure(api_key=self.api_key) #Google AI kütüphanesini yapılandırır. Bu adımdan sonra kütüphane yapacağı tüm API çağrılarında bu anahtarı kullanır
        # kodlar çalışırken bir hata oluşursa program çökmek yerine okunaklı sonuçlar üretir.
        except ImportError:
            raise ImportError("google-generativeai kütüphanesini yükleyin: pip install google-generative-ai")
        except Exception as e:
            raise RuntimeError(f"API yapılandırması sırasında bir hata oluştu: {e}")
       
       # metin üretme işini yapan fonksiyondur.
    def generate_text(self, prompt: str, model: str = "gemini-2.0-flash", max_output_tokens: int = 512) -> str: #sirayla girdi metni,gemini modeli ve üretilen yanıtın maks uzunluğunu belirtir
        """
        Verilen prompt'u kullanarak Gemini modelinden metin üretir.
        
        Not: Güncel API'de max_output_tokens doğrudan generate_content içinde 
        bir parametre değildir. Bu, 'generation_config' içinde ayarlanır.
        """
        try:
            # Model adıyla bir model nesnesi oluşturulur
            model_instance = genai.GenerativeModel(model)
            
            # Üretim ayarları (generation config) oluşturulur
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_output_tokens
            )

            # Asıl API çağrısının yapıldığı yerdir.girdileri sunucuya gönderir
            response = model_instance.generate_content(
                prompt,
                generation_config=generation_config
            )

            
            return response.text
            
        except Exception as e:
            # API'den gelebilecek hataları yakalamak için kullanılır
            raise RuntimeError(f"Gemini API çağrısında hata oluştu: {e}")
# alttaki kodlar kodunuzu test etmek veya doğrudan çalıştırmak için bir giriş noktası görevi görür.
# yani dosyayı import etmeden direkt tek başına çalıştırdığınızda terminale yazı yazıp kontrol sağlamak içindir olmasada kod çalışır.
if __name__ == "__main__":
    try:
        client = GeminiClient()
        response_text = client.generate_text("Merhaba, nasılsın?")
        print(response_text)
    except Exception as e:
        print(e)
