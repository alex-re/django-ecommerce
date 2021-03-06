# Generated by Django 3.1.4 on 2021-01-23 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_delete_refund'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='refund_granted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='refund_requested',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('reason', models.CharField(max_length=1000)),
                ('accepted', models.BooleanField(default=False)),
                ('order_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.order')),
            ],
        ),
    ]
