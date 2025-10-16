# chat_gemini.py

# import os  # Artık buna ihtiyacımız yok
# from dotenv import load_dotenv # Artık buna ihtiyacımız yok
import streamlit as st # YENİ: Streamlit kütüphanesini import ediyoruz
import google.generativeai as genai

def ensure_api_key():
    """
    Streamlit secrets'tan API anahtarını yükler ve kontrol eder.
    """
    # DEĞİŞTİRİLDİ: .env yerine st.secrets kullanıyoruz
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except KeyError:
        # st.secrets içinde anahtar bulunamazsa hata verir
        raise KeyError("GEMINI_API_KEY bulunamadı. Lütfen Streamlit secrets'ı yapılandırın.")
    
    if not api_key:
        raise ValueError("GEMINI_API_KEY secret'ı boş olamaz.")
        
    return api_key

class GeminiClient:
    def __init__(self):
        """
        API anahtarını Streamlit secrets'tan yükler ve Google Generative AI'ı yapılandırır.
        """
        try:
            self.api_key = ensure_api_key()
            genai.configure(api_key=self.api_key)
        except ImportError:
            raise ImportError("google-generativeai kütüphanesini yükleyin: pip install google-generative-ai")
        except Exception as e:
            raise RuntimeError(f"API yapılandırması sırasında bir hata oluştu: {e}")
            
    # generate_text fonksiyonu aynı kalabilir, burada bir değişiklik yok
    def generate_text(self, prompt: str, model: str = "gemini-1.5-flash", max_output_tokens: int = 512) -> str:
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

# Bu test bölümünü şimdilik olduğu gibi bırakabiliriz,
# ancak lokalde çalıştırırken secrets dosyasının olması gerekir.
if __name__ == "__main__":
    # Bu bölümün lokalde çalışması için .streamlit/secrets.toml dosyanızın olması gerekir.
    # Aksi takdirde "KeyError" alırsınız.
    try:
        client = GeminiClient()
        response_text = client.generate_text("Merhaba, nasılsın?")
        print(response_text)
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        print("\nLokalde test için projenizin ana dizininde '.streamlit/secrets.toml' dosyası oluşturduğunuzdan emin olun.")
