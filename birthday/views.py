from django.shortcuts import get_object_or_404, redirect, render
from .forms import BirthdayForm

from datetime import date

from .models import Birthday

from django.core.paginator import Paginator

from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy


#миксин
#class BirthdayMixin:
    #model = Birthday
    #form_class = BirthdayForm
    #template_name = 'birthday/birthday.html'
    #success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context


class BirthdayCreateView(CreateView):
    model = Birthday
    form_class = BirthdayForm

    # Указываем модель, с которой работает CBV...
    #model = Birthday
    # Этот класс сам может создать форму на основе модели!
    # Нет необходимости отдельно создавать форму через ModelForm.
    # Указываем поля, которые должны быть в форме:
    #fields = '__all__'
    #form_class = BirthdayForm

    # Явным образом указываем шаблон:
    #template_name = 'birthday/birthday.html'
    # Указываем namespace:name страницы, куда будет перенаправлен пользователь
    # после создания объекта:
    #success_url = reverse_lazy('birthday:list') 

class BirthdayUpdateView(UpdateView):
    model = Birthday
    form_class = BirthdayForm

class BirthdayDeleteView(DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')
    #model = Birthday
    #template_name = 'birthday/birthday.html'
    #success_url = reverse_lazy('birthday:list') 
    #def delete_birthday(request, pk):
    # Получаем объект модели или выбрасываем 404 ошибку.
    #instance = get_object_or_404(Birthday, pk=pk)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
   # form = BirthdayForm(instance=instance)
    #context = {'form': form}
    # Если был получен POST-запрос...
    #if request.method == 'POST':
        # ...удаляем объект:
        #instance.delete()
        # ...и переадресовываем пользователя на страницу со списком записей.
        #return redirect('birthday:list')
    # Если был получен GET-запрос — отображаем форму.
    #return render(request, 'birthday/birthday.html', context)



class BirthdayListView(ListView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = 'id'
    # ...и даже настройки пагинации:
    paginate_by = 10 

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