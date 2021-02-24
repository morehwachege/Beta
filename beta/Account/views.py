from django.shortcuts import render
from django.views.generic import TemplateView


class SigninView(TemplateView):
    template_name = 'signin.html'
