"""app URL Configuration

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
from django.urls import path

from .views.requirement import RequirementViewSet
from .views.level import LevelViewSet
from .views.match import MatchViewSet
from .views.player import PlayerViewSet
from .views.consequence import ConsequenceViewSet
from .views.origin import OriginViewSet
from .views.item import ItemViewSet
from .views.event import EventViewSet
from .views.character_class import CharacterClassViewSet
from .views.character import CharacterViewSet
from .views.body import BodyViewSet


urlpatterns = [
    path('requirement', RequirementViewSet.as_view()),
    path('level', LevelViewSet.as_view()),
    path('match', MatchViewSet.as_view()),
    path('player.py', PlayerViewSet.as_view()),
    path('consequence', ConsequenceViewSet.as_view()),
    path('origin', OriginViewSet.as_view()),
    path('item', ItemViewSet.as_view()),
    path('event', EventViewSet.as_view()),
    path('character-class', CharacterClassViewSet.as_view()),
    path('character', CharacterViewSet.as_view()),
    path('body', BodyViewSet.as_view())
]
