import datetime as dt
from typing import Optional


class Calculator:
    def __init__(self, limit):
        self.records = []
        self.limit = limit

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        values = [rec.amount for rec in self.records
                  if rec.date == today]
        today_amount = sum(values)
        return today_amount

    def get_week_stats(self):
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        """Берем интервал 7 дней, включая сегодня"""
        values = [rec.amount for rec in self.records if
                  today >= rec.date > week_ago]
        week_amount = sum(values)
        return week_amount


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        today_amount = self.get_today_stats()
        week_amount = self.get_week_stats()
        today_remain = self.limit - today_amount
        if today_remain > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей'
                    f' калорийностью не более {today_remain} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency):
        today_amount = self.get_today_stats()
        week_amount = self.get_week_stats()
        currencies = {
            'usd': [self.USD_RATE, "USD"],
            'eur': [self.EURO_RATE, "Euro"],
            'rub': [self.RUB_RATE, "руб"]
        }
        if currency not in currencies:
            return f'Валюты {currency} нету в нашей базе данных!'
        today_remain = self.limit - today_amount
        rem_cash_value = today_remain / currencies[currency][0]
        rounded_value = round(rem_cash_value, 2)
        abs_cash_value = abs(rounded_value)
        if rem_cash_value > 0:
            return (f'На сегодня осталось {rounded_value}'
                    f' {currencies[currency][1]}')
        elif rem_cash_value == 0:
            return 'Денег нет, держись'
        return (f'Денег нет, держись: твой долг - {abs_cash_value}'
                f' {currencies[currency][1]}')


class Record:
    def __init__(self, amount, comment, date: Optional[str] = None):
        self.amount = amount
        if date is not None:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = dt.date.today()
        self.comment = comment
