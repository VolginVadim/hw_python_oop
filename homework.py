import datetime as dt
from typing import Optional


class Calculator:
    def __init__(self, limit):
        self.records=[]
        self.limit=limit

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_amount=0
        for record in self.records:
            if record.date==dt.date.today():
               today_amount+=record.amount
        return today_amount

    def get_week_stats(self):
        today=dt.date.today()
        week_ago=today-dt.timedelta(days=7)
        week_amount=0
        for record in self.records:
            if today>=record.date>=week_ago:
                week_amount+=record.amount
        return week_amount


class CaloriesCalculator(Calculator):
        def __init__(self, limit):
            self.limit=limit
            super().__init__(self.limit)

        def get_today_stats(self):
            amount=super().get_today_stats()
            return f'{amount} калорий уже съедено сегодня.'

        def get_calories_remained(self):
            calories_value=self.limit-super().get_today_stats()
            if calories_value>0:
                return (f'Сегодня можно съесть что-нибудь ещё, но с общей'
                        f' калорийностью не более {calories_value} кКал')
            else:
                return 'Хватит есть!'
                
        def get_week_stats(self):
            week_calories=super().get_week_stats()
            return f'{week_calories} калорий получено за последние 7 дней'


class CashCalculator(Calculator):
        USD_RATE=60.0
        EURO_RATE=70.0
        RUB_RATE=1

        def __init__(self, limit):
            self.limit=limit
            super().__init__(self.limit)

        def get_today_stats(self):
            amount=super().get_today_stats()
            return f'{amount} денег потрачено сегодня сегодня.'

        def get_today_cash_remained(self, currency):
            currencies={
            'usd': [self.USD_RATE, "USD"],
            'eur': [self.EURO_RATE, "Euro"],
            'rub': [self.RUB_RATE, "руб"]
            }
            if currency not in currencies:
                return f'Валюты {currency} нету в нашей базе данных!'
            money_left=self.limit-super().get_today_stats()
            money_value=money_left/currencies[currency][0]
            rounded_value=round(money_value, 2)
            if money_value>0:
                return (f'На сегодня осталось {rounded_value}'
                f' {currencies[currency][1]}')
            elif money_value==0:
                return 'Денег нет, держись'
            else:
                abs_money_value=abs(rounded_value)
                return (f'Денег нет, держись: твой долг - {abs_money_value}'
                f' {currencies[currency][1]}')

        def get_week_stats(self):
            week_money=super().get_week_stats()
            return f'{week_money} денег потрачено за последние 7 дней'


class Record:
    def __init__(self, amount, comment, date: Optional[str]=None):
        self.amount=amount
        if date != None:
            self.date=dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date=dt.date.today()
        self.comment=comment