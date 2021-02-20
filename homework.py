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
        return sum(
            recorded_object.amount for recorded_object in self.records
            if recorded_object.date == today)

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
    RUB_RATE = 1

    def get_today_cash_remained(self, currency) -> str:
        the_remainded = self.calculate_the_remained()
        if the_remainded == 0:
            return 'Денег нет, держись'

        name_currency = {
            'rub': {'value': self.RUB_RATE,
                    'name': 'руб'},
            'usd': {'value': self.USD_RATE,
                    'name': 'USD'},
            'eur': {'value': self.EURO_RATE,
                    'name': 'Euro'}
        }

        the_remainded = (
            round((the_remainded / name_currency[currency]['value']), 2))
        if the_remainded > 0:
            return ('На сегодня осталось '
                    f'{the_remainded} {name_currency[currency]["name"]}')
        return ('Денег нет, держись: твой долг - '
                f'{abs(the_remainded)} {name_currency[currency]["name"]}')
