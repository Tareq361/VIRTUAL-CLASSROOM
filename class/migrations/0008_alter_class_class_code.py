# Generated by Django 4.0 on 2022-06-03 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0007_alter_class_class_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='class_code',
            field=models.CharField(default='CkaFZfY8', max_length=120),
        ),
    ]
