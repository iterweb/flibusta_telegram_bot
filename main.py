import cfscrape
import telebot
from bs4 import BeautifulSoup
import time
import random

TOKEN = ""

bot = telebot.TeleBot(TOKEN)
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}

scraper = cfscrape.CloudflareScraper()

chat = []

def parsing_post(finding_urls):
    download_links = []
    for link in finding_urls:
        url = scraper.get(link, headers=headers)
        html = BeautifulSoup(url.content, 'html.parser')
        title = html.find('h1', class_='title').text
        field = html.find('div', id='main').find_all('a')
        discription = html.find('div', id='main').find_all('p')

        try:
            f = field[36]['href']
            if '/b/' in f and not f.endswith('/read'):
                download_links.append('http://flibusta.is' + field[36]['href'])
        except:
            pass
        try:
            f = field[37]['href']
            if '/b/' in f and not f.endswith('/read'):
                download_links.append('http://flibusta.is' + field[37]['href'])
        except:
            pass
        try:
            f = field[38]['href']
            if '/b/' in f and not f.endswith('/read'):
                download_links.append('http://flibusta.is' + field[38]['href'])
        except:
            pass
        try:
            f = field[39]['href']
            if '/b/' in f and not f.endswith('/read'):
                download_links.append('http://flibusta.is' + field[39]['href'])
        except:
            pass

        send_telegram = ('\t\n').join((title +'\n', 'Автор: ' + field[34].text +'\n', discription[1].text
                                       +'\n')+tuple(download_links))
        idchat = str(chat[0])
        time.sleep(random.uniform(3, 5))
        scraper.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s' %(TOKEN, idchat, send_telegram))

        download_links.clear()


def parsing_url(user):

    finding_urls = []
    create_url = 'http://flibusta.is/booksearch?ask=%s' %user.replace(' ','+')

    url = scraper.get(create_url, headers=headers)
    html = BeautifulSoup(url.content, 'html.parser')
    link_name = html.find('div', id='main')

    for link in link_name.find_all('li'):
        for ls in link.find_all('a'):
            lss = ('http://flibusta.is' + ls['href'])
            if '/b/' in lss:
                finding_urls.append(lss)
    time.sleep(random.uniform(3, 5))
    if not finding_urls:

        idchat = str(chat[0])
        scraper.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=Ничего не найдено. Введите название '
                    'книги для поиска' % (TOKEN, idchat))

    else:
        return parsing_post(finding_urls)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    bot.reply_to(message, 'Привет ✌, %s! Я книжный бот, помогу тебе найти любую книгу на сайте Флибуста!\n\nДля поиска '
                          'введи название книги!'
                 %user_name)


@bot.message_handler(content_types=["text"])
def send_anytext(message):
    user = message.text.lower()
    chat_id = message.chat.id
    chat.clear()
    chat.append(chat_id)
    if user != '':
        bot.send_message(chat_id, 'Ищу книгу: ' + user)
        return parsing_url(user)


bot.polling()