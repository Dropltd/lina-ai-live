import os
from google import genai


class LinaBrain:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY bulunamadı.")

        self.client = genai.Client(api_key=self.api_key)

        self.system_prompt = """
Sen Lina'sın.

Canlı yayınlarda kullanılan eğlenceli bir yapay zeka karakterisin.

Konuşma tarzın:
- Türkçe konuş.
- Samimi ve doğal ol.
- Kısa ve akıcı cevaplar ver.
- Gereksiz uzun açıklamalar yapma.
- Yerine göre espri yap.
- İzleyiciyle sohbet ediyormuş gibi konuş.
- Robot gibi konuşma.
"""

    def ask(self, message):
        response = self.client.models.generate_content(
            model="gemini-3.8-flash",
            contents=message,
            config={
                "system_instruction": self.system_prompt,
                "max_output_tokens": 300,
            },
        )

        return response.text


if __name__ == "__main__":
    lina = LinaBrain()
    print(lina.ask("Merhaba Lina, kendini kısaca tanıt."))
