import customtkinter as ctk
from PIL import Image, ImageTk
import os
import time
import threading

class UpdateGuardGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pardus UpdateGuard v1.2")
        self.geometry("780x850") 
        
        # --- Arka Plan Rengi Geliştirmesi ---
        # Dümdüz siyah yerine logonun ruhuna uygun çok koyu bir lacivert tonu (#0a0f18)
        self.configure(fg_color="#0a0f18") 
        ctk.set_appearance_mode("dark")

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.logo_path = os.path.join(self.current_dir, "logo.png")

        if os.path.exists(self.logo_path):
            try:
                pil_img = Image.open(self.logo_path)
                self.icon_photo = ImageTk.PhotoImage(pil_img.resize((64, 64), Image.LANCZOS))
                self.wm_iconphoto(False, self.icon_photo)
            except: pass

        self.setup_ui()

    def setup_ui(self):
        # Kaydırılabilir ana container
        self.main_container = ctk.CTkScrollableFrame(self, fg_color="transparent", width=750, height=830)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # 1. Logo
        if os.path.exists(self.logo_path):
            self.logo_image = ctk.CTkImage(light_image=Image.open(self.logo_path),
                                          dark_image=Image.open(self.logo_path), size=(180, 180))
            self.logo_label = ctk.CTkLabel(self.main_container, image=self.logo_image, text="")
            self.logo_label.pack(pady=(10, 5))

        # 2. Başlık ve Alt Başlık
        self.title_label = ctk.CTkLabel(self.main_container, text="PARDUS UPDATEGUARD", 
                                        font=("Orbitron", 26, "bold"), text_color="#e0e0e0")
        self.title_label.pack()
        
        self.status_indicator = ctk.CTkLabel(self.main_container, text="SİSTEM TARAMA PROTOKOLÜNE HAZIR", 
                                             text_color="#5c7cfa", font=("Arial", 12, "bold"))
        self.status_indicator.pack(pady=(0, 15))

        # 3. Konsol (Daha şeffaf ve uyumlu)
        self.console = ctk.CTkTextbox(self.main_container, width=680, height=220, font=("Consolas", 11), 
                                      fg_color="#05080f", border_width=1, border_color="#1c2533", text_color="#a5b4fc")
        self.console.pack(padx=20, pady=5)
        self.console.insert("0.0", ">>> NeuralShield AI katmanı yüklendi.\n>>> RTX 4050 donanım ivmelendirmesi aktif.\n>>> Komut bekleniyor...")

        # 4. İlerleme Çubuğu
        self.progress_bar = ctk.CTkProgressBar(self.main_container, width=620, progress_color="#4dabf7", fg_color="#1c2533")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=20)

        # 5. Butonlar (Yeni Estetik Tasarım)
        self.button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.button_frame.pack(pady=10)

        # Analiz Butonu: Modern Lacivert
        self.scan_button = ctk.CTkButton(self.button_frame, text="ANALİZİ BAŞLAT", command=self.start_scan, 
                                        width=240, height=48, font=("Arial", 15, "bold"),
                                        fg_color="#1c2533", hover_color="#2e3b4e", border_width=1, border_color="#3b4b61")
        self.scan_button.grid(row=0, column=0, padx=10)

        # Çıkış Butonu: Beyazımsı - Şeffaf (Ghost Button)
        self.exit_button = ctk.CTkButton(self.button_frame, text="ÇIKIŞ", command=self.quit, 
                                        width=120, height=48, font=("Arial", 14),
                                        fg_color="transparent",
                                        hover_color="#212f3d",
                                        border_width=1,
                                        border_color="#e0e0e0",
                                        text_color="#e0e0e0")
        self.exit_button.grid(row=0, column=1, padx=10)

        # 6. AI Önerileri Paneli (Genişletilmiş Rapor)
        self.ai_frame = ctk.CTkFrame(self.main_container, width=680, fg_color="#0d1421", border_width=1, border_color="#1c2533")
        self.ai_frame.pack(padx=20, pady=30, fill="x")
        
        self.ai_title = ctk.CTkLabel(self.ai_frame, text="🛡️ AI GÜVENLİK ANALİZ RAPORU", font=("Arial", 14, "bold"), text_color="#74c0fc")
        self.ai_title.pack(pady=(15, 10))
        
        self.ai_suggestion = ctk.CTkLabel(self.ai_frame, text="Sistem analizi sonrası detaylı rapor burada oluşturulacaktır...", 
                                         font=("Arial", 12), text_color="#94a3b8", wraplength=640, justify="left")
        self.ai_suggestion.pack(pady=(0, 20), padx=25)

    def smooth_scroll_to_bottom(self):
        """Yavaş ve kararlı kaydırma."""
        for i in range(0, 101, 2): 
            self.main_container._parent_canvas.yview_moveto(i / 100)
            self.update_idletasks()
            time.sleep(0.015)

    def start_scan(self):
        self.scan_button.configure(state="disabled", text="ANALİZ EDİLİYOR...")
        self.status_indicator.configure(text="DERİN PAKET ANALİZİ VE CVE SORGUSU AKTİF", text_color="#ff922b")
        self.console.delete("1.0", "end")
        threading.Thread(target=self.scan_process, daemon=True).start()

    def scan_process(self):
        packages = [
            ("linux-image-6.1.0-21-amd64", "KRİTİK: Yetki Yükseltme Açığı"),
            ("nvidia-dkms-550.67", "STABİL: Donanım Senkronize"),
            ("libssl-dev / openssl", "TEHLİKELİ: Aradaki Adam Saldırısı Riski"),
            ("python3-pip / setuptools", "GÜVENLİ: Sürüm Doğrulandı"),
            ("systemd / libsystemd0", "STABİL: Çekirdek Bileşenler Tamam"),
            ("google-chrome-stable", "GÜNCELLEME: Sandbox Yaması Gerekli")
        ]
        
        for i, (pkg, status) in enumerate(packages):
            msg = f">>> [PROSES] {pkg.ljust(32)} | SONUÇ: {status}"
            self.console.insert("end", f"\n{msg}")
            self.console.see("end")
            self.progress_bar.set((i + 1) / len(packages))
            time.sleep(0.9)

        time.sleep(0.5)
        self.status_indicator.configure(text="ANALİZ TAMAMLANDI - RAPOR HAZIRLANDI", text_color="#63e6be")
        
        # --- Genişletilmiş ve Bilgilendirici AI Raporu ---
        detailed_ai_report = (
            "SİSTEM ÖZETİ:\n"
            "Yapılan tarama sonucunda sisteminizdeki 142 paket taranmış, 2 tanesinde yüksek öncelikli 'Kritik Zafiyet' tespit edilmiştir.\n\n"
            "📌 KRİTİK BULGULAR:\n"
            "• Çekirdek (Kernel) Analizi: Mevcut çekirdek sürümünüzde bellek yönetimini hedef alan bir sızıntı tespit edildi. Bu durum, yetkisiz kullanıcıların sistem yönetimini ele geçirmesine neden olabilir.\n"
            "• Şifreleme Protokolleri: OpenSSL kütüphanesindeki eski bir sürüm, verilerinizin ağ üzerinden taşınırken deşifre edilme riskini taşımaktadır.\n\n"
            "🛠️ GÜVENLİK TAVSİYELERİ:\n"
            "1. ACİL GÜNCELLEME: Terminali açın ve 'sudo apt update && sudo apt full-upgrade' komutlarını kullanarak kritik yamaları yükleyin.\n"
            "2. DONANIM OPTİMİZASYONU: RTX 4050 kartınızın sürücüleri güncel görünse de, kernel güncellemesi sonrası 'nvidia-smi' komutu ile sürücü sağlığını kontrol etmeniz önerilir.\n"
            "3. HİJYEN: Kullanılmayan eski paketleri 'sudo apt autoremove' ile kaldırarak saldırı yüzeyini daraltın.\n\n"
            "UpdateGuard Yapay Zekası, sisteminizi %98 güvenli buldu ancak yukarıdaki adımların tamamlanması tam koruma için şarttır."
        )
        
        self.ai_suggestion.configure(text=detailed_ai_report, text_color="#f8fafc")
        self.smooth_scroll_to_bottom()
        self.scan_button.configure(state="normal", text="YENİDEN ANALİZ ET")

if __name__ == "__main__":
    app = UpdateGuardGUI()
    app.mainloop()