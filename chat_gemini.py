import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st

def ensure_api_key():
    """
    Streamlit Cloud'un secret'larını veya yerel .env dosyasını kullanarak
    API anahtarını güvenli bir şekilde yükler. Hata vermeden kontrol eder.
    """
    # Önce yereldeki .env dosyasını kontrol etmeye çalışırız.
    # Bu, yerel geliştirmeyi önceliklendirir.
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key

    # .env'de anahtar yoksa veya dosya mevcut değilse, Streamlit'in secret'larını deneriz.
    # Bu, Streamlit Cloud'da çalışmasını sağlar.
    try:
        if hasattr(st, 'secrets') and "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            if api_key:
                return api_key
    except Exception:
        # st.secrets erişimi yerelde bazen hata verebilir, bu yüzden es geçiyoruz.
        pass

    # Hiçbir yerde anahtar bulunamazsa hata veririz.
    raise EnvironmentError(
        "GEMINI_API_KEY bulunamadı. Lütfen projenizdeki .env dosyasını "
        "veya Streamlit Cloud Secrets ayarlarınızı kontrol edin."
    )

# --- SINIFINIZIN GERİ KALANI AYNI KALACAK ---

class GeminiClient:
    def __init__(self):
        """
        API anahtarını yükler ve Google Generative AI'ı yapılandırır.
        """
        try:
            self.api_key = ensure_api_key()
            genai.configure(api_key=self.api_key)
        except ImportError:
            raise ImportError("google-generativeai kütüphanesini yükleyin: pip install google-generative-ai")
        except Exception as e:
            # ensure_api_key'den veya genai.configure'dan gelen hatayı yakalar.
            raise RuntimeError(f"API yapılandırması sırasında bir hata oluştu: {e}")

    # --- generate_text fonksiyonu ve diğer kodlar aynı kalacak ---
    def generate_text(self, prompt: str, model: str = "gemini-2.0-flash", max_output_tokens: int = 512) -> str:
        # ... (Bu fonksiyonun içeriği değişmeyecek)
        try:
            model_instance = genai.GenerativeModel(model)
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_output_tokens
            )
            response = model_instance.generate_content(
                prompt,
                generation_config=generation_config
            )
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini API çağrısında hata oluştu: {e}")

# ... (if __name__ == "__main__" bloğu aynı kalacak)
# alttaki kodlar kodunuzu test etmek veya doğrudan çalıştırmak için bir giriş noktası görevi görür.
# yani dosyayı import etmeden direkt tek başına çalıştırdığınızda terminale yazı yazıp kontrol sağlamak içindir olmasada kod çalışır.
if __name__ == "__main__":
    try:
        client = GeminiClient()
        response_text = client.generate_text("Merhaba, nasılsın?")
        print(response_text)
    except Exception as e:
        print(e)
