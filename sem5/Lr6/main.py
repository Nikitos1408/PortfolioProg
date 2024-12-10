import time
import json
import requests
from datetime import datetime
from xml.etree import ElementTree as ET

class CurrenciesList:

    def __init__(self, desired_currencies=None):
        self.url = "http://www.cbr.ru/scripts/XML_daily.asp"
        self.desired_currencies = desired_currencies

    def operation(self):
        """Получает курсы валют с сайта ЦБ РФ и возвращает словарь."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            currencies = {}
            for valute in root.findall('.//Valute'):
                Name = valute.find('Name').text  # Get the Name element
                if self.desired_currencies is None or Name in self.desired_currencies: #Filter by Name
                    CharCode = valute.find('CharCode').text
                    Nominal = int(valute.find('Nominal').text)
                    Value = float(valute.find('Value').text.replace(",", "."))
                    currencies[CharCode] = {'Nominal': Nominal, 'Name': Name, 'Value': Value}
            return currencies
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к ЦБ РФ: {e}")
            return None
        except ET.ParseError as e:
            print(f"Ошибка при парсинге XML: {e}")
            return None


class Decorator:
    _component = None

    def __init__(self, component):
        self._component = component

    def operation(self):
        return self._component.operation()


class ConcreteDecoratorJSON(Decorator):
    def operation(self):
        data = super().operation()
        if data:
            return json.dumps(data, ensure_ascii=False, indent=4)
        else:
            return None


class ConcreteDecoratorCSV(Decorator):
    def operation(self):
        data = super().operation()
        if data:
            try:
                output = []
                header = ['CharCode', 'Nominal', 'Name', 'Value']
                output.append(header)
                for char_code, valute_data in data.items():
                    row = [char_code, valute_data['Nominal'], valute_data['Name'], valute_data['Value']]
                    output.append(row)
                return self.write_csv(output)
            except AttributeError:
                try:
                    data = json.loads(data)
                    output = []
                    header = ['CharCode', 'Nominal', 'Name', 'Value']
                    output.append(header)
                    for char_code, valute_data in data.items():
                        row = [char_code, valute_data['Nominal'], valute_data['Name'], valute_data['Value']]
                        output.append(row)
                    return self.write_csv(output)
                except json.JSONDecodeError:
                    print("Error: Invalid JSON data received.")
                    return None
        else:
            return None

    def write_csv(self, data):
        output = ""
        for row in data:
          output +=  ";".join(map(str, row)) + "\n"
        return output


if __name__ == "__main__":

    desired_currencies = ['Доллар США', 'Евро']
    currencies = CurrenciesList(desired_currencies)

    print("Базовый вариант (словарь):\n", currencies.operation())
    json_decorator = ConcreteDecoratorJSON(currencies)
    print("\nJSON формат:\n", json_decorator.operation())
    csv_decorator = ConcreteDecoratorCSV(currencies)
    print("\nCSV формат:\n", csv_decorator.operation())
    csv_decorator_from_json = ConcreteDecoratorCSV(ConcreteDecoratorJSON(currencies))
    print("\nCSV формат (через JSON):\n", csv_decorator_from_json.operation())