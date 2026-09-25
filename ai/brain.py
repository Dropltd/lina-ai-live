from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "lina.json"


def load_persona():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def build_prompt(user_message):
    persona = load_persona()

    name = persona["name"]
    language = persona["language"]
    personality = persona["personality"]

    return f"""
Sen {name} isimli sanal bir AI yayıncısısın.

Dil: {language}
Tarz: {personality["style"]}
Ton: {personality["tone"]}
Mizah: {personality["humor"]}

Kısa, doğal ve günlük konuş.
İzleyiciyle sohbet ediyormuş gibi cevap ver.
Asla gerçek bir insan olduğunu iddia et.

İzleyicinin mesajı:
{user_message}
""".strip()


class LinaBrain:
    def __init__(self):
        self.persona = load_persona()

    def create_prompt(self, user_message):
        return build_prompt(user_message)
