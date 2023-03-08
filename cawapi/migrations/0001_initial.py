# Generated by Django 4.1.6 on 2023-03-08 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('goal_entry', models.CharField(max_length=500)),
                ('affirmation', models.CharField(max_length=255)),
                ('distraction', models.CharField(max_length=255)),
                ('significant', models.BooleanField(default=False)),
                ('overall_rating', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('answer', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('profile_image_url', models.URLField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
                ('created_on', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField()),
                ('journal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal_id', to='cawapi.journal')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_id', to='cawapi.survey')),
            ],
        ),
        migrations.AddField(
            model_name='journal',
            name='writer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cawapi.user'),
        ),
    ]
