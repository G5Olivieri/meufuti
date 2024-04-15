from django import forms
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View

from court.models import Reservation


class UserRegisterForm(forms.Form):
    first_name = forms.CharField(label="Primeiro nome", widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Sobrenome", widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Usuário", widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password_confirm = forms.CharField(label="Confirmar senha",
                                       widget=forms.PasswordInput(attrs={"class": "form-control"}))
    next = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("As senhas não conferem")

        return cleaned_data


class UserRegisterView(View):
    def get(self, request):
        next_page = request.GET.get("next", "/")
        form = UserRegisterForm()
        form.initial['next'] = next_page
        return render(request, "registration/register.html", context={"form": form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = User(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            next_page = form.cleaned_data.get("next", "/")
            return redirect(next_page)


class UserReservationsView(LoginRequiredMixin, View):
    template_name = 'user/reservations.html'

    def get(self, request: HttpRequest, **kwargs):
        context = {'reservations': Reservation.objects.filter(user=request.user)}
        return render(self.request, self.template_name, context=context)
