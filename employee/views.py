from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render
from django.core.exceptions import ValidationError
from .models import *


def index(request):
    return render(request, 'index.html')


def registration(request):
    error = ""
    if request.method == "POST":
        fn = request.POST['first_name']
        ln = request.POST['last_name']
        sc = request.POST['sccode']
        em = request.POST['mail']
        pwd = request.POST['password']

        if not sc:
            username = (fn.lower() + ln.lower()).replace(" ", "")  # Generate username without spaces
        else:
            username = sc

        try:
            User = get_user_model()
            user = User.objects.create_user(first_name=fn, last_name=ln, username=username, password=pwd, email=em)
            EmployeeDetails.objects.create(user=user)
            EmployeeExperience.objects.create(user=user)
            EmployeeEducation.objects.create(user=user)
            error = "No"
        except:
            error = "Yes"
    return render(request, 'registration.html')


def emp_log(request):
    error1 = ""
    if request.method == 'POST':
        mail = request.POST['mail']
        pwd = request.POST["password"]

        user_model = get_user_model()
        user = user_model.objects.filter(email=mail).first()

        if user is not None:
            auth_user = authenticate(request, username=user.username, password=pwd)

            if auth_user is not None:
                login(request, auth_user)
                error1 = "No"
            else:
                error1 = "Yes"
        else:
            error1 = "Yes"
    return render(request, 'emp_log.html', {'error1': error1})


def emp_home(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    return render(request, 'emp_home.html')


def profile(request):
    error = ""
    user = request.user
    employee = EmployeeDetails.objects.filter(user=user).first()

    if request.method == "POST":
        fn = request.POST.get('first_name', '')
        ln = request.POST.get('last_name', '')
        sc = request.POST.get('sccode', '')
        dep = request.POST.get('empdep', '')
        fct = request.POST.get('function', '')
        con = request.POST.get('contact', '')
        jd = request.POST.get('joindate', '')
        gd = request.POST.get('gender', None)

        user.first_name = fn
        user.last_name = ln
        user.username = sc or (fn.lower() + ln.lower())  # Set username as sccode or combination of first and last name
        employee.empdep = dep
        employee.function = fct
        employee.contact = con
        employee.joindate = jd
        employee.gender = gd

        try:
            user.save()
            employee.save()
            # Handle successful save or update
        except:
            error = "Yes"

    context = {
        'employee': employee,
        'error': error
    }

    return render(request, 'profile.html', context)


def experience(request):
    error = ""
    user = request.user
    experience_, created = EmployeeExperience.objects.get_or_create(employee=user)

    if request.method == 'POST':
        company = request.POST.get('company', '')
        position = request.POST.get('position', '')
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        description = request.POST.get('description', '')

        if start_date:  # Ensure start_date is not empty
            experience_.start_date = start_date
        if end_date:  # Ensure end_date is not empty
            experience_.end_date = end_date

        experience_.company = company
        experience_.position = position
        experience_.description = description

        try:
            experience_.full_clean()  # Validate the instance
            experience_.save()
            # Handle successful save or update
        except ValidationError as e:
            print(e)  # Print validation errors to the console
            error = "Yes"

    context = {
        'experience': experience_,
        'error': error
    }

    return render(request, 'experience.html', context)


def admin_login(request):
    return render(request, 'admin_login.html')


def log_out(request):
    logout(request)
    return redirect('index')
