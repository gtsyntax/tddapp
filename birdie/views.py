from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import TemplateView, CreateView, UpdateView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail

import stripe
from .models import Post
from .forms import PostForm


class HomeView(TemplateView):
    template_name = 'birdie/home.html'


class AdminView(TemplateView):
    template_name = 'birdie/admin.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AdminView, self).dispatch(request, *args, **kwargs)


class PostCreateView(CreateView):
    template_name = 'birdie/create.html'
    form_class = PostForm


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'birdie/update.html'
    form_class = PostForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        if getattr(request.user, 'first_name', None) == 'Tony':
            raise Http404()
        else:
            return super(PostUpdateView, self).post(request, *args, **kwargs)


class PaymentView(View):
    def post(self, request, *args, **kwargs):
        charge = stripe.Charge.create(
            amount=100,
            currency='try',
            description='',
            token=request.POST.get('token'),
        )
        send_mail(
            'Payment received',
            'Charge {} succeeded!'.format(charge['id']),
            'server@example.com',
            ['admin@example.com']
        )
        return redirect('/')



