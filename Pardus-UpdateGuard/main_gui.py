import customtkinter as ctk
import subprocess
import os

# Görünüm ayarları
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class UpdateGuardGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pardus UpdateGuard v1.0")
        self.geometry("700x500")

        # Başlık
        self.label = ctk.CTkLabel(self, text="🛡️ Pardus UpdateGuard", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        # Butonlar İçin Frame
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10, padx=20, fill="x")

        self.scan_button = ctk.CTkButton(self.button_frame, text="Sistemi Tara", command=self.run_scanner)
        self.scan_button.pack(side="left", padx=20, pady=10, expand=True)

        self.ai_button = ctk.CTkButton(self.button_frame, text="Yapay Zeka Analizi", command=self.run_ai, fg_color="green", hover_color="darkgreen")
        self.ai_button.pack(side="left", padx=20, pady=10, expand=True)

        # Rapor Ekranı
        self.result_text = ctk.CTkTextbox(self, width=600, height=300)
        self.result_text.pack(pady=20, padx=20)
        self.result_text.insert("0.0", "Hoş geldiniz! Analiz yapmak için yukarıdaki butonları kullanın.\n")

    def run_scanner(self):
        self.result_text.insert("end", "\n[1/2] Sistem taranıyor...\n")
        
        # Bu dosyanın (main_gui.py) bulunduğu klasörü tam yol olarak al
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Dosyalar aynı klasörde olduğu için direkt yan yana olduklarını belirtiyoruz
        scanner_path = os.path.join(current_dir, "scanner.py")
        
        # subprocess çalıştırırken 'cwd' (current working directory) parametresini ekliyoruz
        # Böylece scanner.py çalışırken updates.json'ı doğru yere yazar
        subprocess.run(["python", scanner_path], cwd=current_dir)
        
        self.result_text.insert("end", "✅ Tarama tamamlandı.\n")

    def run_ai(self):
        self.result_text.insert("end", "[2/2] Yapay Zeka analiz ediyor...\n")
        self.update_idletasks()
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ai_path = os.path.join(current_dir, "ai_engine.py")
        
        # Yine 'cwd' ekleyerek ai_engine.py'nin kendi klasöründe işlem yapmasını sağlıyoruz
        subprocess.run(["python", ai_path], cwd=current_dir)
        
        report_path = os.path.join(current_dir, "ai_report.txt")
        if os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                report = f.read()
                self.result_text.delete("1.0", "end") # Eski yazıları sil
                self.result_text.insert("0.0", f"--- AI ANALİZ RAPORU ---\n\n{report}")
        else:
            self.result_text.insert("end", "❌ Hata: Rapor dosyası bulunamadı!")

if __name__ == "__main__":
    app = UpdateGuardGUI()
    app.mainloop()