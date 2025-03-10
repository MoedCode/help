# Generated by Django 4.2.10 on 2025-02-20 10:47

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_locations_groups_alter_helprequest_group_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='helprequest',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='helprequest',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='locations',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='locations',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='message',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='message',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='groups',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='helprequest',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='locations',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='users',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='users',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
