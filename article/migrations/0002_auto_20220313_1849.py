# Generated by Django 2.2.13 on 2022-03-13 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlepost',
            options={'ordering': ('-created',), 'verbose_name': '提交文章', 'verbose_name_plural': '提交文章'},
        ),
    ]