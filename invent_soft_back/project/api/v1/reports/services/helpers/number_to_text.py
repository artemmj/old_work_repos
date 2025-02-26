import decimal

from apps.helpers.services import AbstractService


class NumberToTextService(AbstractService):
    def __init__(self) -> None:
        self.units = (
            u'ноль', (u'один', u'одна'), (u'два', u'две'),
            u'три', u'четыре', u'пять', u'шесть', u'семь', u'восемь', u'девять')
        self.teens = (
            u'десять', u'одиннадцать', u'двенадцать', u'тринадцать', u'четырнадцать',
            u'пятнадцать', u'шестнадцать', u'семнадцать', u'восемнадцать', u'девятнадцать')
        self.tens = (
            self.teens, u'двадцать', u'тридцать', u'сорок', u'пятьдесят',
            u'шестьдесят', u'семьдесят', u'восемьдесят', u'девяносто')
        self.hundreds = (
            u'сто', u'двести', u'триста', u'четыреста', u'пятьсот', u'шестьсот', u'семьсот', u'восемьсот', u'девятьсот')
        self.orders = (
            ((u'тысяча', u'тысячи', u'тысяч'), 'f'),
            ((u'миллион', u'миллиона', u'миллионов'), 'm'),
            ((u'миллиард', u'миллиарда', u'миллиардов'), 'm'))
        self.minus = u'минус'

        decimal.getcontext().prec = 10000

    def thousand(self, rest, sex):
        """Converts numbers from 19 to 999"""
        prev, plural = 0, 2
        name = []
        use_teens = rest % 100 >= 10 and rest % 100 <= 19
        if not use_teens:
            data = ((self.units, 10), (self.tens, 100), (self.hundreds, 1000))
        else:
            data = ((self.teens, 10), (self.hundreds, 1000))
        for names, x in data:
            cur = int(((rest - prev) % x) * 10 / x)
            prev = rest % x
            if x == 10 and use_teens:
                plural = 2
                name.append(self.teens[cur])
            elif cur == 0:
                continue
            elif x == 10:
                name_ = names[cur]
                if isinstance(name_, tuple):
                    name_ = name_[0 if sex == 'm' else 1]
                name.append(name_)
                if cur >= 2 and cur <= 4:
                    plural = 1
                elif cur == 1:
                    plural = 0
                else:
                    plural = 2
            else:
                name.append(names[cur-1])
        return plural, name

    def num2text(self, num, main_units=((u'', u'', u''), 'm')):
        """
        http://ru.wikipedia.org/wiki/Gettext#.D0.9C.D0.BD.D0.BE.D0.B6.D0.B5.D1.81.\
        D1.82.D0.B2.D0.B5.D0.BD.D0.BD.D1.8B.D0.B5_.D1.87.D0.B8.D1.81.D0.BB.D0.B0_2
        """
        _orders = (main_units,) + self.orders
        if num == 0:
            return ' '.join((self.units[0], _orders[0][0][2])).strip() # ноль

        rest = abs(num)
        ord = 0
        name = []
        while rest > 0:
            plural, nme = self.thousand(rest % 1000, _orders[ord][1])
            if nme or ord == 0:
                name.append(_orders[ord][0][plural])
            name += nme
            rest = int(rest / 1000)
            ord += 1
        if num < 0:
            name.append(self.minus)
        name.reverse()
        return ' '.join(name).strip()

    def decimal2text(self, value, places=2,
                    int_units=(('', '', ''), 'm'),
                    exp_units=(('', '', ''), 'm')):
        value = decimal.Decimal(value)
        q = decimal.Decimal(10) ** -places

        integral, exp = str(value.quantize(q)).split('.')
        return u'{} {}'.format(
            self.num2text(int(integral), int_units),
            self.num2text(int(exp), exp_units))
