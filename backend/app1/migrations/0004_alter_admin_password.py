# Generated by Django 4.2.7 on 2023-11-30 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_alter_admin_emailid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='password',
            field=models.CharField(),
        ),
    ]
