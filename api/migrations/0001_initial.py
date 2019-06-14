# Generated by Django 2.2.2 on 2019-06-14 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('score', models.FloatField()),
                ('link', models.CharField(max_length=512)),
                ('year', models.IntegerField()),
                ('genres', models.ManyToManyField(to='api.Genre')),
            ],
        ),
    ]
