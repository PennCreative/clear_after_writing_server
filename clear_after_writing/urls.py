"""clear_after_writing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from cawapi.views import register_user, check_user
from cawapi.views import UserView, JournalView, SurveyView, StatView, todaysJournalView, WriterJournalView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserView, 'user')
router.register(r'journals', JournalView, 'journal')
router.register(r'surveys', SurveyView, 'survey')
router.register(r'stats', StatView, 'stat')
router.register(r'writer-journals', WriterJournalView, 'writer-journal')


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('checkuser', check_user),
    path('today', todaysJournalView.as_view(), name='today-journals'),
    path('<str:date>', todaysJournalView.as_view(), name='journals-by-date'),
    path('journals/writer/', WriterJournalView.as_view({'get': 'list_by_writer_id'}), name='writer-journals'),
    path('surveys/', StatView.as_view({'get': 'list'}), name='surveys-by-journal-id'),
    path('surveys/<int:id>', SurveyView.as_view({'get': 'retrieve'}), name='survey-detail'),
]
