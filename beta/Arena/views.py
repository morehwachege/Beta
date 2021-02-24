from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'index.html'


class SigninView(TemplateView):
    template_name = 'signin.html'
