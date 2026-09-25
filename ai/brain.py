import os
from google import genai
from google.genai import types


class LinaBrain:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError("GEMINI_API_KEY bulunamadı.")

        self.client = genai.Client(api_key=api_key)

        self.system_prompt = """
Sen Lina'sın.

Lina, canlı yayınlarda kullanılan eğlenceli bir yapay zeka karakteridir.

Konuşma tarzın:
- Türkçe konuş.
- Samimi ve doğal konuş.
- Kısa ve akıcı cevaplar ver.
- Gereksiz uzun açıklamalar yapma.
- Yerine göre espri yap.
- İzleyiciyle sohbet ediyormuş gibi konuş.
- Robot gibi konuşma.
- Sana Lina diye hitap edildiğinde kendini Lina olarak tanıt.
"""

    def ask(self, message):
        response = self.client.models.generate_content(
            model="gemini-3.8-flash",
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                max_output_tokens=300,
                temperature=0.8,
            ),
        )

        return response.text


if __name__ == "__main__":
    lina = LinaBrain()

    cevap = lina.ask(
        "Merhaba Lina, kendini kısaca tanıt ve canlı yayında "
        "izleyicilerle ne yapacağını söyle."
    )

    print(cevap)
