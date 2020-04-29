from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileCreationForm, complaintForm
from django.views.generic import CreateView
from .models import complaint, Profile
from django.contrib.auth.models import User
from home.models import notification


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        form1 = ProfileCreationForm(request.POST)
        if form.is_valid() and form1.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            user = User.objects.filter(username=username).first()
            profile = Profile(
                StudentID=form1.cleaned_data.get('StudentID'),
                Branch=form1.cleaned_data.get('Branch'),
                YearOfStudy=form1.cleaned_data.get('YearOfStudy'),
                ContactNumber=form1.cleaned_data.get('ContactNumber'),
                user=user
            )
            profile.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
        form1 = ProfileCreationForm()
        context = {
            'form': form,
            'form1': form1,
            'notifications': notification.objects.all()
        }
        return render(request, 'user/register.html', context)


class CreateComplaintView(CreateView):
    model = complaint
    form_class = complaintForm
    template_name = 'user/post_complaint.html'
    success_url = 'complaintSuccess'

    def form_valid(self, form):
        form.instance.complaintUser = Profile.objects.get(user=self.request.user)
        return super(CreateComplaintView, self).form_valid(form)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'notifications': notification.objects.all()
    }

    return render(request, 'user/profile.html', context)
