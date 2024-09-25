# Generated by Django 4.2.4 on 2023-09-02 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SMSApp', '0032_service_is_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='Approvals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approved', models.BooleanField(default=False)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SMSApp.service')),
            ],
        ),
    ]
