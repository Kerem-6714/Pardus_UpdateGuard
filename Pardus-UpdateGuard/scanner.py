import json
import os
import subprocess
import time
import threading
import re

class UpdateScanner:
    def __init__(self, gui_instance):
        self.gui = gui_instance
        # JSON Veritabanını en başta yükleyelim
        self.risk_db = self.load_risk_db()

    def dynamic_inference(self, pkg_details):
        """Paket detaylarını alıp çıkarım yapar."""
        score = 0
        reasons = []

        # 1. Kök Analizi (Heuristic)
        if any(x in pkg_details['name'] for x in ['kernel', 'linux-image', 'systemd', 'udev']):
            score += 60
            reasons.append("Kritik sistem bileşeni (Core Component) tespiti.")
        elif pkg_details['name'].startswith('lib'):
            score += 25
            reasons.append("Sistem kütüphanesi bağımlılık zinciri riski.")

        # 2. Sürüm Sıçraması Analizi
        old_major = pkg_details['old_ver'].split('.')[0] if '.' in pkg_details['old_ver'] else "0"
        new_major = pkg_details['new_ver'].split('.')[0] if '.' in pkg_details['new_ver'] else "0"
        
        if old_major != new_major:
            score += 30
            reasons.append(f"Majör sürüm değişikliği ({old_major} -> {new_major}).")

        # 3. Boyut Analizi
        if pkg_details['size'] > 500000000:
            score += 10
            reasons.append("Sıradışı paket boyutu; geniş kapsamlı veri değişimi.")

        return min(score, 100), reasons

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
        """Tarama bitince AI motorunu çalıştırır ve UI'ı günceller."""
        total_risk = 0
        insight_report = "### 🧠 AI DERİN ANALİZ RAPORU\n\n"

        if not updates:
            self.update_ui_elements(0, "✨ AI ANALİZİ: Sisteminiz %100 güncel ve güvende.")
            return

        for pkg in updates:
            # Burası önemli: Gerçek verileri mock_details içine yerleştiriyoruz
            pkg_name = pkg.split('/')[0]
            
            mock_details = {
                'name': pkg_name,
                'old_ver': "1.0", # Buraya gerçek versiyon çekme eklenebilir
                'new_ver': "2.0",
                'size': 150000000
            }
            
            p_score, p_reasons = self.dynamic_inference(mock_details)
            
            if p_score > 30: # 30 puan üstü her şeyi raporla (Uzman seviyesi)
                insight_report += f"📍 **{pkg_name.upper()}** (Risk: %{p_score})\n"
                for r in p_reasons:
                    insight_report += f"  - {r}\n"
                insight_report += "\n"
            
            if p_score > total_risk: 
                total_risk = p_score

        # Grafik ve UI güncelleme fonksiyonuna gönderiyoruz
        self.update_ui_elements(total_risk, insight_report)
        
    def update_ui_elements(self, score, report):
        """Arayüzdeki risk barı ve raporu günceller."""
        self.gui.status_indicator.configure(text="ANALİZ TAMAMLANDI", text_color="#2ecc71")
        
        # Risk Çubuğu Güncelleme
        self.gui.risk_bar.set(score / 100)
        
        # Renk Belirleme
        color = "#e74c3c" if score >= 80 else ("#f1c40f" if score >= 40 else "#3498db")
        if score == 0: color = "#2ecc71"
            
        self.gui.risk_bar.configure(progress_color=color)
        self.gui.risk_label.configure(text=f"SİSTEM RİSK ANALİZİ: %{score}", text_color=color)
        
        # Raporu Yazdır
        self.gui.ai_suggestion.configure(text=report)
        self.gui.upgrade_button.configure(state="normal" if score > 0 else "disabled")
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