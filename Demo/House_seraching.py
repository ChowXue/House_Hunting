# -*- coding: UTF-8 -*-


import requests, traceback, csv, time, random
from bs4 import BeautifulSoup
from tqdm import tqdm

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

def getHTMLText(url):
    try:
        r = requests.get(url, headers=header, allow_redirects=False)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        print("")

def getHouseInfo():
    url = 'http://nj.58.com/chuzu/pn{page}/'
    output_file = 'HouseInfo.csv'
    csv_file = open(output_file, 'w', encoding='utf-8-sig')
    file = csv.writer(csv_file, delimiter=',')
    for n in tqdm(range(1,70)):
        time.sleep(random.randint(5,10))
        html = getHTMLText(url.format(page=n))
        soup = BeautifulSoup(html, 'html.parser')
        houseInfo = soup.find_all('div', attrs={'class': 'des'})
        priceInfo = soup.find_all('div', attrs={'class': 'listliright'})
        for i in range(len(houseInfo)):
            try:
                if houseInfo[i] == []:
                    continue
                houseUrl = houseInfo[i].find('h2').a['href']
                title = houseInfo[i].find('h2').a.string.strip()
                location = houseInfo[i].find('p', attrs={'class': 'add'}).find_all('a')
                houseLoc = location[0].string + location[1].string.split('.')[0]
                price = priceInfo[i].find('div', attrs={'class': 'money'}).b.string + '元/月'
                file.writerow([title + " " + price, houseLoc, houseUrl])
            except:
                continue

if __name__ == '__main__':
    getHouseInfo()



