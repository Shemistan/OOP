import datetime as dt

DATA_FORMAT = '%d.%m.%Y'


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            date = dt.datetime.strptime(date, DATA_FORMAT)
        else:
            date = dt.datetime.now()
        self.date = date.date()


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self) -> int:
        today = dt.datetime.now()
        today = today.date()
        get_today_status = 0
        for recorded_object in self.records:
            if recorded_object.date == today:
                get_today_status += recorded_object.amount
        return get_today_status

    def get_week_stats(self) -> int:
        today = dt.datetime.now()
        today = today.date()
        return sum(
            recorded_object.amount for recorded_object in self.records
            if today >= recorded_object.date > (today - dt.timedelta(days=7)))

    def calculate_the_remained(self) -> int:
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str:
        get_today_status = self.calculate_the_remained()
        if get_today_status > 0:
            return ('Сегодня можно съесть что-нибудь '
                    'ещё, но с общей калорийностью не '
                    f'более {get_today_status} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def get_today_cash_remained(self, currency) -> str:
        the_remainded = self.calculate_the_remained()
        if the_remainded == 0:
            return 'Денег нет, держись'
        # Всю ночь голову ломал, другого выхода я не вижу.
        # Только 2 словаря.
        value_currency = {
            'rub': 1,
            'usd': self.USD_RATE,
            'eur': self.EURO_RATE
        }

        name_currency = {
            'rub': 'руб',
            'usd': 'USD',
            'eur': 'Euro'
        }
        the_remainded = round((the_remainded / value_currency[currency]), 2)
        if the_remainded > 0:
            return ('На сегодня осталось '
                    f'{the_remainded} {name_currency[currency]}')
        return ('Денег нет, держись: твой долг - '
                f'{abs(the_remainded)} {name_currency[currency]}')
