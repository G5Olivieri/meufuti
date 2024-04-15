import logging

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from court.models import Court, CourtImage, Reservation

logger = logging.getLogger(__name__)


class CourtsView(View):
    template_name = "court/index.html"

    def get(self, request: HttpRequest, **kwargs):
        q = request.GET.get('q', None)
        if q is None:
            courts = Court.objects.all()
        else:
            courts = Court.objects.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(street__icontains=q) |
                Q(neighborhood__icontains=q) |
                Q(city__icontains=q) |
                Q(state__icontains=q) |
                Q(facilities__in=q) |
                Q(availability_weeks__in=q)
            )

        context = {'courts': courts}
        return render(request, self.template_name, context)


class CourtByIdView(TemplateView):
    template_name = "court/court.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['court'] = Court.objects.get(id=kwargs['id'])
        return context


class CourtCreateForm(forms.ModelForm):
    image = forms.ImageField(label="Imagem", widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Court
        fields = ['name', 'description', 'zip_code', 'street', 'number', 'neighborhood', 'city', 'state', 'facilities',
                  'availability_weeks', 'availability_times', 'single_price', 'monthly_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'neighborhood': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'facilities': forms.TextInput(attrs={'class': 'form-control'}),
            'availability_weeks': forms.TextInput(attrs={'class': 'form-control'}),
            'availability_times': forms.TextInput(attrs={'class': 'form-control'}),
            'single_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'monthly_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CourtCreateView(LoginRequiredMixin, View):
    login_url = "/accounts/login/"
    redirect_field_name = "next"
    template_name = "court/create.html"

    def get(self, request: HttpRequest, **kwargs):
        context = {}
        context['form'] = CourtCreateForm()
        return render(request, self.template_name, context=context)

    def post(self, request: HttpRequest):
        form = CourtUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            court = Court(
                owner=request.user,
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                zip_code=form.cleaned_data['zip_code'],
                street=form.cleaned_data['street'],
                number=form.cleaned_data['number'],
                neighborhood=form.cleaned_data['neighborhood'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                facilities=form.cleaned_data['facilities'],
                availability_weeks=form.cleaned_data['availability_weeks'],
                availability_times=form.cleaned_data['availability_times'],
                single_price=form.cleaned_data['single_price'],
                monthly_price=form.cleaned_data['monthly_price']
            )
            court.save()
            if form.cleaned_data['image']:
                court_image = CourtImage(court=court, image=form.cleaned_data['image'])
                court_image.save()
            return redirect('court.get_by_id', id=court.id)


class CourtUpdateForm(forms.ModelForm):
    image = forms.ImageField(label="Imagem", widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Court
        fields = ['name', 'description', 'zip_code', 'street', 'number', 'neighborhood', 'city', 'state',
                  'facilities',
                  'availability_weeks', 'availability_times', 'single_price', 'monthly_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'neighborhood': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'facilities': forms.TextInput(attrs={'class': 'form-control'}),
            'availability_weeks': forms.TextInput(attrs={'class': 'form-control'}),
            'availability_times': forms.TextInput(attrs={'class': 'form-control'}),
            'single_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'monthly_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CourtUpdateView(LoginRequiredMixin, View):
    login_url = "/accounts/login/"
    redirect_field_name = "next"
    template_name = "court/update.html"

    def get(self, request: HttpRequest, **kwargs):
        court = Court.objects.get(id=kwargs['id'])
        if request.user.id == court.owner_id:
            context = {}
            form = CourtUpdateForm(instance=court)
            court_image = CourtImage.objects.filter(court=court).first()
            if court_image is not None:
                form.fields['image'].initial = court_image.image
            context['form'] = form
            context['court'] = court
            return render(request, self.template_name, context=context)
        raise PermissionError("You are not the owner of this court")

    def post(self, request: HttpRequest, **kwargs):
        court = Court.objects.filter(id=kwargs['id'])[0]
        if request.user.id == court.owner_id:
            form = CourtUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                court.name = form.cleaned_data['name']
                court.description = form.cleaned_data['description']
                court.zip_code = form.cleaned_data['zip_code']
                court.street = form.cleaned_data['street']
                court.number = form.cleaned_data['number']
                court.neighborhood = form.cleaned_data['neighborhood']
                court.city = form.cleaned_data['city']
                court.state = form.cleaned_data['state']
                court.facilities = form.cleaned_data['facilities']
                court.availability_weeks = form.cleaned_data['availability_weeks']
                court.availability_times = form.cleaned_data['availability_times']
                court.single_price = form.cleaned_data['single_price']
                court.monthly_price = form.cleaned_data['monthly_price']
                court.save()
                if form.cleaned_data['image'] is not None:
                    court_image = CourtImage.objects.filter(court=court).first()
                    if court_image is None:
                        court_image = CourtImage(court=court, image=form.cleaned_data['image'])
                    else:
                        court_image.image = form.cleaned_data['image']
                    court_image.save()
                return redirect('court.get_by_id', id=court.id)
            else:
                return render(request, self.template_name, context={'form': form, 'court': court})

        raise PermissionError("You are not the owner of this court")


class CourtDeleteView(LoginRequiredMixin, View):
    login_url = "/accounts/login/"
    redirect_field_name = "next"
    template_name = "court/update.html"

    def post(self, request: HttpRequest, **kwargs):
        court = Court.objects.get(id=kwargs['id'])
        if request.user.id == court.owner_id:
            court.delete()
            return redirect('court.index')
        raise PermissionError("You are not the owner of this court")


class CourtReserveForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'time', 'duration']


class CourtReserveView(LoginRequiredMixin, View):
    login_url = "/accounts/login/"
    redirect_field_name = "next"
    template_name = "court/reserve.html"

    def get(self, request: HttpRequest, **kwargs):
        court = Court.objects.get(id=kwargs['id'])
        context = {'court': court, 'form': CourtReserveForm()}
        return render(request, self.template_name, context=context)

    def post(self, request: HttpRequest, **kwargs):
        court = Court.objects.get(id=kwargs['id'])
        form = CourtReserveForm(request.POST)
        if form.is_valid():
            reservation = Reservation(
                court=court,
                user=request.user,
                date=form.cleaned_data['date'],
                time=form.cleaned_data['time'],
                duration=form.cleaned_data['duration'] * 3600
            )
            reservation.save()
            return redirect('court.get_by_id', id=court.id)
        else:
            return render(request, self.template_name, context={'form': form, 'court': court})


class CourtReservationsView(TemplateView):
    template_name = "court/reservations.html"

    def get_context_data(self, **kwargs):
        court = Court.objects.get(id=kwargs['id'])
        if court.owner_id != self.request.user.id:
            raise PermissionError("You are not the owner of this court")
        context = super().get_context_data(**kwargs)
        context['court'] = court
        context['reservations'] = Reservation.objects.filter(court=court)
        return context


class CourtMyView(LoginRequiredMixin, TemplateView):
    template_name = "court/my.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courts'] = Court.objects.filter(owner=self.request.user)
        return context
