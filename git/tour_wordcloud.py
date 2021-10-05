# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import pandas as pd

df = pd.read_csv("tour_place.csv")
df

import konlpy 

# +
import re

# 텍스트 정제 함수 : 한글 이외의 문자는 전부 제거
def text_cleaning(text):
    # 한글의 정규표현식으로 한글만 추출
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    result = hangul.sub('', str(text))
    return result


# +
# 함수를 적용하여 리뷰에서 한글만 추출

df['text'] = df['ETC_CN'].apply(lambda x: text_cleaning(x))
del df['ETC_CN']

# 한 글자 이상의 텍스트를 가지고 있는 데이터만 추출합니다
df = df[df['text'].str.len() > 0]
df.head(20)
type(df)
# -

# 의미없는 문자 공백으로 바꾸기
# , "있는": ' ', "있어요": ' ',"없는": ' ' ,"입니다": ' ', "같았어요": ' ' , "있었습니다": ' '})
df['text'] = df['text'].str.replace("있습니다", ' ')

df['text'][0]

# +
text = df['text'][0]

text_list = "".join(text)

text_list = text_list.replace('.', ' ').replace('"',' ').replace(',',' ').replace("'"," ").replace('·', ' ').replace('=',' ').replace('\n',' ')

text_list

# +
# 단어를 형태소 단위로 추출

from konlpy.tag import Okt
okt = Okt()
def get_pos(x):
    tagger = Okt()
    pos = tagger.pos(x)
    pos = ['{}/{}'.format(word,tag) for word, tag in pos]
    return pos


get_pos(df['text'][0])
# 형태소 추출 동작을 테스트합니다.
# -

df['meaning_word'] = ""

# +
from konlpy.tag import Okt

meaning_word = []
okt = Okt()
def get_pos(x):
    tagger = Okt()
    pos = tagger.pos(x)
    for word, tag in pos:
        if tag in ['Noun','Adjective', 'verb']:
            meaning_word.append(word)
            meaning_word_list = " ".join(meaning_word)
            meaning_word_list = meaning_word_list.replace('.', ' ').replace('"',' ').replace(',',' ').replace("'"," ").replace('·', ' ').replace('=',' ').replace('\n',' ')
#             df['meaning_word_list'] = meaning_word_list
    
            
#     meaning_word_list = "".join(meaning_word)
#     df['meaning_word_list'][x] = meaning_word_list
    return meaning_word_list

#     for i in range(46):
#         meaning_word = get_pos(df['text'][i])
#         meaning_word_list = "".join(meaning_word)
#         meaning_word_list = meaning_word_list.replace('.', ' ').replace('"',' ').replace(',',' ').replace("'"," ").replace('·', ' ').replace('=',' ').replace('\n',' ')
#         df['meaning_word_list'] = meaning_word_list
  
    
    
i = 45
    

meaning_word = get_pos(df['text'][i])
df["meaning_word"][i] = meaning_word


df["meaning_word"]

df.to_csv("C:/Users/mubit/OneDrive/바탕 화면/PNU 해커톤/tour_explain.csv")


# df = pd.read_csv("C:/Users/mubit/OneDrive/바탕 화면/PNU 해커톤/tour_word.csv")
# df

# +
worddf = pd.read_csv("/tour_explain.csv")

worddf
# -

worddf['meaning_word'][0]

# +
# td-idf 형태로 변환

from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np

corpus = worddf['meaning_word']

vect = CountVectorizer()
document_term_matrix = vect.fit_transform(corpus)       # 문서-단어 행렬 

tf = pd.DataFrame(document_term_matrix.toarray(), columns=vect.get_feature_names())  
                                             # TF (Term Frequency)
D = len(tf)
ddf = tf.astype(bool).sum(axis=0)
idf = np.log((D+1) / (ddf+1)) + 1             # IDF (Inverse Document Frequency)

# TF-IDF (Term Frequency-Inverse Document Frequency)
tfidf = tf * idf                      
tfidf = tfidf / np.linalg.norm(tfidf, axis=1, keepdims=True)
# -

tfidf

import matplotlib.pyplot as plt
import nltk 
from konlpy.tag import Kkma
from konlpy.tag import Twitter
from wordcloud import WordCloud

# +
# 첫 번째 행의 텍스트를 리스트로 만들기

text = worddf['meaning_word']

text_list = "".join(text)

# text_list = text.replace('.', ' ').replace('"',' ').replace(',',' ').replace("'"," ").replace('·', ' ').replace('=',' ').replace('\n',' ').replace("있습니다", ' '))

text_list

# -

tfidf["가시"][1]

# +
i = 46

a = tfidf.iloc[i]
a = dict(a)

wordcloud = WordCloud().generate(text_list)

font = 'C:/Windows/Fonts/NanumGothic_1.ttf'

wc = WordCloud(font_path=font,\
		background_color="white", \
		width=1000, \
		height=1000, \
		max_words=100, \
		max_font_size=300)

wc = wc.generate_from_frequencies(a)
wc.to_file('wordcloud_{}.jpg'.format(i))



plt.figure(figsize=(10,10))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()


for i in range(45):
    a = tfidf.iloc[i]
    a = dict(a)

    wordcloud = WordCloud().generate(text_list)

    font = 'C:/Windows/Fonts/NanumGothic_1.ttf'

    wc = WordCloud(font_path=font,\
            background_color="white", \
            width=1000, \
            height=1000, \
            max_words=100, \
            max_font_size=300)

    wc = wc.generate_from_frequencies(a)
    wc.to_file('wordcloud_{}.jpg'.format(i))



    plt.figure(figsize=(10,10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    


# 있다, 입니다, 있는, 있습니다, 있었습니다, 없는, 있다는, 같아요, 같았어요
# -



def color_func(word, font_size, position,orientation,random_state=None, **kwargs):
    return("hsl({:d},{:d}%, {:d}%)".format(np.random.randint(212,313),np.random.randint(26,32),np.random.randint(45,80)))


