from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

import denemesonuc.models

def fetch(
    driver: WebDriver,
    ad: str,
    no: int,
    duzey: int,
    sehir: str,
    kurum: str,
    deneme: denemesonuc.models.DenemeLogin,
) -> denemesonuc.models.DenemeResult:
    """### denek ve deneme bilgileriyle eski tip deneme sonuçlarını çeker

    returns DenemeResult if successful
    raises DenekNotFound if denek did not take the test"""

    de = denemesonuc.models.DenemeResult()

    if deneme.logout_url:
        driver.get(deneme.logout_url)

    driver.get(deneme.url)

    seviye = Select(driver.find_element("id", "seviye"))
    seviye.select_by_visible_text(f"{str(duzey)}.Sınıf")

    ilkodu = Select(driver.find_element("id", "ilkodu"))
    ilkodu.select_by_visible_text(sehir)

    okuladi = driver.find_element("id", "kurumarama")
    okuladi.send_keys(kurum)
    WebDriverWait(driver, 2).until(EC.presence_of_element_located(("id", "ui-id-2")))
    okulasilad = driver.find_element("id", "ui-id-2")
    okulasilad.click()

    ogrnoinp = driver.find_element("id", "ogrencino")
    ogrnoinp.send_keys(str(no))

    ogradinp = driver.find_element("id", "isim")
    ogradinp.send_keys(ad)

    driver.find_element("name", "bulbtn1").submit()

    document = "/html/body/div[1]/section/div/div"
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(("xpath", f"{document}/div[1]"))
        )
    except TimeoutException as e:
        raise TimeoutException("denek probably did not take the test") from e

    deneme_select = Select(driver.find_element("id", "digersinavlarcombo"))
    deneme_type = deneme_select.first_selected_option.text
    if (deneme_type != deneme.deneme_adi) and deneme.deneme_adi:
        if deneme.deneme_adi in [i.text for i in deneme_select.options]:
            deneme_select.select_by_visible_text(deneme.deneme_adi)
            WebDriverWait(driver, 5).until(
                EC.text_to_be_present_in_element(
                    ("xpath", f"{document}/div[4]/div/div"), deneme.deneme_adi
                )
            )
        else:
            raise denemesonuc.models.DenekNotFound("denek did not take the test")

    derece_head = f"{document}/div[5]/div/div[3]/div"
    d_sinif = int(driver.find_element("xpath", f"{derece_head}/div[2]").text)
    d_kurum = int(driver.find_element("xpath", f"{derece_head}/div[3]").text)
    d_il = int(driver.find_element("xpath", f"{derece_head}/div[5]").text)
    d_genel = int(driver.find_element("xpath", f"{derece_head}/div[6]").text)
    de.drc = denemesonuc.models.DenemeDerece(d_sinif, d_kurum, d_il, d_genel)

    de.sinif = driver.find_element("xpath", f"{document}/div[1]/div[2]/div[3]").text.replace(
        "-", ""
    )  # 9larda "-9A" gibi, diğer sınıflarda "11A" gibi gözüküyor o yüzden

    de.puan = float(
        driver.find_element("xpath", f"{document}/div[5]/div/div[1]/div/div")
        .text.replace(",", ".")
        .split(" ")[-1]
    )  # "puanınız: 123,456" gibi göründüğü için

    available_heads = []
    i = 0
    while True:
        try:
            i += 1
            head = f"{document}/div[7]/div/div[{i}]/div[1]/div[2]/div[2]"
            if driver.find_element("xpath", f"{head}/div[1]").text:
                available_heads.append(head)
        except:
            break

    def getDers(name: str = "") -> denemesonuc.models.DersSonuc:
        """#### dersleri tek tek toplamak yerine yazılmış fonksiyon"""
        if name:
            matches = [
                head
                for head in available_heads
                if name == driver.find_element("xpath", head[:-14] + "/div[1]/div/div").text
            ]
            if not matches:
                return denemesonuc.models.DersSonuc()
            head = matches[0]
        else:
            head = f"{document}/div[6]/div/div/div[1]/div[2]/div[2]"  # genel sonuçlar her zaman vardır herhalde

        d_ss = int(driver.find_element("xpath", f"{head}/div[1]").text)
        d_ds = int(driver.find_element("xpath", f"{head}/div[2]").text)
        d_ys = int(driver.find_element("xpath", f"{head}/div[3]").text)
        d_bs = d_ss - d_ds - d_ys
        d_ns = float(driver.find_element("xpath", f"{head}/div[4]").text.replace(",", "."))
        return denemesonuc.models.DersSonuc(d_ds, d_ys, d_bs, d_ns, d_ss)

    de.genel = getDers()
    de.edb = getDers("Türkçe Testi Toplamı")
    de.trh = getDers("Tarih-1")
    de.cog = getDers("Coğrafya-1")
    de.din = getDers("Din Kül. ve Ahl. Bil.")
    de.mat = getDers("Matematik Testi Toplamı")
    de.fiz = getDers("Fizik")
    de.kim = getDers("Kimya")
    de.biy = getDers("Biyoloji")
    de.fel = getDers("Felsefe")
    de.sfl = getDers("Felsefe (Seçmeli)")

    return de
