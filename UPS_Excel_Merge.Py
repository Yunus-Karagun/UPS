import os
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# Birleştirmek istediğiniz Excel dosyalarının bulunduğu klasörü belirtin
klasor_yolu = "D:\\UPS"

# Klasördeki tüm Excel dosyalarını alın
dosya_listesi = [dosya for dosya in os.listdir(klasor_yolu) if dosya.endswith('.xls')]

# Birleştirilmiş veriyi tutacak boş bir DataFrame oluşturun
birlesik_veri = pd.DataFrame()

# Her bir Excel dosyasını okuyarak birleştirilmiş veriye ekleyin
for dosya in dosya_listesi:
    dosya_yolu = os.path.join(klasor_yolu, dosya)
    df = pd.read_excel(dosya_yolu)
    
    # Her satıra dosya adını içeren bir sütun ekleyin
    df['DosyaAdi'] = dosya
    
    # DataFrame'leri birleştirirken `concat` fonksiyonunu kullanın
    birlesik_veri = pd.concat([birlesik_veri, df], ignore_index=True)

# 'FaturaNo' sütununu oluşturun
birlesik_veri["FaturaNo"] = birlesik_veri['DosyaAdi'].str.split(pat="_", expand=True)[0]
fatura_column = birlesik_veri.pop('FaturaNo')
birlesik_veri.insert(0, 'FaturaNo', fatura_column)

# Birleştirilmiş veriyi yeni bir Excel dosyasına kaydedin
birlesik_veri.to_excel('D:\\UPS\\UPS\\UPS_All.xlsx', index=False)

print("Veriler birleştirildi ve 'D:\\UPS\\UPS\\UPS_All.xlsx' dosyasına kaydedildi.")