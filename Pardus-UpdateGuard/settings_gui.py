import customtkinter as ctk
import webbrowser
from config_handler import ConfigHandler

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.title("UpdateGuard - Gelişmiş Ayarlar")
        self.geometry("680x500") # Yan menü için genişliği biraz artırdık
        self.resizable(False, False)
        
        # Pencereyi her zaman önde tut
        self.attributes("-topmost", True)
        
        # Mevcut ayarları yükle
        self.config = ConfigHandler.load_config()
        
        # Aktif sayfayı takip etmek için değişken
        self.current_page = None
        
        # --- Arayüz Düzeni ---
        self.setup_sidebar_ui()
        
        # İlk açılışta Görünüm sayfasını yükle
        self.show_page("appearance")

    def setup_sidebar_ui(self):
        # 1. SOL YAN MENÜ (SIDEBAR)
        self.sidebar_frame = ctk.CTkFrame(self, width=180, corner_radius=0, fg_color="#0d1421", border_width=1, border_color="#1c2533")
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False) # Genişliğin sabit kalması için
        
        # Menü Başlığı
        self.menu_title = ctk.CTkLabel(self.sidebar_frame, text="⚙️ KONTROL", font=("Arial", 14, "bold"), text_color="#74c0fc")
        self.menu_title.pack(pady=(20, 30))
        
        # Menü Butonları
        self.btn_view = ctk.CTkButton(self.sidebar_frame, text="🎨 Görünüm", anchor="w", fg_color="transparent", text_color="#e0e0e0", hover_color="#1c2533", command=lambda: self.show_page("appearance"))
        self.btn_view.pack(fill="x", padx=10, pady=5)
        
        self.btn_sec = ctk.CTkButton(self.sidebar_frame, text="🛡️ Güvenlik Motoru", anchor="w", fg_color="transparent", text_color="#e0e0e0", hover_color="#1c2533", command=lambda: self.show_page("security"))
        self.btn_sec.pack(fill="x", padx=10, pady=5)
        
        self.btn_hist = ctk.CTkButton(self.sidebar_frame, text="📜 Güncelleme Geçmişi", anchor="w", fg_color="transparent", text_color="#e0e0e0", hover_color="#1c2533", command=lambda: self.show_page("history"))
        self.btn_hist.pack(fill="x", padx=10, pady=5)
        
        self.btn_info = ctk.CTkButton(self.sidebar_frame, text="ℹ️ Hakkında", anchor="w", fg_color="transparent", text_color="#e0e0e0", hover_color="#1c2533", command=lambda: self.show_page("about"))
        self.btn_info.pack(fill="x", padx=10, pady=5)

        # 2. SAĞ İÇERİK PANELİ (CONTENT AREA)
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # 3. EN ALT BUTON PANELİ (KAYDET / İPTAL)
        # Sağ panelin içine en alta yapışacak şekilde konumlandıracağız
        self.action_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.action_frame.pack(side="bottom", fill="x", pady=(10, 0))
        
        self.btn_save = ctk.CTkButton(self.action_frame, text="Değişiklikleri Kaydet", fg_color="#2ecc71", hover_color="#27ae60", text_color="#000", font=("Arial", 12, "bold"), command=self.save_and_close)
        self.btn_save.pack(side="right", padx=5)
        
        self.btn_cancel = ctk.CTkButton(self.action_frame, text="İptal", fg_color="#e74c3c", hover_color="#c0392b", font=("Arial", 12), command=self.destroy)
        self.btn_cancel.pack(side="right", padx=5)

    def clear_content_frame(self):
        """Sağ taraftaki paneli temizler (Butonlar hariç)."""
        for widget in self.content_frame.winfo_children():
            if widget != self.action_frame:
                widget.destroy()

    def update_sidebar_buttons(self, active_page):
        """Hangi sayfadaysak o butonu parlak yapar, diğerlerini söndürür."""
        # Renkleri sıfırla
        self.btn_view.configure(fg_color="transparent", text_color="#e0e0e0")
        self.btn_sec.configure(fg_color="transparent", text_color="#e0e0e0")
        self.btn_hist.configure(fg_color="transparent", text_color="#e0e0e0")
        self.btn_info.configure(fg_color="transparent", text_color="#e0e0e0")
        
        # Aktif olanı renklendir
        if active_page == "appearance":
            self.btn_view.configure(fg_color="#1c2533", text_color="#74c0fc")
        elif active_page == "security":
            self.btn_sec.configure(fg_color="#1c2533", text_color="#74c0fc")
        elif active_page == "history":
            self.btn_hist.configure(fg_color="#1c2533", text_color="#74c0fc")
        elif active_page == "about":
            self.btn_info.configure(fg_color="#1c2533", text_color="#74c0fc")

    def show_page(self, page_name):
        """Tıklanan sekmeye göre sağ paneli dinamik olarak doldurur."""
        if self.current_page == page_name:
            return
        
        self.current_page = page_name
        self.clear_content_frame()
        self.update_sidebar_buttons(page_name)
        
        # Sayfa içeriklerini oluşturacak container frame
        page_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        page_frame.pack(side="top", fill="both", expand=True)
        
        # --- SAYFA İÇERİKLERİ ---
        if page_name == "appearance":
            ctk.CTkLabel(page_frame, text="🎨 Görünüm Ayarları", font=("Arial", 16, "bold"), text_color="#f8fafc").pack(anchor="w", pady=(0, 20))
            
            ctk.CTkLabel(page_frame, text="Uygulama Teması:", font=("Arial", 13, "bold")).pack(anchor="w", pady=5)
            self.theme_combo = ctk.CTkComboBox(page_frame, values=["Dark", "Light", "System"], command=self.change_theme_instant)
            self.theme_combo.pack(anchor="w", pady=(0, 20))
            self.theme_combo.set(self.config["appearance_mode"])
            
            self.notify_check = ctk.CTkCheckBox(page_frame, text="Kritik risklerde masaüstü bildirimi gönder")
            self.notify_check.pack(anchor="w", pady=10)
            if self.config["notifications"]: self.notify_check.select()
            
        elif page_name == "security":
            ctk.CTkLabel(page_frame, text="🛡️ Güvenlik Motoru Yapılandırması", font=("Arial", 16, "bold"), text_color="#f8fafc").pack(anchor="w", pady=(0, 15))
            
            ctk.CTkLabel(page_frame, text="AI Analiz Hassasiyeti:", font=("Arial", 13, "bold")).pack(anchor="w", pady=5)
            self.sensitivity_combo = ctk.CTkComboBox(page_frame, values=["Paranoyak", "Dengeli", "Esnek"])
            self.sensitivity_combo.pack(anchor="w", pady=(0, 15))
            self.sensitivity_combo.set(self.config["ai_sensitivity"])
            
            ctk.CTkLabel(page_frame, text="Yoksayılacak Paketler (Her satıra bir paket):", font=("Arial", 13, "bold")).pack(anchor="w", pady=5)
            self.ignore_text = ctk.CTkTextbox(page_frame, width=440, height=160, fg_color="#05080f", border_width=1, border_color="#1c2533")
            self.ignore_text.pack(fill="both", expand=True, pady=5)
            
            ignore_packages = "\n".join(self.config["ignore_list"])
            self.ignore_text.insert("1.0", ignore_packages)
            
        elif page_name == "history":
            ctk.CTkLabel(page_frame, text="📜 Güncelleme Geçmişi & Audit Log", font=("Arial", 16, "bold"), text_color="#f8fafc").pack(anchor="w", pady=(0, 15))
            
            # Gerçek APT loglarını parse etme aşaması için şık bir simüle edilmiş log ekranı
            log_view = ctk.CTkTextbox(page_frame, width=440, height=240, font=("Consolas", 11), fg_color="#05080f", border_width=1, border_color="#1c2533", text_color="#a5b4fc")
            log_view.pack(fill="both", expand=True)
            
            # Örnek geçmiş verisi (Kullanıcı diğer uygulamadan yapsa bile APT veritabanından yakalayacağımız kısım)
            log_view.insert("0.0", f">>> [AUDIT] Son sistem taraması: {config.get('last_scan', 'Bugün')}\n"
                                   ">>> [INFO] /var/log/apt/history.log analiz ediliyor...\n"
                                   ">>> [OK] Son harici güncelleme: 3 gün önce (Pardus Updater tarafından)\n"
                                   ">>> [AI ANALİZ] Güncellenen paket: linux-image-amd64 -> Risk Durumu: Kararlı\n"
                                   ">>> [AI ANALİZ] Güncellenen paket: firefox-esr -> Risk Durumu: Güvenli\n")
            log_view.configure(state="disabled") # Kullanıcı değiştiremesin
            
        elif page_name == "about":
            ctk.CTkLabel(page_frame, text="UpdateGuard AI Projesi", font=("Arial", 20, "bold"), text_color="#74c0fc").pack(pady=(20, 10))
            ctk.CTkLabel(page_frame, text="Versiyon: 1.2.0-Stable\nLisans: GNU GPLv3 (Özgür Yazılım)", font=("Arial", 13), justify="center").pack(pady=5)
            ctk.CTkLabel(page_frame, text="Pardus Ekosistemi için Akıllı Karar Destek Sistemi", font=("Arial", 12, "italic"), text_color="#94a3b8").pack(pady=10)
            
            self.github_label = ctk.CTkLabel(page_frame, text="🌐 Proje GitHub Sayfası", font=("Arial", 13, "underline"), text_color="#3498db", cursor="hand2")
            self.github_label.pack(pady=20)
            self.github_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/UpdateGuard-Project"))

    def change_theme_instant(self, choice):
        """Temayı tıklandığı an canlı değiştirir."""
        ctk.set_appearance_mode(choice)

    def save_and_close(self):
        """Aktif sayfadaki ve bellekteki verileri toplar, JSON'a kaydeder."""
        # Eğer güvenlik sekmesi açıksa textbox verilerini çek, kapalıysa eski veriyi koru
        if hasattr(self, "ignore_text") and self.ignore_text.winfo_exists():
            raw_text = self.ignore_text.get("1.0", "end-1c").strip()
            ignore_list = [pkg.strip() for pkg in raw_text.split("\n") if pkg.strip()]
        else:
            ignore_list = self.config["ignore_list"]
            
        # UI elementleri mevcutsa değerlerini al, yoksa eski config değerini koru
        theme_val = self.theme_combo.get() if hasattr(self, "theme_combo") and self.theme_combo.winfo_exists() else self.config["appearance_mode"]
        sens_val = self.sensitivity_combo.get() if hasattr(self, "sensitivity_combo") and self.sensitivity_combo.winfo_exists() else self.config["ai_sensitivity"]
        notify_val = bool(self.notify_check.get()) if hasattr(self, "notify_check") and self.notify_check.winfo_exists() else self.config["notifications"]
        
        updated_settings = {
            "appearance_mode": theme_val,
            "ai_sensitivity": sens_val,
            "ignore_list": ignore_list,
            "notifications": notify_val
        }
        
        ConfigHandler.save_config(updated_settings)
        ctk.set_appearance_mode(updated_settings["appearance_mode"])
        self.destroy()