# Generated by Django 4.2.1 on 2023-05-17 22:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Employee', '0004_employeeexperience_delete_employeeeducation'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EmployeeExperience',
            new_name='Employee_Experience',
        ),
        migrations.CreateModel(
            name='Employee_Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(max_length=100)),
                ('institution', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('description', models.TextField(blank=True)),
                ('certificates', models.FileField(blank=True, null=True, upload_to='certificates/')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]