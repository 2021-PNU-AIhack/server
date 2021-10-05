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

import requests
import xmltodict
import json
import pandas as pd

df = pd.read_csv("/Users/kimmiso/Desktop/PNU 해커톤/tour_info1.csv")

df["image"] = ""
df["id"] = ""
df["관광소요시간"] = ""
df["예측혼잡도"] = ""
df["혼잡도레벨"] = ""


# +
def keyword_search_data(keyword, i):
    url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/searchKeyword'

    params = {
        'ServiceKey': "6gkOfxSEGnHWBsLb9+J9JYGA6h519yt6M0wBx4YGpWFXl2+nDrWmSOSpqCeMDkIRjn3VM6irah6lnnVygRtBYQ==",
        'MobileApp': 'AppTest',
        'MobileOS': 'ETC',
        'pageNo': '1',
        'areaCode': '6',
        'keyword': keyword,
    }

    res = requests.get(url, params=params)
    # res.text
    # res.url

    # xml to dict
    data = xmltodict.parse(res.text)

    # dict to json
    json_data = json.dumps(data)

    # json to dict
    dict_data = json.loads(json_data)
    dict_data['response']['header']['resultCode']  # 0000
    dict_data = dict_data['response']['body']['items']['item']
    
    
    addr = dict_data['addr1']
    contentid = dict_data['contentid']
    firstimage = dict_data['firstimage']
    title = dict_data['title']
    
    df["image"][i] = firstimage
    df["id"][i] = contentid
    
    result = {'addr':addr, 'contentid':contentid, 'firstimage':firstimage, 'title':title} 
    

    return result


keyword_search_data()
# -

df

for i in range(45):
    title = df["PLACE_NM"][i]
    keyword_search_data(title, i)


# +
def more_information(contentId, i):
    url = 'http://api.visitkorea.or.kr/openapi/service/rest/DataLabService/tarTursmRqmtList'

    params = {
        'ServiceKey': "6gkOfxSEGnHWBsLb9+J9JYGA6h519yt6M0wBx4YGpWFXl2+nDrWmSOSpqCeMDkIRjn3VM6irah6lnnVygRtBYQ==",
        'MobileApp': 'AppTest',
        'MobileOS': 'ETC',
        'pageNo': '1',
        'baseYm': '202107',
        'contentId': contentId,
    }

    res = requests.get(url, params=params)
    # xml to dict
    data = xmltodict.parse(res.text)

    # dict to json
    json_data = json.dumps(data)

    # json to dict
    dict_data = json.loads(json_data)
    dict_data['response']['header']['resultCode']  # 0000
    dict_data = dict_data['response']['body']['items']['item']
    
    

    time = dict_data['avgTursmRqmtTm']
    
    
    df["관광소요시간"][i] = time
    return time

more_information(126078)


# +
def deco_info(contentId, i):
    
    
    #http://api.visitkorea.or.kr/openapi/service/rest/DataLabService/tarDecoList?serviceKey=6gkOfxSEGnHWBsLb9%2BJ9JYGA6h519yt6M0wBx4YGpWFXl2%2BnDrWmSOSpqCeMDkIRjn3VM6irah6lnnVygRtBYQ%3D%3D&pageNo=1&numOfRows=10&MobileOS=ETC&MobileApp=AppTest&startYmd=20210811&endYmd=20210927&contentId=126078
    url = "http://api.visitkorea.or.kr/openapi/service/rest/DataLabService/tarDecoList"
    
    
    params = {
        'ServiceKey': "6gkOfxSEGnHWBsLb9+J9JYGA6h519yt6M0wBx4YGpWFXl2+nDrWmSOSpqCeMDkIRjn3VM6irah6lnnVygRtBYQ==",
        'MobileApp': 'AppTest',
        'MobileOS': 'ETC',
        'pageNo': '1',
        'startYmd': '20210927',
        'endYmd':'20210927',
        'contentId': contentId,
    }

    res = requests.get(url, params=params)
    # xml to dict
    data = xmltodict.parse(res.text)

    # dict to json
    json_data = json.dumps(data)

    # json to dict
    dict_data = json.loads(json_data)
    dict_data['response']['header']['resultCode']  # 0000
    dict_data = dict_data['response']['body']['items']['item']
    
    DecoRat = dict_data["estiDecoRat"]
    Decolevel = dict_data["estiDecoDivCd"]
    estiNum = dict_data["estiNum"]
    
    df["예측혼잡도"][i] = DecoRat
    df["혼잡도레벨"][i] = Decolevel
    
    
    

    return dict_data

    
deco_info()    
    
# estiDecoRat = 예측혼잡도 비율
# estiDecoDivCd = 구분코드 (1:쾌적, 2:여유, 3:보통, 4:약간혼잡, 5:혼잡)
# estiNum  = 예측 방문객수 
# -
for i in range(45):
    id = df['id'][i]
    more_information(id, i)
    deco_info(id, i)

df.to_csv("/Users/kimmiso/Desktop/PNU 해커톤/tour_info1.csv")



