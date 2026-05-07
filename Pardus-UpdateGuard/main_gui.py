import customtkinter as ctk
from PIL import Image, ImageTk
import os
import time
import threading

# Not: ai_engine ve scanner dosyalarının aynı klasörde olduğunu varsayıyoruz.
# Eğer henüz oluşturmadıysan bu importlar hata verebilir, basit fonksiyonlarla simüle edebilirsin.
# from ai_engine import AIAnalyzer
# from scanner import SystemScanner

class UpdateGuardGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Pencere Konfigürasyonu ---
        self.title("Pardus UpdateGuard v1.0")
        self.geometry("700x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- Logo ve Yol Ayarları ---
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.logo_path = os.path.join(self.current_dir, "logo.png")
        if os.path.exists(self.logo_path):
            try:
                # 1. Görseli Pillow ile aç
                pil_img = Image.open(self.logo_path)
                
                # 2. İkon için boyutu küçült (Panelde 2000x2000 çok ağır kaçar, 32x32 yeterlidir)
                pil_img_resized = pil_img.resize((32, 32), Image.LANCZOS)
                
                # 3. Tkinter'in anlayacağı PhotoImage formatına çevir
                self.icon_photo = ImageTk.PhotoImage(pil_img_resized)
                
                # 4. İkonu pencereye ata
                self.wm_iconphoto(False, self.icon_photo)
                
            except Exception as e:
                print(f"Panel ikonu yüklenemedi: {e}")
        # --- Arayüz Elemanlarını Oluştur ---
        self.setup_ui()

    def setup_ui(self):
        # 1. Logo Bölümü
        if os.path.exists(self.logo_path):
            try:
                raw_image = Image.open(self.logo_path)
                self.logo_image = ctk.CTkImage(
                    light_image=raw_image,
                    dark_image=raw_image,
                    size=(160, 160)
                )
                self.logo_label = ctk.CTkLabel(self, image=self.logo_image, text="")
                self.logo_label.pack(pady=(25, 10))
            except Exception as e:
                print(f"Logo yükleme hatası: {e}")

        # 2. Başlık ve Alt Başlık
        self.title_label = ctk.CTkLabel(
            self, 
            text="PARDUS UPDATEGUARD", 
            font=ctk.CTkFont(family="Arial", size=26, weight="bold")
        )
        self.title_label.pack(pady=(0, 5))

        self.subtitle_label = ctk.CTkLabel(
            self, 
            text="AI Destekli Güvenlik ve Güncelleme Denetçisi", 
            font=ctk.CTkFont(size=14, slant="italic"),
            text_color="gray"
        )
        self.subtitle_label.pack(pady=(0, 20))

        # 3. Ana Panel (Status Box)
        self.status_frame = ctk.CTkFrame(self, width=600, height=150)
        self.status_frame.pack(pady=10, padx=40, fill="x")

        self.status_text = ctk.CTkTextbox(
            self.status_frame, 
            height=150, 
            font=("Consolas", 12),
            fg_color="#1a1a1a"
        )
        self.status_text.pack(expand=True, fill="both", padx=10, pady=10)
        self.status_text.insert("0.0", "Sistem taranmaya hazır...\nRTX 4050 ve AI motoru aktif.")

        # 4. İlerleme Çubuğu
        self.progress_bar = ctk.CTkProgressBar(self, width=500)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=20)

        # 5. Butonlar Paneli
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=20)

        self.scan_button = ctk.CTkButton(
            self.button_frame, 
            text="SİSTEMİ TARA", 
            command=self.start_scan_thread,
            font=ctk.CTkFont(size=15, weight="bold"),
            height=45,
            width=200,
            hover_color="#1f538d"
        )
        self.scan_button.grid(row=0, column=0, padx=10)

        self.exit_button = ctk.CTkButton(
            self.button_frame, 
            text="ÇIKIŞ", 
            command=self.quit,
            fg_color="transparent",
            border_width=2,
            text_color="white",
            hover_color="#333333",
            height=45,
            width=100
        )
        self.exit_button.grid(row=0, column=1, padx=10)

    # --- Fonksiyonellik ---

    def log_message(self, message):
        """Textbox'a güvenli bir şekilde mesaj ekler."""
        self.status_text.insert("end", f"\n[>] {message}")
        self.status_text.see("end")

    def start_scan_thread(self):
        """Arayüzün donmaması için taramayı ayrı bir thread'de başlatır."""
        self.scan_button.configure(state="disabled", text="TARANIYOR...")
        thread = threading.Thread(target=self.run_scan_logic)
        thread.start()

    def run_scan_logic(self):
        """Simüle edilmiş AI tarama mantığı."""
        self.log_message("Donanım kontrol ediliyor: NVIDIA GeForce RTX 4050 bulundu.")
        time.sleep(1)
        
        steps = ["Kernel verileri okunuyor...", "Paket listesi analiz ediliyor...", "AI zafiyet taraması yapıyor...", "Güvenlik duvarı kontrol ediliyor..."]
        
        for i, step in enumerate(steps):
            self.log_message(step)
            self.progress_bar.set((i + 1) / len(steps))
            time.sleep(1.2) # İşlem yapılıyormuş gibi bekleme

        self.log_message("TARAMA TAMAMLANDI!")
        self.log_message("Durum: Sisteminiz güncel ve güvende.")
        self.scan_button.configure(state="normal", text="YENİDEN TARA")
        self.progress_bar.set(1)

if __name__ == "__main__":
    app = UpdateGuardGUI()
    app.mainloop()