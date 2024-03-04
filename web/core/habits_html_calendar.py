from django.utils.timezone import get_current_timezone
from calendar import HTMLCalendar
import datetime


class HabitsHTMLCalendar(HTMLCalendar):
    def __init__(self, start, end):
        super().__init__()
        self.start_date = start
        self.end_date = end

    def formatday(self, day, weekday):
        """
        Return a day as a table cell.
        """
        if day == 0:
            # day outside month
            return '<td class="noday">&nbsp;</td>'
        else:
            date = datetime.date(self.year, self.month, day)
            if self.start_date <= date <= self.end_date:
                return '<td class="table-success">{}</td>'.format(day)
            else:
                return '<td>{}</td>'.format(day)

    def formatmonth(self, year, month, withyear=True):
        """
        Return a formatted month as a table.
        """
        self.year, self.month = year, month
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="table">')
        a('\n')
        a(self.formatmonthname(year, month, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(year, month):
            a(self.formatweek(week))
        a('</table>')
        return ''.join(v)
