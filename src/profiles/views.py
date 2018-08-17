from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, CreateView, DetailView

from .forms import RegisterForm
from .models import Profile
from menus.models import Item
from restaurants.models import RestaurantLocation

User = get_user_model()


def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        profile = get_object_or_404(Profile, activation_key=code)

        if not profile.activated:
            profile.activated = True
            profile.activation_key = None

            user_ = profile.user
            user_.is_active = True

            user_.save()
            profile.save()

            return redirect("/login/")

    return redirect("/login/")


class LogInView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect('/')
        return super(LogInView, self).dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super(RegisterView, self).get_form_kwargs()
        kwargs['url'] = self.request.build_absolute_uri(reverse('activate', kwargs={'code': 'e'}))

        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect('/')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)


class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwgars):
        username_to_toggle = request.POST.get('username')
        profile_, _ = Profile.objects.toogle_follow(request.user, username_to_toggle)

        return redirect(f"/u/{profile_.user.username}/")


class ProfileDetailView(DetailView):
    template_name = 'profiles/user.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')

        if not username:
            raise Http404()

        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data()

        user = context['user']  # Already in the context.
        query = self.request.GET.get('q')

        if user.profile in self.request.user.is_following.all():
            context['is_following'] = True
        else:
            context['is_following'] = False

        item_exists = Item.objects.filter(user=user).exists()
        qs = RestaurantLocation.objects.filter(owner=user).search(query)

        if qs.exists and item_exists:
            context['locations'] = qs

        return context
