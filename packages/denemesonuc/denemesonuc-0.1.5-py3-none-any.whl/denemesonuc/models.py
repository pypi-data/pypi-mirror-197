from dataclasses import dataclass
from typing import Optional
from warnings import warn


@dataclass
class DersSonuc:
    """derslere göre sonuçları saklamak için oluşturulan sınıf"""

    dogru: int = 0
    """doğru soru sayısı"""
    yanlis: int = 0
    """yanlış soru sayısı"""
    bos: int = 0
    """boş soru sayısı"""
    net: float = 0.0
    """net değeri"""
    soru: int = 0
    """soru sayısı"""


@dataclass
class DenemeDerece:
    """dereceleri tutmak için oluşturulan sınıf"""

    sinif: int
    """sınıf içindeki derece"""
    kurum: int
    """kurum içindeki derece"""
    il: int
    """il içindeki derece"""
    genel: int
    """genel içindeki derece"""


@dataclass
class DenemeLogin:
    """deneme giriş bilgilerini tutan sınıf"""

    deneme_adi: str = ""
    deneme_type: str = "new"
    url: str = "https://bes.karnemiz.com/?pg=ogrgiris"
    logout_url: str = ""

    def __post_init__(self):
        if self.deneme_type == "new" and not self.logout_url:
            warn(
                "logout_url is empty with new type option. this may cause selenium.exceptions.NoSuchElementException as not logged out.",
                RuntimeWarning,
            )
        if not self.deneme_type in ("new", "old"):
            raise ValueError("deneme_type must be 'new' or 'old'")
        if not self.url.startswith("https://"):
            raise ValueError("url must start with 'https://'")
        if self.logout_url and not self.logout_url.startswith("https://"):
            raise ValueError("logout_url must start with 'https://'")


@dataclass
class DenemeResult:
    """deneme sonuç bilgilerini tutan sınıf"""

    genel: Optional[DersSonuc] = None
    """genel (bütün dersler) sonucu"""
    edb: Optional[DersSonuc] = None
    """edebiyat sonucu"""
    trh: Optional[DersSonuc] = None
    """tarih sonucu"""
    cog: Optional[DersSonuc] = None
    """coğrafya sonucu"""
    din: Optional[DersSonuc] = None
    """din kültürü ve ahlak bilgisi sonucu"""
    mat: Optional[DersSonuc] = None
    """matematik sonucu"""
    fiz: Optional[DersSonuc] = None
    """fizik sonucu"""
    kim: Optional[DersSonuc] = None
    """kimya sonucu"""
    biy: Optional[DersSonuc] = None
    """biyoloji sonucu"""
    fel: Optional[DersSonuc] = None
    """felsefe sonucu"""
    sfl: Optional[DersSonuc] = None
    """seçmekli felsefe sonucu"""
    drc: Optional[DenemeDerece] = None
    """derece bilgileri"""
    sinif: Optional[str] = None
    """sınıf bilgisi"""
    puan: Optional[float] = None
    """puan değeri"""


class DenekNotFound(Exception):
    """denek bulunamadı hatası
    deneğin olamaması ya da deneğin denemede olmaması durumunda raise edilir"""

    pass
