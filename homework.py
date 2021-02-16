import datetime as dt


class Record:
    def __init__(self, amount, comment, date=dt.datetime.now()):
        self.amount = amount
        self.comment = comment
        if type(date) == str:
            date = date.replace('.', '')
            date = dt.datetime.strptime(date, '%d%m%Y')
        self.date = date.date()

    def return_amount(self):
        return self.amount

    def return_date(self):
        return self.date


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.get_today_status = 0
        self.day = 0

    def add_record(self, record):
        self.records.append(record)

    def get_one_day_stats(self):
        self.get_today_status = 0
        for i in self.records:
            if i.return_date() == self.today:
                self.get_today_status += i.return_amount()
        return self.get_today_status

    def get_today_stats(self):
        self.today = dt.datetime.now()
        self.today = self.today.date()
        return self.get_one_day_stats()

    def get_week_stats(self):
        self.today = dt.datetime.now()
        self.today = self.today.date()
        self.week_status = 0
        self.day = 0
        while self.day < 7:
            self.week_status += self.get_one_day_stats()
            self.today -= dt.timedelta(days=1)
            self.day += 1
        return self.week_status

    def the_remained(self):
        return abs(self.limit - self.get_today_stats())


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        if self.limit > super().get_today_stats():
            return (f'Сегодня можно съесть что-нибудь '
                    f'ещё, но с общей калорийностью не '
                    f'более {self.the_remained()} кКал')
        else:
            return f'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def get_today_cash_remained(self, currency):
        self.currency_list = {}
        self.currency = currency
        self.get_today_status = self.get_today_stats()

        self.name_currency = {
            'rub': 'руб',
            'usd': 'USD',
            'eur': 'Euro'
        }

        self.currency_list = {
            'rub': self.the_remained(),
            'usd': round((self.the_remained() / self.USD_RATE), 2),
            'eur': round((self.the_remained() / self.EURO_RATE), 2)
        }

        if self.get_today_status < self.limit:
            return (f'На сегодня осталось '
                    f'{self.currency_list[self.currency]} '
                    f'{self.name_currency[self.currency]}')
        elif self.get_today_status == self.limit:
            return f'Денег нет, держись'
        else:
            return (f'Денег нет, держись: твой долг - '
                    f'{abs(self.currency_list[self.currency])} '
                    f'{self.name_currency[self.currency]}')
