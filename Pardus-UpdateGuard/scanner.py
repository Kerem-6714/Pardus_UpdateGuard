import subprocess
import time
import threading

class UpdateScanner:
    def __init__(self, gui_instance):
        """
        gui_instance: main_gui.py içindeki ana sınıfın (self) referansı.
        Bu sayede buradaki verileri ekrandaki konsola ve ilerleme çubuğuna gönderebiliriz.
        """
        self.gui = gui_instance

    def start_scan_thread(self):
        """Tarama işlemini arayüzü dondurmamak için ayrı bir kanalda (thread) başlatır."""
        scan_thread = threading.Thread(target=self.scan_process)
        scan_thread.daemon = True
        scan_thread.start()

    def scan_process(self):
        """Ana tarama ve analiz süreci."""
        # Arayüz Hazırlığı
        self.gui.scan_button.configure(state="disabled", text="SİSTEME BAĞLANILIYOR...")
        self.gui.status_indicator.configure(text="CANLI VERİ ÇEKİLİYOR...", text_color="#f1c40f")
        self.gui.console.delete("1.0", "end")
        self.gui.progress_bar.set(0)

        try:
            # 1. ADIM: Pardus Terminaline Bağlanma (Subprocess)
            # 'apt list --upgradable' komutu sistemdeki güncellemeleri getirir.
            self.gui.console.insert("end", ">>> [SİSTEM] APT Paket Yöneticisi sorgulanıyor...\n")
            
            raw_output = subprocess.check_output(
                ["apt", "list", "--upgradable"], 
                stderr=subprocess.STDOUT
            ).decode("utf-8")

            # Metni satırlara böl ve başlık kısmını atla
            all_lines = raw_output.splitlines()
            real_updates = [line for line in all_lines if "/" in line]

            if not real_updates:
                self.gui.console.insert("end", ">>> [BİLGİ] Sisteminiz tamamen güncel.\n>>> Analiz edilecek riskli paket bulunamadı.")
                self.gui.progress_bar.set(1.0)
                self.finalize_scan([])
                return

            # 2. ADIM: Paket Analiz Döngüsü (Gerçek Zamanlı)
            total_count = len(real_updates)
            self.gui.console.insert("end", f">>> [BİLGİ] {total_count} adet güncelleme paketi bulundu. Analiz başlıyor...\n")

            for i, line in enumerate(real_updates):
                # Paket ismini ayıkla (Örn: linux-image-amd64)
                pkg_name = line.split("/")[0]
                
                # --- Geliştirme Kategorisi: Kural Tabanlı AI Mantığı ---
                risk_level = "DÜŞÜK RİSK"
                if any(k in pkg_name.lower() for k in ["linux", "kernel", "ssl", "ssh", "firmware", "nvidia"]):
                    risk_level = "KRİTİK GÜVENLİK"

                # Konsola canlı yazdır
                msg = f">>> [ANALİZ] {pkg_name.ljust(30)} | DURUM: {risk_level}"
                self.gui.console.insert("end", f"\n{msg}")
                self.gui.console.see("end")
                
                # Progress bar güncelleme
                self.gui.progress_bar.set((i + 1) / total_count)
                time.sleep(0.2) # Görsellik için hafif bekleme

            # 3. ADIM: Final Raporu
            self.finalize_scan(real_updates)

        except Exception as e:
            self.gui.console.insert("end", f"\n\n[KRİTİK HATA] Sistem verisi çekilemedi: {e}")
            self.gui.scan_button.configure(state="normal", text="YENİDEN DENE")

    def finalize_scan(self, updates):
        """Tarama bitince AI önerilerini ekrana basar."""
        self.gui.status_indicator.configure(text="ANALİZ TAMAMLANDI", text_color="#2ecc71")
        
        if not updates:
            report = "✨ AI ANALİZİ: Sisteminiz güvenli. Şu an için herhangi bir müdahale gerekmiyor."
        else:
            critical_count = sum(1 for p in updates if any(k in p for k in ["linux", "kernel", "ssl"]))
            
            report = (
                f"📊 ANALİZ ÖZETİ:\n"
                f"İncelenen {len(updates)} paketten {critical_count} tanesi yüksek riskli.\n\n"
                "🛡️ AI TAVSİYESİ:\n"
                "Sistem çekirdeği bileşenleri güncellenecek listesinde. "
                "UpdateGuard, bu güncellemelerin Pardus üzerinde 'Secure Boot' "
                "ve 'Nvidia Driver' uyumunu bozmaması için işlemden sonra "
                "sistemi yeniden başlatmanızı önerir."
            )

        self.gui.ai_suggestion.configure(text=report)
        self.gui.scan_button.configure(state="normal", text="YENİDEN TARA")
        self.gui.smooth_scroll_to_bottom()