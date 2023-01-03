from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from bs4 import BeautifulSoup
import requests
from http import HTTPStatus

BASE_URL = 'https://www.pais.co.il/lotto/showMoreResults.aspx?fromIndex=0&amount=49&fromNumber={}&toNumber={}'
STRONG_NUM_INDEX = 3


def scrap(req, game_number):
    try:
        url = BASE_URL.format(game_number,game_number)
        response = requests.get(url=url)
        if response.status_code != HTTPStatus.OK: 
            print('failed to fetch,', 'for req', req)
            return HttpResponse(status=response.status_code)
        try:
            data = winning_numbers_parser(response.text)
        except Exception as e:
            return HttpResponse(status=HTTPStatus.NO_CONTENT)
            
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return HttpResponse(status=response.status_code)   

def winning_numbers_parser(data):
    parser = BeautifulSoup(data, 'html.parser')
    numbers = parser.find_all('li',{'class': 'loto_info_num archive'})
    if len(numbers) == 0:
        raise Exception('scrapper faild')
    winning_numbers = {"numbers": []}
    for number in numbers:
        winning_numbers["numbers"].append(number.div.text)
    str_num_divs = parser.find('div',{'class': 'loto_info_num strong archive'})
    winning_numbers["strong_num"] = str_num_divs.contents[STRONG_NUM_INDEX].text
    return winning_numbers