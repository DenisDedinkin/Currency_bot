import json
import requests
from config import keys

class ConvertionException(Exception):
    pass

class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты!')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f"Валюта {base} не найдена!")
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f"Валюта {quote} не найдена!")
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}")
        total_quote = json.loads(r.content)[keys[quote]]
        res = total_quote * float(amount)
        res = round(res, 2)
        text = f"Цена {amount} {base} в {quote} - {res}"
        return text