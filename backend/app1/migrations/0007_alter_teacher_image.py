# Generated by Django 4.2.1 on 2023-12-11 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_teacher_acoe_teacher_email_teacher_empid_teacher_hod_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='teacher'),
        ),
    ]