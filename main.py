import pandas
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


main_url = 'https://9anime.to/home'
anime_to_download = pandas.read_csv('anime.csv', header=None, index_col=0, squeeze=True).to_dict()
df = pandas.read_csv('anime.csv', header=None, index_col=0, squeeze=True)

options = Options()
options.headless = True
driver = webdriver.Chrome('D:/New folder (2)/Chrom Driver/chromedriver.exe', options=options)
driver.get(main_url)
time.sleep(20)
html = driver.page_source
driver.quit()
projects_soup = BeautifulSoup(html, 'lxml')
c = projects_soup.find_all('a', {'class': 'name'})
anime_available = {}
for i in c:
    anime_available[i.text] = i['href']
video_link = {}
for anime, ep in anime_to_download.items():
    for name, link in anime_available.items():
        if anime == name:
            try:
                if ep == int(link[-1]) or ep == int(link[-2:]):
                    options = Options()
                    options.headless = True
                    driver = webdriver.Chrome('D:/New folder (2)/Chrom Driver/chromedriver.exe', options=options)
                    driver.get(link)
                    wait = WebDriverWait(driver, 10)
                    time.sleep(20)
                    frame = driver.find_elements_by_tag_name('iFrame')
                    wait.until(EC.frame_to_be_available_and_switch_to_it(frame[0]))
                    html2 = driver.page_source
                    driver.quit()
                    soup = BeautifulSoup(html2, 'lxml')
                    video_link[anime] = soup.find("video").get("src")
            except ValueError:
                pass

for i, j in video_link.items():
    print("Downloading file:%s" % i)
    r = requests.get(j, stream=True)
    with open('D:/anime/' + i, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

    print("%s downloaded!\n" % i)
    df[i] = df[i] + 1
    df.to_csv('anime.csv')

print("All videos downloaded!")








