from django.urls import include, path
#from . import views
from .views import HomeView, ArticleDetailView, AddPostView, UpdatePostView, DeletePostView, LikeView, DislikeView, AddCategoryView, AddCommentView, AddAuthorView, AppointmentView

urlpatterns = [
    #path('', views.home, name='home'),
    path('', HomeView.as_view(), name='home'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name = 'article-details'),
    path('add_post/', AddPostView.as_view(), name = 'add_post'),
    path('add_category/', AddCategoryView.as_view(), name = 'add_category.html'),
    path('article/edit<int:pk>', UpdatePostView.as_view(), name = 'update_post'),
    path('article/<int:pk>/remove', DeletePostView.as_view(), name='delete_post'),
    path('like/<int:pk>', LikeView, name='like_post'),
    path('dislike/<int:pk>', DislikeView, name='dislike_post'),
    path('article/<int:pk>/comment/', AddCommentView.as_view(), name = 'add_comment'),
    path('article/<int:pk>/author/', AddAuthorView.as_view(), name = 'add_author.html'),
    path('accounts/', include('allauth.urls')),
    path('appointment/', AppointmentView.as_view(), name='make-appointment'),
]
