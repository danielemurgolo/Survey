# Generated by Django 4.2 on 2023-04-12 15:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("survey", "0004_rename_question_integerquestion_text"),
    ]

    operations = [
        migrations.RenameField(
            model_name="countryquestion",
            old_name="question",
            new_name="text",
        ),
    ]
