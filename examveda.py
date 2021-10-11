import requests

from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / '
                  '92.0.4515.159Safari / 537.36', 
}
url = "https://www.examveda.com/mcq-question-on-competitive-english/"

r = requests.get(url, headers=headers)
htmlContent = r.content
soup = BeautifulSoup(htmlContent, 'html.parser')
soup = soup.select('.page-shortcode')[0].select('a')

for category in soup:
    print(category['href'], category.text)
