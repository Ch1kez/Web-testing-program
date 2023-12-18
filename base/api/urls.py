from django.urls import path

from .views import (
    MailListCreateView, MailDetailView,
    TargetListCreateView, TargetDetailView,
    TestListCreateView, TestDetailView,
    TuserListCreateView, TuserDetailView,
    WebsiteTableListCreateView, WebsiteTableDetailView,
    api_home, api_tables, custom_response
)

urlpatterns = [
    path('', api_home, name='home'),

    path('custom-response/', custom_response, name='custom-response'),

    path('api/', api_tables, name='api-home'),

    path('api/mails/', MailListCreateView.as_view(), name='mail-list'),
    path('api/mails/<int:pk>/', MailDetailView.as_view(), name='mail-detail'),

    path('api/targets/', TargetListCreateView.as_view(), name='targets-list'),
    path('api/targets/<int:pk>/', TargetDetailView.as_view(), name='targets-detail'),

    path('api/tests/', TestListCreateView.as_view(), name='test-list'),
    path('api/tests/<int:pk>/', TestDetailView.as_view(), name='test-detail'),

    path('api/tusers/', TuserListCreateView.as_view(), name='tuser-list'),
    path('api/tusers/<int:pk>/', TuserDetailView.as_view(), name='tuser-detail'),

    path('api/website-tables/', WebsiteTableListCreateView.as_view(), name='website-table-list'),
    path('api/website-tables/<int:pk>/', WebsiteTableDetailView.as_view(), name='website-table-detail'),
]
