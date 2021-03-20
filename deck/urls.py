from django.urls import path
from . import views

urlpatterns = [
    path('', views.DeckListView.as_view(), name='deck_list'),
    path('deck/<int:pk>/', views.DeckDetailView.as_view(), name='deck_detail'),
    path('deck/new/', views.DeckNewView.as_view(), name="deck_new"),
    path('card_list/', views.CardListView.as_view(), name='card_list'),
    path('card/<int:pk>/', views.CardDetailView.as_view(), name='card_detail'),
    path('like/', views.LikeView, name='like'),

    path('deck_order_by/', views.DeckOrderByView, name='deck_order_by'),

    path('num_change/', views.NumChangeView, name='num_change'),

    path('num_reset/', views.NumReset, name='num_reset'),
    path('narrowing/', views.Narrowing, name='narrowing'),
    path('deck_narrowing/', views.deck_narrowing, name='deck_narrowing'),

    path('userpage/', views.MypageView.as_view(), name='mypage'),
    ]