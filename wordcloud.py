#웹 크롤링을 위한 import
from bs4 import BeautifulSoup
import requests

#wordcloud import
import re
from wordcloud import  WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


def text_convert(txtfile):
    text = "The Harry Potter series, written by J.K. Rowling, is perhaps the most popular set of novels of the modern era. With seven books and many blockbuster films to its name, the series has amassed about 15 billion dollars in sales. How did this phenomenon become what it is? For those scratching their heads, the reason can be broken down into several areas: Rowling garnered a generous initial contract for her book, separate book covers were created for both teens and adults, midnight releases/promotions/pre-orders made the public more fanatic about the series, and fan blogs were rampant. In fact, these are just a few of the main reasons why the Harry Potter took off the way it did.\n\nThe first book in the series, “Harry Potter and the Philosopher’s Stone,” was rejected 12 times before it was picked up by Bloomsbury—a small publisher in England. At the time, Rowling was living on benefits as a single mother, so receiving this contract was her first step to success. However, getting a book contract does not ensure the success of a book. The story was adored by children and adults alike, and this had much to do with the popularity of the initial book and the series as a whole (Rappaport, Sarah).\n\nIn light of this, her publisher made separate covers for young readers and adults. According to BusinessInsider.com, “Adults love reading the Harry Potter books, but few want to be seen toting around a child’s book. To make it easier for adults, Bloomsbury Publishing, the British publishing house that first bought the rights to Rowling’s books, published a second version of the books with “adult” (i.e., less colorful and more boring) book covers” (Aquino, Judith). This made it easier for a full range of ages to enjoy the series. This is not an easy feat for young adult fiction.\n\nAnother factor that worked like a charm was that when the Harry Potter series became an obvious success, the publisher, and Rowling herself through her own website for the books, conducted midnight releases, special promotions, and pre-ordering to engage readers even more. According to BusinessInsider.com, “Starting with the fourth book, Harry Potter and the Goblet of Fire, crowds of people wearing black robes, ties and round-frame glasses began showing up at bookstores for midnight release parties in 2000. Customers who feared their local bookstore would run out of copies responded by pre-ordering over 700,000 copies prior to the July 8, 2000 release date, according to Gunelius. The seventh and final book in the Harry Potter series became the fastest-selling book in history, reports The New York Times, with more than 11 million copies sold during the first 24 hours in three markets alone” (Aquino, Judith). The fandom around the books created more lucrative opportunities for the series.\n\nAlso, based on fans, blogs were created that were dedicated to the story, details, plot, characters, and much more about the series. In the beginning, Rowling did not have too much in the way of advertising, and the fans did a lot of work for her. According to HubSpot, “The fans took over and created many viral campaigns on her behalf talking about the excitement they had over upcoming releases. Harry Potter is often a trending topic on Twitter, Facebook events and page are abundant and thousands of bloggers create posts on their behalf. These promotions are more genuine because they come from the source, the fans, instead of the person who makes a profit” (Leist, Rachel). This organic advertising propelled the Harry Potter novel series into being the most successful one ever.\n\nNow that Rowling has sold millions of copies of her Harry Potter books and has seen each one adapted into films, merchandise, fan art, and more, we can safely say that this series is a global phenomenon. Through an initial contract, advertising for both teens and adults, special releases and parties, and organic advertising from fans via the internet, Harry Potter and his universe took over as the most successful bestselling book of all time. \n"
    with open('test.txt', encoding='utf-8') as f:
        text = ''.join(f.readlines())
    return text


def url_convert(url):
    text = ""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        for item in soup.find_all('div'):
            if item.has_attr('data-i18n'):
                print(item.find_all(text=True))
                text = text + str(item.find_all(text=True))
            elif item.find_all(re.compile("h[1-9]"),text=True):
                print(item.find_all(text=True))
                text = text + str(item.find_all(text=True))
            else:
                text = text + str(item.find_all(text=True))
        return text
    else:
        print(response.status_code)


file_type = "URL"
file_name = "test.txt"
URL = "https://allganize.ai"
#URL = "http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf"
converted_text = ""
if file_type == "TXT":
    converted_text = text_convert(file_name)
elif file_type == "URL":
    converted_text = url_convert(URL)

mask = np.array(Image.open('cloud.png'))
wc = WordCloud(background_color="white",mask=mask).generate(converted_text)
wc.to_file('output.png')
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()
