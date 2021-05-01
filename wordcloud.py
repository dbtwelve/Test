#웹 크롤링을 위한 import
from konlpy.tag import Okt
import nltk
from bs4 import BeautifulSoup
from collections import Counter
import requests

import re
from wordcloud import  WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


def text_convert(txtfile):
    text = ""
    with open('test.txt', encoding='utf-8') as f:
        text = ''.join(f.readlines())
    return text


def url_convert(url):
    text = ""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.find_all('div'):
            if item.has_attr('data-i18n'):
                #print(item.find_all(text=True))
                text = text + str(item.find_all(text=True))
            elif item.find_all(re.compile("h[1-9]"),text=True):
                #print(item.find_all(text=True))
                text = text + str(item.find_all(text=True))
            else:
                text = text + str(item.find_all(text=True))
        return text
    else:
        pass#print(response.status_code)


def url_convert2(url):
    result = []
    content = ""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find_all(['script', 'style', 'header', 'footer', 'form'])
        for item in script_tag:
            item.extract()

        content = soup.get_text()
        print(content)
        return content

def isEnglishOrKorean(text):
    kr_text = ""
    en_text = ""
    for c in text:
        if ord('가') <= ord(c) <= ord('힣'):
            kr_text += c
        elif ord('a') <= ord(c.lower()) <= ord('z'):
            en_text += c
    return kr_text, en_text

def get_noun(text):
    kr_text, en_text = isEnglishOrKorean(text)
    print(kr_text)
    engin = Okt()
    kr_nouns = [word for word in engin.nouns(kr_text) if len(word) >= 2]

    is_noun = lambda pos: pos[:2] == "NN"
    tokenized = nltk.word_tokenize(en_text)

    en_nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]

    nouns = kr_nouns + en_nouns



    count = Counter(nouns)
    noun_list = count.most_common(100)
    return noun_list


def get_noun2(text):

    engin = Okt()
    nouns = [word for word in engin.nouns(text) if len(word) >= 2]
    print(nouns)
    count = Counter(nouns)
    noun_list = count.most_common(100)
    return noun_list


def get_noun3(text):
    #cleaned_text = re.sub('[~!\@#$%^&*()_+=?]<>', '', text)
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]',
                          '', text)

    #print(cleaned_text)
    is_noun = lambda pos: pos[:2] == "NN"
    tokenized = nltk.word_tokenize(cleaned_text)

    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]

    count = Counter(nouns)
    noun_list = count.most_common(100)
    return noun_list

def visualize(list):

    mask = np.array(Image.open('cloud.png'))
    wc = WordCloud(background_color="white", mask=mask, font_path='font/NanumGothic.ttf').generate_from_frequencies(dict(list))
    wc.to_file('output.png')
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
file_type = "URL"
file_name = "test.txt"

URL="https://allganize.ai/"
URL = "http://www.naver.com"
URL = "http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf"
converted_text = ""
if file_type == "TXT":
    converted_text = text_convert(file_name)
elif file_type == "URL":
    converted_text = url_convert2(URL)
#cleaned_text = re.sub('[^A-Za-z0-9가-힣]', '', converted_text)

noun_list = get_noun3(converted_text)#get_noun(cleaned_text)
visualize(noun_list)



