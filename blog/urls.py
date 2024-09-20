from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, CommentUpdateView, CommentDeleteView
from . import views #. means current directory

#always end url with a trailing slash, good practice
urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'), #empty as we want it to direct to home page, which is the default page
    #when we use class-based view, we cant just pass it as we passed function view,
    #they need to be conb=verted to an actual view which is done by a method called as_view
    #we have to create a urlpattern that contains a variable, for detail view
    #django makes it so that we can add variables to our actual route
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    #pk means primary key; i.e, post 1 has pk 1 and so on (using variable makes it so that we don't have to make url for each post)
    #specifying that we only want to see int after post, preventing string
    #detail view expects variable to be pk so we're following a convention, if we want to change the name, we have to make sure to mention that in it's class
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    #as create and update share the same form, it expects the dir to be blog/post_form.html
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    #uses the same template the one we used for create view
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_id>/comment-update/<int:pk>/', CommentUpdateView.as_view(template_name = 'blog/comment_update.html'), name='comment-update'),
    path('post/<int:post_id>/comment-delete/<int:pk>/', CommentDeleteView.as_view(template_name = 'blog/comment_confirm_delete.html'), name='comment-delete'),
    path('about/', views.about, name='blog-about'),
]