# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    # The home page
    path('', views.index, name='home'),

    # LCA API endpoints
    path('lca-api/api-call/', views.lca_api_call, name='lca_api_call'),
    path('lca-api/test/', views.lca_api_test, name='lca_api_test'),

    # Additional endpoints
    path('lca-data-management/', views.lca_data_management, name='lca_data_management'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]
