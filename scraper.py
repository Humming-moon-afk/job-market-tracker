import requests
import bs4
#defined website
website = "https://www.stepstone.de/?ef_id=Cj0KCQjwg5zTBhCLARIsAP2AFU5nZ_1pQRODyFO6jggfgR4XzvYCEkbuZTBsSqSgNgVowhSu9W3hV38aAoMHEALw_wcB%3AG%3As&cid=SEA_GO_DE-DE-BRAND---E%7C%5BA%5D_c_stepstone--%7CBRAND001--_stepstone_FP_RSA1&loc_interest=&loc_physical=9042017&s_kwcid=AL%21523%213%21656170929052%21e%21%21g%21%21stepstone%2120029062170%21149789846153&adjust_t=1qeexpc4_1q2jhhw2&adjust_campaign=SEA_GO_DE-DE-BRAND---E%7C%5BA%5D_c_stepstone--%7CBRAND001--_stepstone_FP_RSA1&gad_source=1&gad_campaignid=20029062170&gbraid=0AAAAADj_ilV7D8k7z_2-FMV9QFx8a-Ihm&gclid=Cj0KCQjwg5zTBhCLARIsAP2AFU5nZ_1pQRODyFO6jggfgR4XzvYCEkbuZTBsSqSgNgVowhSu9W3hV38aAoMHEALw_wcB"
#get status and html
#header to identify
headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}
data = requests.get(website, headers=headers)
print(data.status_code)
soup = bs4.BeautifulSoup(data.text, "html.parser")