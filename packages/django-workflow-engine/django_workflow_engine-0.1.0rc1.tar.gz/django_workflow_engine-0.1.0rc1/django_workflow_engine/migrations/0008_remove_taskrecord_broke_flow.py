# Generated by Django 4.0.3 on 2022-07-07 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("django_workflow_engine", "0007_flow_running"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="taskrecord",
            name="broke_flow",
        ),
    ]
