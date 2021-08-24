# Generated by Django 3.2.5 on 2021-07-18 15:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0002_material'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('page_no', models.IntegerField()),
                ('material_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='class.material')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='class.student')),
            ],
        ),
    ]
