import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(page_title="AI Hediye Danışmanı", page_icon="🎁", layout="centered")

api_key = os.getenv("GEMINI_API_KEY")


def build_prompt(recipient, interests, budget, tone):
    return f"""
    Sen yaratıcı ama gerçekçi hediye önerileri üreten bir hediye danışmanısın.

    Kullanıcı bilgileri:
    - Hediye alınacak kişi: {recipient}
    - İlgi alanları: {interests}
    - Bütçe: {budget}
    - Hediye tarzı: {tone}

    Lütfen tam olarak 3 hediye önerisi ver.

    Her öneride şu başlıklar olsun:
    1. Hediye Adı
    2. Neden Uygun?
    3. Tahmini Bütçe
    4. Sunum Notu

    Cevap Türkçe olsun.
    """


def get_gift_suggestions(api_key, prompt):
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


st.title("🎁 AI Hediye Danışmanı")
st.markdown("Hediye seçmeyi kolaylaştıran basit bir AI destekli öneri uygulaması.")
st.markdown("---")

recipient = st.text_input("Hediye kime alınacak?")
interests = st.text_area("Kişinin ilgi alanları neler?")
budget = st.selectbox(
    "Bütçe aralığı",
    ["0-250 TL", "250-500 TL", "500-1000 TL", "1000+ TL"]
)
tone = st.selectbox(
    "Hediye tarzı",
    ["Romantik", "Eğlenceli", "Klasik", "Anlamlı", "Teknolojik"]
)

if st.button("Önerileri Getir"):
    if not recipient or not interests:
        st.warning("Lütfen gerekli alanları doldur.")
    elif not api_key:
        st.error("API key bulunamadı. .env dosyasını kontrol et.")
    else:
        try:
            prompt = build_prompt(recipient, interests, budget, tone)

            with st.spinner("Hediye önerileri hazırlanıyor..."):
                suggestions = get_gift_suggestions(api_key, prompt)

            st.success("Öneriler hazır.")
            st.subheader("🎁 Hediye Önerileri")
            st.write(suggestions)

        except Exception as e:
            st.error("Şu anda öneriler alınamadı. Lütfen tekrar dene.")
            st.caption(str(e))

st.markdown("---")
st.caption("Bu öneriler yapay zekâ tarafından oluşturulmuştur.")