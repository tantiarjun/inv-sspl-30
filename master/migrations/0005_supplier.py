# Generated by Django 5.1.1 on 2024-09-23 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0004_item_added_on'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_name', models.CharField(max_length=200)),
                ('phone_no', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=400)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
    ]
