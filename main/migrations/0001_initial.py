# Generated by Django 3.2.13 on 2022-06-13 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_price', models.FloatField(default=0)),
                ('max_price', models.FloatField(default=0)),
                ('tick_size', models.FloatField(default=0)),
                ('min_qty', models.FloatField(default=0)),
                ('max_qty', models.FloatField(default=0)),
                ('step_size', models.FloatField(default=0)),
                ('onboard_date', models.DateTimeField(null=True)),
                ('base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base', to='main.coin')),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quote', to='main.coin')),
            ],
        ),
        migrations.CreateModel(
            name='Candle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_time', models.DateTimeField()),
                ('close_time', models.DateTimeField()),
                ('open', models.FloatField(null=True)),
                ('high', models.FloatField(null=True)),
                ('close', models.FloatField(null=True)),
                ('low', models.FloatField(null=True)),
                ('volume', models.FloatField(null=True)),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.symbol')),
            ],
        ),
    ]