from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.exceptions import ValidationError
from .models import *


def Index(request):
    return render(request, 'Index.html')


def Registration(request):
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
            Employee_Details.objects.create(user=user)
            Employee_Experience.objects.create(user=user)
            Employee_Education.objects.create(user=user)
            error = "No"
        except:
            error = "Yes"
    return render(request, 'Registration.html')


def Emp_log(request):
    error1 = ""
    if request.method == 'POST':
        mail = request.POST['mail']
        pwd = request.POST["password"]

        User = get_user_model()
        user = User.objects.filter(email=mail).first()

        if user is not None:
            auth_user = authenticate(request, username=user.username, password=pwd)

            if auth_user is not None:
                login(request, auth_user)
                error1 = "No"
            else:
                error1 = "Yes"
        else:
            error1 = "Yes"
    return render(request, 'Emp_log.html', {'error1': error1})


def Emp_home(request):
    if not request.user.is_authenticated:
        return redirect('Emp_Login')
    return render(request, 'Emp_home.html')


def Profile(request):
    error = ""
    user = request.user
    employee = Employee_Details.objects.filter(user=user).first()

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

    return render(request, 'Profile.html', context)


def Experience(request):
    error = ""
    user = request.user
    experience, created = Employee_Experience.objects.get_or_create(employee=user)

    if request.method == 'POST':
        company = request.POST.get('company', '')
        position = request.POST.get('position', '')
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        description = request.POST.get('description', '')

        if start_date:  # Ensure start_date is not empty
            experience.start_date = start_date
        if end_date:  # Ensure end_date is not empty
            experience.end_date = end_date

        experience.company = company
        experience.position = position
        experience.description = description

        try:
            experience.full_clean()  # Validate the instance
            experience.save()
            # Handle successful save or update
        except ValidationError as e:
            print(e)  # Print validation errors to the console
            error = "Yes"

    context = {
        'experience': experience,
        'error': error
    }

    return render(request, 'Experience.html', context)


def Admin_Login(request):
    return render(request, 'Admin_Login.html')


def Logout(request):
    logout(request)
    return redirect('Index')
