# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf.urls import  url
from django.contrib import admin
from django.urls import path, include  # add this
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import include, path
from rest_framework import routers
from forecast import views

router = routers.DefaultRouter()
router.register(r'measurements', views.MeasurementsViewSet)
router.register(r'forecast_models', views.ForecastModelsViewSet)
router.register(r'forecasts', views.ForecastsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("authentication.urls")),  # add this
    path("", include("app.urls")),  # add this
    path('', include(router.urls)),
    url(r'^train_models/', views.TrainModels.as_view()),
    url(r'^update_models/', views.UpdateModels.as_view()),
    url(r'^forecast_energy/', views.ForecastEnergy.as_view()),
    url(r'^query/', views.ESQueryView.as_view()),    
    url(r'^forecast_evaluation/', views.ForecastEvaluation.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	path('dash/', views.dashboard_home, name="dashboard"),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('query_form/', views.query_form_process, name='query_form')] 
    