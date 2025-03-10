# Generated by Django 4.2.10 on 2025-02-24 10:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_rename_nickname_groupmember_group_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_members', to='api.groups')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_memberships', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='GroupMember',
        ),
        migrations.AddConstraint(
            model_name='groupcontact',
            constraint=models.UniqueConstraint(fields=('user', 'group'), name='unique_user_in_group'),
        ),
    ]
