import json
import os

class ConfigHandler:
    # Projenin ana ayar dosyasının adı
    CONFIG_FILE = "config.json"

    # Kullanıcı ilk kez açtığında yüklenecek varsayılan ayarlar
    DEFAULT_SETTINGS = {
        "appearance_mode": "Dark",      # Dark, Light, System
        "ai_sensitivity": "Dengeli",     # Paranoyak, Dengeli, Esnek
        "ignore_list": [],               # Güncellemede taranmayacak paketler
        "notifications": True            # Masaüstü bildirimleri aktif mi?
    }

    @classmethod
    def load_config(cls):
        """Ayarları JSON dosyasından okur. Dosya yoksa veya bozuksa varsayılanı yaratır."""
        if not os.path.exists(cls.CONFIG_FILE):
            cls.save_config(cls.DEFAULT_SETTINGS)
            return cls.DEFAULT_SETTINGS
        
        try:
            with open(cls.CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                # Yeni eklenen ayarlar varsa ve eski dosyada yoksa diye koruma (Merge)
                for key, value in cls.DEFAULT_SETTINGS.items():
                    if key not in config:
                        config[key] = value
                return config
        except (json.JSONDecodeError, IOError):
            # Dosya bozuksa yedekle ve varsayılanı yükle
            return cls.DEFAULT_SETTINGS

    @classmethod
    def save_config(cls, settings):
        """Ayarları güvenli ve atomik bir şekilde JSON dosyasına yazar."""
        try:
            with open(cls.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            return True
        except IOError:
            print("[-] Ayarlar dosyasına yazma hatası oluştu!")
            return False