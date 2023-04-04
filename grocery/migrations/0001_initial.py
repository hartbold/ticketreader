# Generated by Django 4.2 on 2023-04-03 19:46

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
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserStorage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='grocery.storage')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('total', models.BinaryField()),
                ('processedText', models.CharField(max_length=5000)),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='grocery.storage')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('amount', models.IntegerField(default=0)),
                ('unit', models.CharField(choices=[('KL', 'Kilos'), ('GR', 'Grams'), ('UN', 'Unitats'), ('PK', 'Paquets'), ('LI', 'Litres'), ('OT', 'Altres')], default='OT', max_length=2)),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='grocery.storage')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
