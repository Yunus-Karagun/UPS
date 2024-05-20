import os
import win32com.client
import datetime
import pytz

# Outlook'u başlat
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

# KASA klasörünü seç
root_folder = outlook.GetDefaultFolder(6)
kasa_folder = None
for folder in root_folder.Folders:
    if folder.Name == "UPS":
        kasa_folder = folder
        break

if not kasa_folder:
    print("UPS klasörü bulunamadı.")
    exit()

# E-postaları oku
messages = kasa_folder.Items

# Belirli bir tarih
kriter_tarih = datetime.datetime(2024, 1, 17)

# Zaman damgasına göre e-postaları sırala
messages.Sort("[ReceivedTime]", True)

# Excel dosyalarını kaydetmek için hedef klasör
hedef_klasor = "D:\\UPS"

# E-postalardaki Excel dosyalarını belirli bir tarihten sonraki indir
for message in messages:
    received_time = message.ReceivedTime.replace(tzinfo=None)
    
    if received_time >= kriter_tarih:
        attachments = message.Attachments
        for attachment in attachments:
            if attachment.FileName.endswith(('.xls', '.xlsx')):
                # E-posta konusunu al
                konu = message.Subject
                # İlk kelimeyi al
                ilk_kelime = konu.split()[0]
                
                # Excel dosyasının adını oluştur
                dosya_adi = f"{ilk_kelime}_{attachment.FileName}"
                
                hedef_yol = os.path.join(hedef_klasor, dosya_adi)
                attachment.SaveAsFile(hedef_yol)
                print(f"{attachment.FileName} dosyası başarıyla indirildi. Yeni adı: {dosya_adi}")
