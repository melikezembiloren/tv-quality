# Hangi hata türü hangi istasyonda ortaya çıkıyor — üretim hattının fiziksel akışına göre
# elle belirlenmiş bir eşleme. Yeni bir hata kategorisi eklenip burada tanımlanmazsa
# sessizce kaybolmasın diye "Diğer" kovasına düşer.
#
# Bu dosya defect_dashboard ve monthly_report repository'leri arasında paylaşılıyor
# ki iki yerde birbirinden sapan iki kopya oluşmasın.
STATION_BY_CATEGORY_CODE: dict[str, str] = {
    "FACTORY_RESET": "Montaj",
    "ARKA_KAPAK": "Montaj",
    "HOPARLOR": "Montaj",
    "ON_CERCEVE_LOGO": "Montaj",
    "KULAKLIK": "Montaj",
    "ALT_KAPAK": "Montaj",
    "SINYAL": "Montaj",
    "PANEL": "Montaj",
    "BARKOD": "Paketleme",
    "STRAFOR": "Paketleme",
    "AKSESUAR": "Paketleme",
}
