from django.shortcuts import render, get_object_or_404, redirect  # , redirect, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment, Author, Appointment
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import PostForm, CommentForm
from django_filters import FilterSet
from .filters import PostFilter
from django.core.mail import send_mail
from django.views import View
from datetime import datetime
from django.utils.translation import gettext as _
from django.utils.translation import activate, get_supported_language_variant #LANGUAGE_SESSION_KEY
from django.utils import timezone
from django.shortcuts import redirect
import pytz


class Index(View):
    def get(self, request):
        curent_time = timezone.now()

        # .  Translators: This message appears on the home page only
        models = MyModel.objects.all()

        context = {
            'models': models,
            'current_time': timezone.now(),
            'timezones': pytz.common_timezones
        }

        return HttpResponse(render(request, 'index.html', context))

     #по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')

# добавлено 20.12
class Index(View):
    def get(self, request):
        string = _('Hello world')

        return HttpResponse(string)


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()
        send_mail(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
             #имя клиента и дата записи будут в теме для удобства
            message=appointment.message,  # сообщение с кратким описанием проблемы
            from_email='peterbadson@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=[]  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )
        return redirect('appointments:make_appointment')

def home(request):
    return render(request, 'home.html', {})

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('article-details', args=[str(pk)]))

def DislikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.dislikes.add(request.user)
    return HttpResponseRedirect(reverse('article-details', args=[str(pk)]))


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-post_date']
    paginate_by = 5
    #ordering = ['-id']
# ordering - сортировка. -id показывает, что последний пост находится на самом верху.
# Возможно измнить по дате

def get_queryset(self):
    # Получаем обычный запрос
    queryset = super().get_queryset()
    # Используем наш класс фильтрации.
    # self.request.GET содержит объект QueryDict, который мы рассматривали
    # в этом юните ранее.
    # Сохраняем нашу фильтрацию в объекте класса,
    # чтобы потом добавить в контекст и использовать в шаблоне.
    self.filterset = PostFilter(self.request.GET, queryset)
    # Возвращаем из функции отфильтрованный список товаров
    return self.filterset.qs


def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # Добавляем в контекст объект фильтрации.
    context['filterset'] = self.filterset
    return context


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article-details.html'

    #def get_context_data(self, *args, **kwargs):
     #   #cat_menu = Category.objects.all()
     #   context = super(ArticleDetailView, self).get_context_data()
     #   stuff = get_object_or_404(Post, id=self.kwargs['pk']
     #   total_likes = stuff.total_likes()
     #   #context['cat_menu'] = cat_menu
     #   context["total_likes"] = total_likes
     #   return context


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    #fields = '__all__'

class AddAuthorView(CreateView):
    model = Author
    #form_class = PostForm
    template_name = 'add_author.html'
    fields = '__all__'

class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'
    #fields = '__all__'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('home')

class AddCategoryView(CreateView):
    model = Category
    #form_class = PostForm
    template_name = 'add_category.html'
    fields = '__all__'

class UpdatePostView(UpdateView):
    model = Post
    template_name = 'update_post.html'
    fields = ['title', 'title_tag', 'body']

class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')
