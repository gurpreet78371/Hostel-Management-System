from django.shortcuts import render, redirect
from django.contrib import messages
from .models import notification, hostelApplication, messFee, FeeQuery
from user.models import complaint
from .forms import notification as noti_form
from .forms import hostelapplication, messFeeForm, FeeQueryForm
from django.core.files.storage import FileSystemStorage
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django import forms


def home(request):
    context = {
        'notifications': notification.objects.all()
    }
    return render(request, 'home/index1.html', context)


def about(request):
    return render(request, 'home/about.html')


def fee(request):
    fees = {
        'fee_list': messFee.objects.all()
    }
    return render(request, 'home/FeeQuerySelector.html', fees)


class updateFeeView(CreateView):
    model = messFee
    form_class = messFeeForm
    template_name = 'home/updateFee.html'
    success_url = 'users'


def noti(request, id=None):
    content = {'content': notification.objects.get(id=id)}
    return render(request, 'home/shownoti.html', content)


def noti_upload(request):
    if request.method == 'POST' and request.FILES.get('myfile', False):
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'home/noti_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'home/noti_upload.html')


def upload(request):
    if request.method == 'POST':
        form = noti_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Announcement has been posted.')
            return redirect('users')
    else:
        form = noti_form()
    return render(request, 'home/upload_noti.html', {
        'form': form
    })


def success(request):
    return render(request, 'home/success.html')


class CreateMyModelView(CreateView):
    model = hostelApplication
    form_class = hostelapplication
    template_name = 'home/apply.html'
    success_url = 'success'


def CreateFeeQueryView(request):
    if request.method == 'POST':
        form = FeeQueryForm(request.POST)
        if form.is_valid():
            SID = form.cleaned_data.get('SID')
            month = form.cleaned_data.get('month')
            hostelName = form.cleaned_data.get('hostelName')
            # if not SID or not (month and hostelName):
            #     raise forms.ValidationError('You have to write something!')
            print(SID)
            print(month)
            print(hostelName)
            if SID != None:
                content = {'fee_list': messFee.objects.all()}
                return render(request, 'home/fee_details.html', content)
            elif (month != None and hostelName != None):
                content = {'fee_list': messFee.objects.filter(month=month, hostelName=hostelName)}
                return render(request, 'home/fee_details.html', content)
            else:
                form = FeeQueryForm()
                return render(request, 'home/FeeQuerySelector.html', {
                    'form': form
                })
            return render(request, 'home/fee_details.html')
    else:
        form = FeeQueryForm()
        return render(request, 'home/FeeQuerySelector.html', {
            'form': form
        })


@login_required
def users(request):
    if request.user.is_staff or request.user.is_superuser:
        context = dict(complaints=complaint.objects.all(), applications=hostelApplication.objects.all())
        return render(request, 'home/admin_view.html', context)
    else:
        content = dict(notifications=notification.objects.all())
        return render(request, 'home/user_view.html', content)
