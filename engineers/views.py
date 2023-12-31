from django.contrib.auth.views import LoginView
# from django.forms.models import BaseModelForm
# from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.paginator import Paginator
from django.contrib.auth import logout, login

from .forms import *
from .models import *
from .utils import *


class EngineersHome(DataMixin, ListView):
    model = Engineers
    template_name = "engineers/index.html"
    context_object_name = "posts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Engineers.objects.filter(is_published=True).select_related("cat")


# def index(request):
#     posts = Engineers.objects.all()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#
#     return render(request, 'engineers/index.html', context=context)


# @login_required #Декоратор для выведение ошибки 404 неавторизов. польз.
def about(request):
    # contact_list = Engineers.objects.all()
    # paginator = Paginator(contact_list, 3)

    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)
    return render(
        request,
        "engineers/about.html",
        {"menu": [{"title": "О сайте", "url_name": "about"}, {"title": "Обратная связь", "url_name": "contact"},], "title": "О сайте"},)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "engineers/addpage.html"
    success_url = reverse_lazy("home")
    login_url = "/admin/"
    raise_exception = True  # Генерируем ошибку 403 для не разрег пользователей

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'engineers/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


# def contact(request):
#     return HttpResponse("Обратная связь")


class ContactFormView(DataMixin, FormView):
    form_class = (
        ContactForm  # Своя форма   # UserCreationForm  -  джанговская стандартная форма
    )
    template_name = "engineers/contact.html"  # ссылка на шаблон
    success_url = reverse_lazy("home")  # при успешной регистр. пользов.

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect("home")


# def login(request):
#     return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


# def show_post(request, post_slug):
#     post = get_object_or_404(Engineers, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'engineers/post.html', context=context)


class ShowPost(DataMixin, DetailView):
    model = Engineers
    template_name = "engineers/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context["post"])
        return dict(list(context.items()) + list(c_def.items()))


class EngineersCategory(DataMixin, ListView):
    model = Engineers
    template_name = "engineers/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Engineers.objects.filter(
            cat__slug=self.kwargs["cat_slug"], is_published=True
        ).select_related("cat")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs["cat_slug"])
        c_def = self.get_user_context(
            title="Категория - " + str(c.name),
            cat_selected=c.pk,
        )
        return dict(list(context.items()) + list(c_def.items()))


# def show_category(request, cat_id):
#     posts = Engineers.objects.filter(cat_id=cat_id)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_id,
#     }
#
#     return render(request, 'engineers/index.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm  # Своя форма   # UserCreationForm  -  джанговская стандартная форма
    template_name = "engineers/register.html"  # ссылка на шаблон
    success_url = reverse_lazy("login")  # при успешной регистр. пользов.

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = "engineers/login.html"  # ссылка на шаблон

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy("home")


def logout_user(request):
    logout(request)
    return redirect("login")
