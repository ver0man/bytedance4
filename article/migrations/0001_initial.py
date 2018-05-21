# Generated by Django 2.0.5 on 2018-05-19 23:02

import article.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('mobile', models.CharField(blank=True, max_length=30)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('headshot', models.ImageField(blank=True, default='default_headshot.jpg', upload_to=article.models.get_user_profile_path)),
                ('time_registered', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, verbose_name='title')),
                ('body', models.TextField(verbose_name='body')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='time created')),
                ('last_modified_time', models.DateTimeField(auto_now=True, verbose_name='time last modified')),
                ('status', models.CharField(choices=[('d', 'Draft'), ('o', 'Obsolete'), ('p', 'Published')], default='d', max_length=1, verbose_name='status')),
                ('abstract', models.CharField(blank=True, help_text='Optional, default to first 100 characters', max_length=100, null=True, verbose_name='abstract')),
                ('views', models.IntegerField(default=0, verbose_name='views')),
                ('likes', models.IntegerField(default=0, verbose_name='likes')),
                ('shares', models.IntegerField(default=0, verbose_name='Shares')),
            ],
            options={
                'ordering': ['-last_modified_time'],
            },
        ),
        migrations.CreateModel(
            name='ArticleLiked',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Article')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleStored',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='time created')),
                ('last_modified_time', models.DateTimeField(auto_now=True, verbose_name='time last modified')),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(upload_to=article.models.get_user_image_path)),
            ],
        ),
        migrations.CreateModel(
            name='Labels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('articles', models.ManyToManyField(to='article.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.TextField(blank=True)),
                ('baseProfile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileFollowers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='article.Profile')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Stocks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='StocksWatchers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='images',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Profile'),
        ),
        migrations.AddField(
            model_name='articlestored',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Profile'),
        ),
        migrations.AddField(
            model_name='articleliked',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Profile'),
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Profile'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='article.Category', verbose_name='category'),
        ),
    ]
