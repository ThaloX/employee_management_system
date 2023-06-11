from datetime import datetime
import logging

from django.contrib.auth import logout
from django.db import OperationalError, IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware

from .models import *


def view_index(request):
    return render(request, 'index.html')


def view_registration(request):
    if request.method == "GET":
        return render(request, 'registration.html')

    if request.method == "POST":
        fn = request.POST.get('first_name')
        ln = request.POST.get('last_name')
        sc = request.POST.get('subcontractor_code')
        em = request.POST.get('mail')
        pwd = request.POST.get('password')

        if not sc:
            username = (fn.lower() + ln.lower()).replace(" ", "")  # Generate username without spaces
        else:
            username = sc

        try:
            user_model = get_user_model()
            user = user_model.objects.create_user(first_name=fn, last_name=ln, username=username, password=pwd,
                                                  email=em)
            # EmployeeDetails.objects.create(user=user)
            # EmployeeExperience.objects.create(employee=user)
            # EmployeeEducation.objects.create(employee=user)
            error = "No"
            cause = ""

        except IntegrityError as ex:
            logging.error(ex)
            cause = ex.args[0].split('.')[1]
            error = "Yes"

        except OperationalError as ex:
            logging.error(ex)
            cause = ex.args[0]
            error = "Yes"

        except Exception as ex:
            logging.error(ex)
            cause = ex
            error = "Yes"

        context = {
            'error': error,
            'cause': cause,
        }

        return render(request, 'registration.html', context)


def view_login(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
        pwd = request.POST.get('password')

        user_model = get_user_model()
        user = user_model.objects.filter(email=mail).first()

        context = {}

        if user is None:
            context['error'] = "Yes"
        else:
            auth_user = authenticate(request, username=user.username, password=pwd)

            if auth_user is not None:
                login(request, auth_user)
                context['error'] = "No"
            else:
                context['error'] = "Yes"

        return render(request, 'emp_log.html', context)

    return render(request, 'emp_log.html')


def view_homepage(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    return render(request, 'emp_home.html')


def view_profile(request):
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
        except Exception as ex:
            logging.error(ex)
            error = "Yes"

    context = {
        'employee': employee,
        'error': error
    }

    return render(request, 'profile.html', context)


def view_experience(request):
    user = request.user
    error = "No"

    if request.method == 'POST':
        company = request.POST.get('company', '')
        position = request.POST.get('position', '')
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        description = request.POST.get('description', '')

        if start_date:  # Ensure start_date is not empty
            start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
        if end_date:  # Ensure end_date is not empty
            end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d'))

        try:
            experience = EmployeeExperience.objects.create(
                employee=user,
                company=company,
                position=position,
                start_date=start_date,
                end_date=end_date,
                description=description
            )
            # Handle successful insertion
        except IntegrityError as ex:
            logging.error(ex)  # Print integrity error to the console
            error = "Yes"

    elif request.method == 'GET':
        # Retrieve all existing entries for the user
        experiences = EmployeeExperience.objects.filter(employee=user)

        # Serialize the experiences into a list of dictionaries
        serialized_experiences = []

        for experience in experiences:
            serialized_experiences.append({
                'id': experience.id,
                'company': experience.company,
                'position': experience.position,
                'start_date': experience.start_date,
                'end_date': experience.end_date,
                'description': experience.description,
            })

        context = {
            'experiences': serialized_experiences
        }

        return render(request, 'experience.html', context)

    context = {
        'experience': experience,
        'error': error
    }

    return render(request, 'experience.html', context)


def view_education(request):
    user = request.user
    education, created = EmployeeEducation.objects.get_or_create(employee=user)

    error = "No"

    if request.method == 'POST':
        company = request.POST.get('company', '')
        position = request.POST.get('position', '')
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        description = request.POST.get('description', '')

        if start_date:  # Ensure start_date is not empty
            education.start_date = start_date
        if end_date:  # Ensure end_date is not empty
            education.end_date = end_date

        education.company = company
        education.position = position
        education.description = description

        try:
            education.full_clean()  # Validate the instance
            education.save()
            # Handle successful save or update
        except ValidationError as ex:
            logging.error(ex)  # Print validation errors to the console
            error = "Yes"

    context = {
        'education': education,
        'error': error
    }

    return render(request, 'education.html', context)


def view_remove_experience(request):
    if request.method == 'POST':
        row_id = request.POST.get('row_id')

        try:
            experience = EmployeeExperience.objects.get(id=row_id)
            experience.delete()
        except EmployeeEducation.DoesNotExist:
            pass

    return redirect('experience')



def view_admin_login(request):
    return render(request, 'admin_login.html')


def view_logout(request):
    logout(request)
    return redirect('index')
