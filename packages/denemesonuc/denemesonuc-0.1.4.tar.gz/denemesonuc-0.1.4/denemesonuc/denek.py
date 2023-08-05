from selenium.webdriver.remote.webdriver import WebDriver

import denemesonuc.fetch_new
import denemesonuc.fetch_old
import denemesonuc.models


class Denek:
    """# denemeye giren kişi. denek.

    `fetchDeneme`: verilen denemenin sonuçlarını çeker
    `getDeneme`: çekilen deneme sonucunu döndürür"""

    def __init__(
        self,
        driver: WebDriver,
        ad: str,
        no: int,
        sinif_duzeyi: int,
        sehir: str,
        ilce: str,
        kurum: str,
    ) -> None:
        """### denek bilgileri

        `ad`: ad
        `no`: numara
        `sinif_duzeyi`: sınıf düzeyi
        `sehir`: şehir, tamamı büyük harf olmalı
        `kurum`: okulun adı"""
        self.__driver = driver
        self.ad = ad
        self.no = no
        self.sinif_duzeyi = sinif_duzeyi
        self.sehir = (
            sehir.replace("ı", "I").replace("i", "İ").upper()
        )  # pythonın localeler ile sorunu var
        self.ilce = ilce.replace("ı", "I").replace("i", "İ").upper()
        self.kurum = kurum
        self.__deneme: dict[str, denemesonuc.models.DenemeResult] = {}

    def __repr__(self) -> str:
        """can sıkıntısı. denekleri stringe çevirmek için. abracadabra"""
        return f"Denek: {self.no} ({self.ad})"

    def fetchDeneme(self, deneme: denemesonuc.models.DenemeLogin) -> int:
        """### denek ve deneme bilgileriyle deneme sonuçlarını çeker

        `deneme`: istenen deneme

        return:
        - 0: çekme başarılı
        - 1:
        - 2: denek denemeye girmemiş"""
        try:
            if deneme.deneme_type == "old":
                self.__deneme[deneme.deneme_adi] = denemesonuc.fetch_old.fetch(
                    self.__driver,
                    self.ad,
                    self.no,
                    self.sinif_duzeyi,
                    self.sehir,
                    self.kurum,
                    deneme,
                )
            else:
                self.__deneme[deneme.deneme_adi] = denemesonuc.fetch_new.fetch(
                    self.__driver,
                    self.ad,
                    self.no,
                    self.sinif_duzeyi,
                    self.sehir,
                    self.ilce,
                    self.kurum,
                    deneme,
                )
        except denemesonuc.models.DenekNotFound:
            return 2
        return 0

    def getDenemeList(self) -> list[str]:
        """### girilen denemelerin adlarının listesini döndürür"""
        return list(self.__deneme.keys())

    def getDeneme(
        self, deneme: denemesonuc.models.DenemeLogin, deneme_adi: str = ""
    ) -> denemesonuc.models.DenemeResult:
        """### çekilmiş deneme sonucunu döndürür

        `deneme`: istenen deneme
        `deneme_adi`: deneme adı, yalnızca `deneme` parametresi boşsa kullanılabilir"""
        if deneme_adi and deneme is None:
            return self.__deneme[deneme_adi]
        return self.__deneme[deneme.deneme_adi]
