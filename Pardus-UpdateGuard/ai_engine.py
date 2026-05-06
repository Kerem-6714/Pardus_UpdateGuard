import json
import requests

def analyze_with_ai():
    # Scanner'dan gelen veriyi oku
    try:
        with open("updates.json", "r") as f:
            updates = json.load(f)
    except FileNotFoundError:
        print("❌ Hata: updates.json bulunamadı. Önce scanner.py'yi çalıştır!")
        return

    print("🤖 Yapay Zeka analizine başlanıyor...")

    # AI'ya göndereceğimiz komut (Prompt)
    prompt = f"""
    Sen bir Pardus Linux güvenlik uzmanısın. Aşağıdaki güncelleme listesini incele:
    {json.dumps(updates, indent=2)}
    
    Hangi paketler kritik sistem dosyasıdır? Hangileri güncellenirken kullanıcı dikkatli olmalıdır? 
    Kısa, profesyonel ve Türkçe bir analiz raporu sun.
    """

    # Ollama API isteği
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("\n--- 🛡️ GÜVENLİK ANALİZ RAPORU ---")
        print(response.json()['response'])
        # Raporu bir metin dosyasına kaydet
        with open("ai_report.txt", "w", encoding="utf-8") as f:
            f.write(response.json()['response'])
        print("\n✅ Analiz raporu 'ai_report.txt' dosyasına kaydedildi.")
    except Exception as e:
        print(f"❌ AI motoruyla iletişim kurulamadı: {e}")

if __name__ == "__main__":
    analyze_with_ai()