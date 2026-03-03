MouseRecorder + Typing

Genel Bakış:
--------------
MouseRecorder, masaüstünde mouse tıklama koordinatlarını gerçek zamanlı kaydetmenizi, tablo üzerinde düzenlemenizi, yazı (typing) aksiyonları eklemenizi, dışa/içe aktarmanızı ve otomatik olarak oynatmanızı sağlayan gelişmiş bir Python uygulamasıdır.

Artık sadece tıklama değil, klavye yazma aksiyonlarıyla birlikte tam otomasyon senaryoları oluşturabilirsiniz.

Program Görseli:
----------------------------------
![Uygulama Ekran Görüntüsü](ebs.png)

Kimler İçin:
--------------
Bu araç özellikle:
- Tekrarlayan mouse + klavye işlemleri yapan kullanıcılar
- Test otomasyonu yapan yazılımcılar
- Veri girişini otomatikleştirmek isteyenler
- Sunum / eğitim için aksiyon kaydı almak isteyenler
- Bot / makro mantığında basit otomasyon kurmak isteyen herkes

Özellikler:
-------------
Mouse Kayıt:
- Mouse tıklamalarını gerçek zamanlı kaydetme
- Sol / Sağ / Orta tuş desteği
- Tek tıklama & çift tıklama ayrımı
- Otomatik click türü algılama

Typing (Yazı Yazdırma):
- Tabloya manuel yazı satırı ekleme
- Oynatma sırasında otomatik yazdırma
- Click + Type kombinasyonu ile senaryo oluşturma

Tablo Yönetimi:
- Koordinatları sıralı şekilde listeleme
- Action türünü değiştirebilme (Click / Type)
- Detayları ComboBox ile düzenleme
- Seçili satırları silme
- Otomatik sıra güncelleme

Veri İşlemleri:
- .txt olarak dışa aktarma
- .txt dosyasından içeri aktarma (Import)
- Eski kayıtlarla uyumluluk
- Clipboard’a tek tıkla kopyalama

Oynatma (Playback):
- Mouse hareket + tıklama otomasyonu
- Çift tıklama desteği
- Yazı yazdırma desteği
- Aksiyonlar arası gecikme

Arayüz:
- Dark (koyu) tema
- Modern buton tasarımı
- Kullanıcı dostu tablo yapısı

Neden Kullanmalı:
------------------
Bu araç, manuel olarak yaptığınız tekrar eden işlemleri otomatik hale getirir.

Örnek kullanım senaryoları:
- Form doldurma otomasyonu
- Web sitesi testleri
- Oyun içi makrolar
- Veri giriş hızlandırma
- Eğitim/demo kayıtları

Kurulum:
---------
1. Repo klonlanır:
git clone https://github.com/ebubekirbastama/ebs-MouseRecorder.git
cd ebs-MouseRecorder

2. Gerekli kütüphaneler yüklenir:
pip install -r requirements.txt

3. Uygulama çalıştırılır:
python ebubekirbastama_mouse_recorder.py

Kullanım:
---------
1. Başlat butonuna basın
2. Mouse ile tıklamalar yapın → tabloya eklenecek
3. İstersen "Yazı Satırı Ekle" ile metin ekleyin
4. Action türünü değiştirebilirsiniz
5. Gereksiz satırları silin
6. Dışa aktar (.txt) veya Clipboard’a kopyala
7. Koordinatları Oynat ile otomasyonu başlatın

Önemli Notlar:
--------------
- Oynatma sırasında mouse kontrolü programa geçer
- Yanlış koordinatlar farklı yerlere tıklayabilir
- Kritik işlemler sırasında dikkatli kullanın

Dosya Yapısı:
--------------
MouseRecorder<br>
├── ebubekirbastama_mouse_recorder.py   # Ana uygulama<br>
├── requirements.txt                    # Gerekli kütüphaneler<br>
├── README.txt                           # Proje açıklaması<br>
└── ebs.png                             # Program görseli<br>

Gelecek Özellikler (Planlanan):
--------------
- Aksiyonlar arası manuel delay ayarlama
- Döngü (loop) çalıştırma
- JSON format desteği
- Koordinat yerine element bazlı tıklama (ileri seviye)
- Makro kaydet / profil sistemi

Lisans:
--------
MIT License © 2026 ebubekirbastama
