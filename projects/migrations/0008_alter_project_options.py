# Generated by Django 3.2.9 on 2022-02-17 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_alter_review_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-vote_ratio', '-vote_total', 'title']},
        ),
    ]
