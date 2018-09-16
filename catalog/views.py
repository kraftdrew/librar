from django.shortcuts import render

# Create your views here.

from .models import Book, Author, BookInstance, Genre


def index(request):
    """

    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # Метод 'all()' применен по умолчанию
    # shoppingcartuser= ShoppingCart.objects.get(user= request.user)
    # books_with_filter_all = Book.objects.filter(genre__book__genre__exact='Startup').count()
    # books_with_filter = books_with_filter_all.count()

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available,
                 'num_authors': num_authors, 'num_visits': num_visits}
    )


from django.views import generic


class BookListView(generic.ListView):  # автоматическое имя для дот-нотации - book_list
    model = Book
    # context_object_name = 'my_book_list'  # ваше собственное имя переменной контекста в шаблоне
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Определение имени вашего шаблона и его расположения
    paginate_by = 2


class BookDetailView(generic.DetailView):
    model = Book


# context_object_name = 'knigi'  # эта переменная передаеться в ХТМЛ файл ""дот-нотация"" /  в даном случае book_detail
#   template_name = 'book_wdetail.html'

class AuthorListView(generic.ListView):  # мемод ищет шаблон с таким же назвиие чтобы передать дума модель
    # template_name = 'catalog/spisak.html' # если не совпадают названия метода и шаблона то нужно указать путь
    model = Author
    paginate_by = 2


class AuthorDetailView(generic.DetailView):
    model = Author


#  template_name = 'catalog/detali.html'

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LeanListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.all_lean'

    def get_queryset(self):
        return BookInstance.objects.all().filter(status__exact='o').order_by('due_back')

    template_name = 'catalog/lean_list.html'
    # Or multiple permissions


#   {% if perms.catalog.all_lean %}


from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm, RenewBookModelForm


@permission_required('catalog.all_lean')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'renewal_date': proposed_renewal_date, })

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


# render : передает 'form' и bookinst' в обект контекста в шаблоне

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    permission_required = 'catalog.author_create'
    fields = '__all__'
    initial = {'date_of_death': '12/10/2016', }


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.author_create'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    permission_required = 'catalog.author_create'
    success_url = reverse_lazy('authors')

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    permission_required = 'catalog.author_create'
    fields = '__all__'
    initial = {'date_of_death': '12/10/2016', }


class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.author_create'
    model = Book
    fields = '__all__'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = 'catalog.author_create'
    success_url = reverse_lazy('authors')