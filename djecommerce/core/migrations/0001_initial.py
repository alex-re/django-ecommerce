# Generated by Django 3.1.4 on 2021-01-22 19:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('TEH', 'Tehran'), ('KAR', 'Karaj'), ('ARA', 'Arak')], max_length=3)),
                ('city', models.CharField(choices=[('TEH', 'Tehran'), ('MAL', 'Malard'), ('AND', 'Andisheh')], max_length=5)),
                ('neighbour', models.CharField(choices=[('APA', 'Apadana'), ('ARA', 'Ararat'), ('AZA', 'Azadi')], max_length=5)),
                ('postal_address', models.CharField(max_length=200)),
                ('plaque', models.CharField(max_length=5)),
                ('unit', models.CharField(max_length=30)),
                ('postal_code', models.CharField(help_text='postal code must be 10 numbers without dash', max_length=10)),
                ('rec_fname', models.CharField(max_length=100)),
                ('rec_lname', models.CharField(max_length=100)),
                ('rec_national_code', models.CharField(help_text='national code must be 10 numbers without dash', max_length=10)),
                ('rec_phone_number', models.CharField(help_text='Example: 09123456789', max_length=11)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('specs', models.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField()),
                ('being_delivered', models.BooleanField(default=False)),
                ('received', models.BooleanField(default=False)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.address')),
                ('products', models.ManyToManyField(to='core.OrderProduct')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
