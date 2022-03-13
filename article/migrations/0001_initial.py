# Generated by Django 2.2.13 on 2022-03-11 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='標題')),
                ('body', models.TextField(verbose_name='內文')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='創建時間')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
