import json
import os
import subprocess
import time
import threading

class UpdateScanner:
    def __init__(self, gui_instance):
        self.gui = gui_instance
        # JSON Veritabanını en başta yükleyelim
        self.risk_db = self.load_risk_db()

    def load_risk_db(self):
        """Dışarıdaki risks.json dosyasını yükler."""
        try:
            with open("risks.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            # Dosya yoksa veya hatalıysa temel bir sözlük döndür
            return {
                "linux-image": {"level": "KRİTİK", "desc": "Çekirdek güncellemesi."},
                "nvidia": {"level": "YÜKSEK", "desc": "Sürücü güncellemesi."}
            }

    def start_scan_thread(self):
        scan_thread = threading.Thread(target=self.scan_process)
        scan_thread.daemon = True
        scan_thread.start()

    def scan_process(self):
        """Ana tarama süreci."""
        # --- ARAYÜZ SIFIRLAMA ---
        self.gui.scan_button.configure(state="disabled", text="ANALİZ YAPILIYOR...")
        self.gui.status_indicator.configure(text="SİSTEM VERİLERİ ANALİZ EDİLİYOR...", text_color="#f1c40f")
        self.gui.console.delete("1.0", "end")
        self.gui.progress_bar.set(0)

        try:
            # --- 1. ADIM: VERİ TOPLAMA ---
            self.gui.console.insert("end", ">>> [SİSTEM] APT terminal bağlantısı kuruluyor...\n")
            
            # Terminal dilini standartlaştırmak için env ekliyoruz (LC_ALL=C)
            env = os.environ.copy()
            env["LC_ALL"] = "C"
            
            raw_output = subprocess.check_output(
                ["apt", "list", "--upgradable"], 
                stderr=subprocess.STDOUT,
                env=env
            ).decode("utf-8")

            all_lines = raw_output.splitlines()
            real_updates = [line for line in all_lines if "/" in line and "[" in line]

            if not real_updates:
                self.handle_no_updates()
                return

            # --- 2. ADIM: ANALİZ DÖNGÜSÜ ---
            total_count = len(real_updates)
            self.gui.console.insert("end", f">>> [BİLGİ] {total_count} adet paket bulundu. Yapay zeka analizi başlıyor...\n")

            for i, line in enumerate(real_updates):
                pkg_name = line.split("/")[0]
                
                # Risk Analizi (JSON'dan veya varsayılan)
                risk_data = self.analyze_risk(pkg_name)
                
                # Konsola yazdırma
                msg = f">>> [ANALİZ] {pkg_name.ljust(35)} | DURUM: {risk_data['level']}"
                self.gui.console.insert("end", f"\n{msg}")
                self.gui.console.see("end")
                
                # İlerleme çubuğunu paket sayısına göre güncelle
                self.gui.progress_bar.set((i + 1) / total_count)
                time.sleep(0.15) # Görsel akıcılık

            # --- 3. ADIM: SONUÇLANDIRMA ---
            self.finalize_scan(real_updates)

        except Exception as e:
            self.gui.console.insert("end", f"\n\n[KRİTİK HATA] İşlem yarıda kesildi: {e}")
            self.gui.scan_button.configure(state="normal", text="YENİDEN DENE")

    def analyze_risk(self, pkg_name):
        """Paket ismine göre veritabanından risk seviyesi döndürür."""
        for key, data in self.risk_db.items():
            if key.lower() in pkg_name.lower():
                return data
        return {"level": "STABİL", "desc": "Standart güncelleme."}

    def handle_no_updates(self):
        """Güncelleme yoksa yapılacak işlemler."""
        self.gui.console.insert("end", ">>> [BİLGİ] Sisteminiz tamamen güncel.\n>>> Herhangi bir risk tespit edilmedi.")
        self.gui.progress_bar.set(1.0)
        self.finalize_scan([])

    def finalize_scan(self, updates):
        """Tarama bitince risk çubuğunu doldurur ve AI raporunu hazırlar."""
        self.gui.status_indicator.configure(text="ANALİZ TAMAMLANDI", text_color="#2ecc71")
        
        # 1. Risk Skorunu Hesapla
        max_score = 0
        if updates:
            for p in updates:
                p_name = p.split("/")[0]
                res = self.analyze_risk(p_name)
                if res["score"] > max_score:
                    max_score = res["score"]
        else:
            max_score = 5 # Güncelleme yoksa risk %5 (Taban değer)

        # 2. Risk Çubuğunu ve Rengini Güncelle
        risk_ratio = max_score / 100
        self.gui.risk_bar.set(risk_ratio)

        if max_score >= 80:
            risk_color = "#e74c3c" # Kırmızı
            risk_status = "KRİTİK"
        elif max_score >= 40:
            risk_color = "#f1c40f" # Sarı
            risk_status = "ORTA RİSK"
        else:
            risk_color = "#2ecc71" # Yeşil
            risk_status = "GÜVENLİ"

        self.gui.risk_bar.configure(progress_color=risk_color)
        self.gui.risk_label.configure(text=f"SİSTEM RİSK ANALİZİ: %{max_score} ({risk_status})", text_color=risk_color)

        # 3. Rapor Metnini Oluştur
        if not updates:
            report = "✨ AI ANALİZİ: Sisteminiz şu an tam koruma altında. Ek bir işleme gerek yok."
            self.gui.upgrade_button.configure(state="disabled") # Güncelleme yoksa buton kapalı kalsın
        else:
            criticals = [u for u in updates if self.analyze_risk(u.split("/")[0])["level"] == "KRİTİK"]
            
            report = f"📊 ANALİZ ÖZETİ:\n"
            report += f"Toplam {len(updates)} paket incelendi. {len(criticals)} adet kritik risk bulundu.\n\n"
            
            if len(criticals) > 0:
                report += "🛡️ KRİTİK UYARI:\nSisteminde çekirdek veya güvenlik seviyesinde değişimler var. "
                report += "UpdateGuard bu güncellemeleri 'Yüksek Öncelikli' olarak işaretledi."
            else:
                report += "✅ GÜVENLİK DURUMU:\nBulunan paketler sistem kararlılığını bozacak düzeyde değil."

            # Güncelleme varsa butonu her durumda aktif et
            self.gui.upgrade_button.configure(state="normal")

        # 4. Arayüzü Güncelle
        self.gui.ai_suggestion.configure(text=report)
        self.gui.scan_button.configure(state="normal", text="YENİDEN TARA")
        self.gui.smooth_scroll_to_bottom()
        
    def start_upgrade_thread(self):
        """Güncelleme işlemini ayrı bir kanalda (thread) başlatır."""
        upgrade_thread = threading.Thread(target=self.upgrade_process)
        upgrade_thread.daemon = True
        upgrade_thread.start()

    def upgrade_process(self):
        """Gerçek Pardus güncelleme komutlarını çalıştırır."""
        # Arayüzü güncelleme moduna al
        self.gui.upgrade_button.configure(state="disabled", text="GÜNCELLENİYOR...")
        self.gui.scan_button.configure(state="disabled")
        
        self.gui.console.insert("end", "\n\n" + "="*50)
        self.gui.console.insert("end", "\n>>> [İŞLEM] Sistem güncelleniyor. Lütfen şifre girin...\n")
        self.gui.console.insert("end", "="*50 + "\n")
        self.gui.console.see("end")

        try:
            # pkexec: Grafik arayüzde yetki (şifre) istemek için
            # apt-get dist-upgrade: Tüm bağımlılıklarla beraber tam güncelleme
            cmd = ["pkexec", "apt-get", "dist-upgrade", "-y"]
            
            # Komut çıktısını canlı olarak konsola yansıtmak için Popen kullanıyoruz
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            for line in process.stdout:
               self.gui.console.insert("end", f"> {line}")
               self.gui.console.see("end")

            process.wait()

            if process.returncode == 0:
               self.gui.console.insert("end", "\n>>> [BAŞARILI] Sistem başarıyla güncellendi!\n")
               self.gui.status_indicator.configure(text="SİSTEM GÜNCEL", text_color="#2ecc71")
            else:
               self.gui.console.insert("end", "\n>>> [İPTAL/HATA] Güncelleme işlemi tamamlanamadı.\n")

        except Exception as e:
            self.gui.console.insert("end", f"\n[KRİTİK HATA] {e}\n")
        
        # İşlem bitince butonları eski haline getir
        self.gui.upgrade_button.configure(state="disabled", text="SİSTEM GÜNCEL")
        self.gui.scan_button.configure(state="normal", text="YENİDEN TARA")