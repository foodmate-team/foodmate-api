# Generated by Django 2.2.7 on 2019-11-10 21:28

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
            ],
        ),
        migrations.CreateModel(
            name='Chef',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('ditance_from_subway', models.IntegerField()),
                ('address', models.CharField(blank=True, max_length=200)),
                ('contact_fb', models.CharField(blank=True, max_length=50)),
                ('contact_ok', models.CharField(blank=True, max_length=50)),
                ('contact_inst', models.CharField(blank=True, max_length=50)),
                ('contact_vk', models.CharField(blank=True, max_length=50)),
                ('menu_items', models.ManyToManyField(to='chefs.MenuItem')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('users.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
