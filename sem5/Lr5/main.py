import requests
from xml.etree import ElementTree as ET
import time
import pandas as pd
import matplotlib.pyplot as plt

class Currency:
    def __init__(self, currencies_ids_lst: list):
        self.__currencies_ids_lst = currencies_ids_lst
        self.__result = self.get_currencies()

    def __del__(self):
        print("Deleting Currency object...")

    def get_currencies(self) -> list:
        #проверка на время запроса
        last_request_time = 0  
        current_time = time.time()
        if current_time - last_request_time < 5: #проверка и ограничение времени запроса на 5 секунд
            time.sleep(5 - (current_time - last_request_time))

        #обращение к сайту
        cur_res_str = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
        current_time = time.time()
        last_request_time = current_time
        result = []

        root = ET.fromstring(cur_res_str.content)
        valutes = root.findall("Valute")
        for _v in valutes:
            valute_id = _v.get('ID')
            valute = {}
            if str(valute_id) in self.__currencies_ids_lst:
                valute_cur_name, valute_cur_val = _v.find('Name').text, _v.find('Value').text
                valute_charcode = _v.find('CharCode').text
                valute[valute_charcode] = (valute_cur_name, valute_cur_val)
                if valute_cur_val != '1': #проверка на номинал - 1
                    valute[valute_charcode] = (valute_cur_name, valute_cur_val)
                result.append(valute)

        return result

    #Создание графика
    def visualize_currencies(self):
        data = self.get_currencies()
        if not data:
            print("Нет данных")
            return

        gr_names = []
        for valute in data:
            for charcode, (name, value) in valute.items():
                gr_names.append(charcode)
        
        gr_values = []
        for valute in data:
            for charcode, (name, value) in valute.items():
                if charcode in gr_names:
                    gr_values.append(float(value.replace(",", ".")))

        plt.figure(figsize=(10, 3))
        plt.bar(gr_names, gr_values, color='blue')
        plt.title('Курс валют')
        plt.xlabel('Название валюты')
        plt.ylabel('Цена')
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.savefig('currencies.jpg')
        plt.close()
        print("График сохранён как currencies.jpg")

    @property
    def currencies_ids_lst(self):
        return self.__currencies_ids_lst

    @currencies_ids_lst.setter
    def currencies_ids_lst(self, value: list):
        if isinstance(value, list):
            self.__currencies_ids_lst = value
            self.__result = self.get_currencies()
        else:
            raise TypeError("Must be a list")

    @property
    def result(self):
        return self.__result

    @result.setter
    def result(self, value: list):
        if isinstance(value, list):
            self.__result = value
        else:
            raise TypeError("Result must be a list")

if __name__ == '__main__':

    cur = Currency(['R01035', 'R01235', 'R01239'])
    if cur:
        print(cur.result)
        cur.visualize_currencies() # Call the new method
