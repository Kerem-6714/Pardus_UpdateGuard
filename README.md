# Pardus UpdateGuard (v1.2)

Pardus UpdateGuard; Linux tabanlı yerli işletim sistemimiz **Pardus** (ve tüm Debian türevleri) için özel olarak geliştirilmiş, siber güvenlik odaklı ve **Yapay Zeka Destekli Sezgisel Analiz Motoruna (Heuristic Inference Engine)** sahip bir paket tarama, risk analiz ve güvenli güncelleme otomasyon yazılımıdır.

Geleneksel paket yöneticileri (`apt`, Synaptic vb.) sistemdeki güncellemeleri sadece düz bir metin listesi olarak sunarken; UpdateGuard arka planda çalışan hibrit tehdit modelleme altyapısı sayesinde her bir paketin sisteme getirebileceği siber risk oranını matematiksel olarak hesaplar ve sistem yöneticisine dinamik, anlaşılır bir güvenlik raporu sunar.

---

## Öne Çıkan Özellikler

* **Evrensel Masaüstü & Sürüm Uyumluluğu:** Pardus'un tüm sürümleriyle (Pardus 21, 23, 26 vb.) ve tüm masaüstü ortamlarıyla (XFCE, GNOME) %100 uyumludur.
* **Modern Siber Arayüz:** `CustomTkinter` kütüphanesi kullanılarak Pardus 26 arayüz standartlarına (1020x740) uygun, donanım hızlandırmalı modern ve göz yormayan Koyu Siber Tema tasarımı.
* **Asenkron Çalışma Mimarisi (Multi-Threading):** Tarama, indirme ve kurulum işlemleri arka planda farklı iş parçacıklarında (thread) yürütülür; böylece arayüz hiçbir zaman "Yanıt Vermiyor" konumuna düşmez, donmaz.
* **Çevre ve Donanım Farkındalığı:** Linux terminal hatlarını kullanarak bilgisayardaki ekran kartını (NVIDIA, AMD, Intel) otomatik tespit eder ve AI raporlarını bu donanım mimarisine göre optimize eder.
* **Gelişmiş Ayarlar & Kalıcı Bellek:** Tema seçimi, AI hassasiyet seviyesi, sistem bildirimleri ve tarama dışı bırakılacak paketlerin (`ignore_list`) yönetimi. Ayarlar program kapatılsa dahi JSON tabanlı kalıcı bellekte saklanır.

---

## Siber Güvenlik Altyapısı ve Risk Algoritması

UpdateGuard, statik imza kontrolü ile dinamik sezgisel analizi birleştiren **Hibrit Siber Tehdit Analiz Altyapısı** üzerine kurulmuştur. Yazılım, risk analizi için **Ağırlıklı Sezgisel Çıkarım Algoritması (Weighted Heuristic Inference Algorithm)** kullanır.

### Matematiksel Risk Skorlama Modeli
Bir paketin nihai risk skoru ($RS$), sisteme etki edebilecek 3 farklı siber ağırlık faktörünün toplamıyla hesaplanır:

$$RS = \min(W_{core} + W_{version} + W_{size}, 100)$$

1.  **Sistem Kök ve Çekirdek Ağırlığı ($W_{core}$):** Saldırganların en çok hedef aldığı `kernel`, `linux-image`, `systemd` veya `udev` gibi bileşenlerin tespiti durumunda Yetki Yükseltme (Privilege Escalation) risklerine karşı sisteme direkt **+60 Puan** eklenir. Paylaşımlı kütüphanelerde (`lib` ile başlayanlar) Tedarik Zinciri Saldırıları (Supply Chain Attack) riskine karşı **+25 Puan** eklenir.
2.  **Sürüm Sıçraması Ağırlığı ($W_{version}$):** Güncellenecek pakette majör bir sürüm değişikliği (Örn: v1.0 -> v2.0) algılanırsa, Sıfırıncı Gün Açıkları (Zero-Day Vulnerability) barındırma ihtimaline karşı **+30 Puan** eklenir.
3.  **Paket Boyutu Değişim Ağırlığı ($W_{size}$):** Güncellenecek veri bloğu 500 MB üzerindeyse, araya zararlı yazılım (Trojan/Backdoor) sızdırılma riskini minimize etmek adına **+10 Puan** eklenir.

### Tehdit Seviyeleri
* 🔴 **$RS \ge 80$ (Kritik):** Çekirdek veya sürücü seviyesinde majör değişim. Kesinlikle admin onayı gerektirir.
* 🟡 **$40 \le RS < 80$ (Yüksek/Orta):** Sistem kütüphanelerinde veya geniş çaplı bağımlılık zincirlerinde değişiklik.
* 🔵🟢 **$RS < 40$ (Düşük / Kararlı):** Standart kullanıcı uygulamaları ve güvenli yamalar.

---

## Güvenlik ve Hata Toleransı (Fault Tolerance)

* **Veritabanı Koruma Çemberi:** `risks.json` veya `config.json` dosyaları silinirse kod çökmez; çalışma zamanında (Runtime) hafızada sanal bir bellek oluşturarak kesintisiz çalışmaya devam eder.
* **Grafiksel Yetki İstemi (`pkexec`):** Sistem güncellenirken terminal tabanlı güvensiz `sudo` yerine, Linux standartlarında grafiksel şifre sorma mimarisi (`policykit`) tetiklenir.
* **Önbellek Kilit Koruması:** Tarama ve kurulum esnasında kritik butonlar geçici olarak dondurularak kullanıcının APT önbelleğini (`/var/lib/dpkg/lock`) kilitlemesi engellenir.
* **Akıllı Kurulum Kontrolü:** Sistemde güncellenecek paket yoksa veya tarama yapılmadıysa, "SİSTEMİ GÜNCELLE" butonu terminal komut hatlarına inmeyerek işlemi güvenli bir uyarıyla sonlandırır.

---

## Kurulum ve Çalıştırma

### Gereksinimler
Sistemin çalışabilmesi için Pardus/Linux ortamında Python3 ve gerekli kütüphanelerin yüklü olması gerekir:

```bash
sudo apt update
sudo apt install python3-pip python3-pil python3-pil.imagetk -y
pip3 install customtkinter
```
---

## Çalıştırma

Proje klasörüne gidin ve ana arayüz dosyasını tetikleyin:

```bash
python3 main_gui.py
```
---

## Lisans

Bu proje **GNU GPLv3** lisansı altında korunmaktadır. Kaynak kodları açık olup, geliştirilmeye ve yerli işletim sistemi ekosistemine katkı sunmaya tamamen müsaittir.