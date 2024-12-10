# Generated by Django 5.1.4 on 2024-12-10 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='language',
            field=models.CharField(choices=[('py', 'python'), ('js', 'javascript'), ('C', 'cprogramming'), ('C++', 'c++')], default='python', max_length=100),
        ),
    ]