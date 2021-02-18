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

    def determine_what_day_it_is(self):
        self.today = dt.datetime.now()
        self.today = self.today.date()
        return self.today

    def get_today_stats(self):
        self.determine_what_day_it_is()
        get_today_status = 0
        for recorded_object in self.records:
            if recorded_object.date == self.today:
                get_today_status += recorded_object.amount
        return get_today_status

    def weekend(self):
        self.determine_what_day_it_is()
        start_day_of_week = self.today
        self.a_week = []
        self.a_week.append(start_day_of_week)
        for day in range(7):
            start_day_of_week -= dt.timedelta(days=1)
            self.a_week.append(start_day_of_week)

    def get_week_stats(self):
        self.weekend()
        self.determine_what_day_it_is()
        get_week_status = 0
        for recorded_object in self.records:
            if recorded_object.date in self.a_week:
                get_week_status += recorded_object.amount
        return get_week_status

    def calculate_the_remained(self):
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        get_today_status = self.get_today_stats()
        if self.limit > get_today_status:
            return ('Сегодня можно съесть что-нибудь '
                    'ещё, но с общей калорийностью не '
                    f'более {self.calculate_the_remained()} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def get_today_cash_remained(self, currency):
        get_today_status = self.get_today_stats()
        if get_today_status == self.limit:
            return 'Денег нет, держись'
        self.name_currency = {
            'rub': 'руб',
            'usd': 'USD',
            'eur': 'Euro'
        }
        the_remainded = self.calculate_the_remained()
        if currency == 'usd':
            the_remainded = round((the_remainded / self.USD_RATE), 2)
        elif currency == 'eur':
            the_remainded = round((the_remainded / self.EURO_RATE), 2)

        if self.limit > get_today_status:
            return (f'На сегодня осталось '
                    f'{the_remainded} '
                    f'{self.name_currency[currency]}')

        return ('Денег нет, держись: твой долг - '
                f'{abs(the_remainded)} {self.name_currency[currency]}')
