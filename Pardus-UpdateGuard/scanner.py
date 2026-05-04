import json

# Şimdilik hata almamak için kütüphaneyi devre dışı bırakıyoruz
# Sadece simülasyon verisiyle çalışacağız
def get_upgradable_packages():
    # Bu liste senin 'sahte' veri setin. CachyOS'ta bunu göreceğiz.
    return [
        {"name": "linux-image-amd64", "section": "kernel", "version": "6.1.0"},
        {"name": "firefox-esr", "section": "web", "version": "128.0"},
        {"name": "libc6", "section": "libs", "version": "2.36"}
    ]

if __name__ == "__main__":
    print("--- 🛡️ UpdateGuard Başlatıldı ---")
    packages = get_upgradable_packages()
    
    # Ekrana yazdır
    for p in packages:
        print(f"Bulunan Paket: {p['name']}")
    
    # Dosyaya kaydet
    with open("updates.json", "w") as f:
        json.dump(packages, f, indent=4)
    print("\n✅ updates.json dosyası oluşturuldu.")