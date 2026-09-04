from django.urls import path
from .import views
from .views import UpdatePostView

urlpatterns = [
#     blogs
    path('', views.home, name="home"),
    path('blogs/', views.blogs, name="blogs"),
    path("blog/<str:slug>/", views.blogs_comments, name="blogs_comments"),
    path("add_blogs/", views.add_blogs, name="add_blogs"),
    path("edit_blog_post/<str:slug>/", UpdatePostView.as_view(), name="edit_blog_post"),
    path("delete_blog_post/<str:slug>/", views.Delete_Blog_Post, name="delete_blog_post"),
    path("search/", views.search, name="search"),
    path("blog/<str:slug>/like/", views.like_blog, name="like_blog"),
    path("category/<str:slug>/", views.category_filter, name="category_filter"),
    path("dashboard/", views.writer_dashboard, name="writer_dashboard"),

#     profile
    path("profile/", views.profile_view, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("user_profile/<int:myid>/", views.user_profile, name="user_profile"),
    
#    user authentication
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
]
