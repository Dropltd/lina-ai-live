import os
import json
from pathlib import Path
from openai import OpenAI


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "lina.json"


def load_persona():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


class LinaBrain:
    def __init__(self):
        self.persona = load_persona()

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError("OPENAI_API_KEY bulunamadı.")

        self.client = OpenAI(api_key=api_key)

    def ask(self, user_message):
        personality = self.persona["personality"]

        system_prompt = f"""
Sen Lina adında sanal bir yayıncı karakterisin.

Dil: {self.persona["language"]}

Kişiliğin:
- Tarz: {personality["style"]}
- Ton: {personality["tone"]}
- Mizah: {personality["humor"]}

Doğal konuş.
Kısa ve anlaşılır cevaplar ver.
Yayın sırasında gerçek bir insanla sohbet ediyormuş gibi davran.
Gereksiz uzun açıklamalar yapma.
"""

        response = self.client.responses.create(
            model="gpt-5-mini",
            instructions=system_prompt,
            input=user_message
        )

        return response.output_text


if __name__ == "__main__":
    lina = LinaBrain()

    cevap = lina.ask("Merhaba Lina, nasılsın?")
    print(cevap)
