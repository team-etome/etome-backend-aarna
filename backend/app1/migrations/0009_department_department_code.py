# Generated by Django 4.2.1 on 2023-12-14 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_department_department_head_subject_subject_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='department_code',
            field=models.CharField(null=True),
        ),
    ]
