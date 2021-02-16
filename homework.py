import datetime as dt

DATA_FORMAT = '%d.%m.%Y'


class Record:
    NOW = dt.datetime.now()

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if type(date) == str:
            date = dt.datetime.strptime(date, DATA_FORMAT)
        else:
            date = self.NOW
        self.date = date.date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = dt.datetime.now()
        self.today = self.today.date()

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        self.get_today_status = 0
        for recorded_object in self.records:
            if recorded_object.date == self.today:
                self.get_today_status += recorded_object.amount
        return self.get_today_status

    def get_week_stats(self):
        self.start_day_of_week = self.today
        self.day = 0
        self.get_week_status = 0
        while self.day < 7:
            for recorded_object in self.records:
                if recorded_object.date == self.start_day_of_week:
                    self.get_week_status += recorded_object.amount
            self.start_day_of_week -= dt.timedelta(days=1)
            self.day += 1
        return self.get_week_status

    def calculating_the_remained(self):
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        if self.limit > self.get_today_stats():
            return (f'Сегодня можно съесть что-нибудь '
                    f'ещё, но с общей калорийностью не '
                    f'более {self.calculating_the_remained()} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def get_today_cash_remained(self, currency):
        self.currency = currency
        self.get_today_status = self.get_today_stats()

        self.name_currency = {
            'rub': 'руб',
            'usd': 'USD',
            'eur': 'Euro'
        }
        self.the_remainded = self.calculating_the_remained()
        self.currency_list = {
            'rub': self.the_remainded,
            'usd': round((self.the_remainded / self.USD_RATE), 2),
            'eur': round((self.the_remainded / self.EURO_RATE), 2)
        }

        if self.get_today_status == self.limit:
            return 'Денег нет, держись'
        elif self.get_today_status < self.limit:
            return (f'На сегодня осталось '
                    f'{self.currency_list[self.currency]} '
                    f'{self.name_currency[self.currency]}')
        else:
            return (f'Денег нет, держись: твой долг - '
                    f'{abs(self.currency_list[self.currency])} '
                    f'{self.name_currency[self.currency]}')
