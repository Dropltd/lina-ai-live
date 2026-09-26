import os
import glob
import subprocess
from pathlib import Path

# =========================================================
# LINA AI - AVATAR ANIMASYON MOTORU
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
FRONT_DIR = BASE_DIR / "front"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


def find_avatar():
    """
    front klasöründeki ilk uygun avatar görselini bulur.
    """

    extensions = ["*.png", "*.jpg", "*.jpeg", "*.webp"]

    for ext in extensions:
        files = glob.glob(str(FRONT_DIR / ext))

        if files:
            return files[0]

    raise FileNotFoundError(
        "❌ Avatar bulunamadı!\n"
        "avatar/front klasörüne PNG veya JPG avatar yükle."
    )


def check_audio(audio_path):
    """
    Ses dosyasının mevcut olup olmadığını kontrol eder.
    """

    if not os.path.exists(audio_path):
        raise FileNotFoundError(
            f"❌ Ses dosyası bulunamadı: {audio_path}"
        )

    return True


def create_talking_avatar(audio_path):
    """
    Lina'nın avatarını ses dosyasıyla konuşturur.

    Şimdilik Wav2Lip motoruna hazırlanmış yapı.
    """

    avatar = find_avatar()
    check_audio(audio_path)

    output_video = OUTPUT_DIR / "lina_talking.mp4"

    print("🧠 Lina avatar motoru başlıyor...")
    print(f"👩 Avatar: {avatar}")
    print(f"🎤 Ses: {audio_path}")

    # Wav2Lip klasörü mevcut mu?
    wav2lip_dir = BASE_DIR.parent / "wav2lip"

    if not wav2lip_dir.exists():

        print()
        print("⚠️ Wav2Lip motoru henüz kurulmamış.")
        print()
        print("Avatar bulundu:")
        print(avatar)
        print()
        print("Ses bulundu:")
        print(audio_path)
        print()
        print("✅ Lina avatar sistemi hazır.")
        print("⏳ Şimdi konuşma motorunu bağlayacağız.")

        return None

    inference_script = wav2lip_dir / "inference.py"

    if not inference_script.exists():
        print("❌ Wav2Lip inference.py bulunamadı.")
        return None

    command = [
        "python",
        str(inference_script),
        "--checkpoint_path",
        str(wav2lip_dir / "checkpoints" / "wav2lip_gan.pth"),
        "--face",
        str(avatar),
        "--audio",
        str(audio_path),
        "--outfile",
        str(output_video)
    ]

    print("🎬 Lina konuşuyor...")

    subprocess.run(command, check=True)

    print()
    print("✅ Lina videosu oluşturuldu!")
    print(f"📹 Çıktı: {output_video}")

    return str(output_video)


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("====================================")
    print("        LINA AVATAR ENGINE")
    print("====================================")

    print()

    try:
        avatar = find_avatar()

        print("👩 Lina avatarı bulundu:")
        print(avatar)

        print()
        print("✅ Avatar sistemi çalışıyor.")
        print()
        print("Bir sonraki aşamada:")
        print("🎤 XTTS sesi")
        print("➡️")
        print("👄 Lina'nın konuşan yüzü")
        print("➡️")
        print("📹 1080x1920 dikey video")
        print("➡️")
        print("📱 TikTok LIVE")
        print()

    except Exception as e:

        print()
        print("❌ HATA:")
        print(e)
