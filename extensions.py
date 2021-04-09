import requests
import json
from config import keys

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Нельзя конвертировать  {base} в {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'{quote} - отсутствует в списке доступных валют.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'{base} - отсутствует в списке доступных валют.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException('Количество валюты должно быть числовым.')

        if float(amount) <= 0:
            raise APIException('Количество валюты должно быть больше 0.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = round(json.loads(r.content)[keys[base]] * float(amount), 2)

        return total_base