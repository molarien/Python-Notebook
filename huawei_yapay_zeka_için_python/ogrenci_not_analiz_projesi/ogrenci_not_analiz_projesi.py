import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

class OgrenciNotAnalizSistemi:
    """
    Öğrenci not verilerini okuyan, analiz eden,
    filtreleyen ve gösrelleştiren bir sınıf
    """

    def __init__(self, dosya_yolu):
        self.dosya_yolu = dosya_yolu
        self.df = None

    def veriyi_oku(self):
        """
        csv dosyasını okur ve df içerisine yükler
        """    
        try:
            self.df = pd.read_csv(self.dosya_yolu)

            if self.df.empty:
                raise ValueError("csv dosyası boş")

            gerekli_sütunlar = {"isim", "yaş", "bolum", "not"}

            if not gerekli_sütunlar.issubset(self.df.columns):
                raise ValueError(
                    f"csv dosyasında gerekli sütunlar eksik"
                    f"Gerekli sütunlar: {gerekli_sütunlar}"
                )

            self.df["not"] = pd.to_numeric(self.df["not"], errors = "raise")

            print("Veri başarıyla okundu")
            print(self.df)

        except FileNotFoundError:
            print(f"Hata: {self.dosya_yolu} bulunamadı")
        except pd.errors.EmptyDataError:
            print("csv dosyası boş")
        except ValueError as error:
            print(f"Hata: {error}")
        except Exception as e:
            print(f"Beklenmeyen hata: {e}")        


    def numpy_ile_hesaplama(self):
        """
        hesaplanan değerler: ortalama, en düşük not, en yüksek not ve std
        """

        try:

            if self.df is None:
                raise ValueError("Önce veri yüklenmeli")

            # not sütununu numpy dizisine çevir
            notlar = self.df["not"].to_numpy()

            print(f"Ortalama: {np.mean(notlar)}")
            print(f"En yüksek not: {np.max(notlar)}")
            print(f"En düşük not: {np.min(notlar)}")
            print(f"Standart Sapma: {np.std(notlar)}")

        except ValueError as hata:
            print(f"Hata: {hata}")
        except Exception as e:
            print(f"Beklenmeyen bir hata oluştu: {e}")


    def pandas_ile_filtreleme(self):

        try:
            if self.df is None:
                raise ValueError("Önce veri okunmalıdır")

            print("Pandas ile filtreleme sonuçları")

            # notu 80 den büyük olan öğrenciler
            yuksek_notlular = self.df[self.df["not"] > 80]
            print(f"Notu 80'den büyük olan öğrenciler: {yuksek_notlular}")

            # bölümü yapay zeka olanlar
            yapay_zeka_ogrencileri = self.df[self.df["bolum"] == "Yapay Zeka"]
            print(f"Bölümü yapay zeka olanlar: {yapay_zeka_ogrencileri}")

            # 22 yaşından büyük olanlar
            yasi_buyuk_olanlar = self.df[self.df["yas"] > 22]
            print(f"Yaşı 22'den büyük olanla: {yasi_buyuk_olanlar}")

        except ValueError as hata:
            print(f"Hata: {hata}")
        except Exception as e:
            print(f"Beklenmeyen bir hata oluştu: {e}")


    def grafik_ciz(self):

        try:
            if self.df is None:
                raise ValueError("Önce veri okunmalı")

            # grafik boyutu ayarlama
            plt.figure(figsize=(10,5))

            plt.bar(self.df["isim"], self.df["not"])
            plt.title("Öğrenci Not Grafiği")
            plt.xlabel("Öğrenci İsimleri")
            plt.ylabel("Notlar")

            plt.tight_layout() # grafiği daha güzel gösterir

            plt.show()

        except Exception as e:
            print(f"Hata: {e}")    


    def tum_analizi_calistir(self):

        self.veriyi_oku()

        if self.df is None:
            print("Analiz durduruldu")
            return

        self.numpy_ile_hesaplama()

        self.pandas_ile_filtreleme()

        self.grafik_ciz()


if __name__ == "__main__":
   mevcut_dizin = Path(__file__).parent
   dosya_yolu = mevcut_dizin / "ogrenci_notlari.csv"
   
   sistem = OgrenciNotAnalizSistemi(dosya_yolu)

   sistem.tum_analizi_calistir() 