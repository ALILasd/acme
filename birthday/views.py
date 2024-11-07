
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from datetime import date
from .forms import BirthdayForm
from .models import Birthday


class BirthdayListView(ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 10


class BirthdayMixin:
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayCreateView(BirthdayMixin, CreateView):
    form_class = BirthdayForm


class BirthdayUpdateView(BirthdayMixin, UpdateView):
    form_class = BirthdayForm


class BirthdayDeleteView(BirthdayMixin, DeleteView):
    pass

class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        return context

def calculate_birthday_countdown(birthday):
    """
    Возвращает количество дней до следующего дня рождения.

    Если день рождения сегодня, то возвращает 0.
    """
    # Сохраняем текущую дату в переменную today.
    today = date.today()
    # Получаем день рождения в этом году
    # с помощью вспомогательной функции (ниже).
    this_year_birthday = get_birthday_for_year(birthday, today.year)

    # Если день рождения уже прошёл...
    if this_year_birthday < today:
        # ...то следующий ДР будет в следующем году.
        next_birthday = get_birthday_for_year(birthday, today.year + 1)
    else:
        # А если в этом году ещё не было ДР, то он и будет следующим.
        next_birthday = this_year_birthday

    # Считаем разницу между следующим днём рождения и сегодняшним днём в днях.
    birthday_countdown = (next_birthday - today).days
    return birthday_countdown


def get_birthday_for_year(birthday, year):
    """
    Получает дату дня рождения для конкретного года.

    Ошибка ValueError возможна только в случае
    с високосными годами и ДР 29 февраля.
    В этом случае приравниваем дату ДР к 1 марта.
    """
    try:
        # Пробуем заменить год в дате рождения на переданный в функцию.
        calculated_birthday = birthday.replace(year=year)
    # Если возникла ошибка, значит, день рождения 29 февраля
    # и подставляемый год не является високосным.
    except ValueError:
        # В этом случае устанавливаем ДР 1 марта.
        calculated_birthday = date(year=year, month=3, day=1)
    return calculated_birthday