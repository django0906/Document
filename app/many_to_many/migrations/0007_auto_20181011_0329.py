# Generated by Django 2.1.2 on 2018-10-11 03:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('many_to_many', '0006_auto_20181011_0131'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='relation',
            unique_together={('from_user', 'to_user')},
        ),
    ]
