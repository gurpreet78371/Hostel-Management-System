from django.shortcuts import render, redirect
from django.contrib import messages
from .models import notification, hostelApplication, messFee, FeeQuery
from user.models import complaint, Profile
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


def payment(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'fee_list': messFee.objects.filter(User=profile)
    }
    print(profile)
    print(context)
    return render(request, 'home/payment.html', context)


def about(request):
    return render(request, 'home/about.html')


def fee(request):
    fees = {
        'fee_list': messFee.objects.all()
    }
    return render(request, 'home/FeeQuerySelector.html', fees)


def updateFeeView(request):

    fees = messFee.objects.all()
    forms = list()

    if request.method == 'POST':
        keys = []
        length = 0
        for key in request.POST.keys():
            keys.append(key)
            length = len(request.POST[key])
        length = length - 1
        for index in range(length):
            dict_messForm = {}
            for key in keys:
                l = list(request.POST.getlist(key))
                value = l[index]
                dict_messForm.update({key:value})
            forms.append(messFeeForm(dict_messForm))

        flag = True
        for form in forms:
            if not form.is_valid():
                flag = False
                break
        if flag:
            for form in forms:
                a = messFee.objects.get(User=form.cleaned_data.get('User'))
                a.month = form.cleaned_data.get('month')
                a.regularFee = form.cleaned_data.get('regularFee')
                rf = form.cleaned_data.get('regularFee')
                a.extraFee = form.cleaned_data.get('extraFee')
                ef = form.cleaned_data.get('extraFee')
                a.discount = form.cleaned_data.get('discount')
                dis = form.cleaned_data.get('discount')
                a.Total = int(rf) + int(ef) - int(dis)
                a.save()
            messages.success(request, f'Fee has been updated ')
            return redirect('users')
    else:
        for fee in fees:
            user = fee.User
            month = fee.month
            regular = fee.regularFee
            extra = fee.extraFee
            discount = fee.discount
            total = fee.Total
            forms.append(messFeeForm(initial={
                'User': user,
                'month': month,
                'regularFee': regular,
                'extraFee': extra,
                'discount': discount,
                'Total': total
            }))
        return render(request, 'home/updateFee.html', {
            'forms': forms
        })


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
    flag = False
    if request.method == 'POST':
        form = FeeQueryForm(request.POST)
        if form.is_valid():
            SID = form.cleaned_data.get('SID')
            month = form.cleaned_data.get('month')
            hostelName = form.cleaned_data.get('hostelName')
            if not SID and not (month and hostelName) and flag:
                messages.warning(request, f'You have to fill correct details')
                form = FeeQueryForm()
                return render(request, 'home/FeeQuerySelector.html', {
                    'form': form
                })
            else:
                if SID:
                    profile = Profile.objects.get(StudentID=SID)
                    content = {'fee_list': messFee.objects.filter(User=profile)}
                    return render(request, 'home/fee_details.html', content)
                elif (month and hostelName):
                    content = {'fee_list': messFee.objects.filter(month=month, hostelName=hostelName)}
                    return render(request, 'home/fee_details.html', content)
                else:
                    form = FeeQueryForm()
                    return render(request, 'home/FeeQuerySelector.html', {
                        'form': form
                    })
                return render(request, 'home/fee_details.html')
            flag = True
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
        return render(request, 'home/index1.html', content)
