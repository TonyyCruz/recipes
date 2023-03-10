# Generated by Django 4.1.7 on 2023-02-24 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0002_alter_recipe_cover"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="cover",
            field=models.ImageField(
                default="base_images/recipes/covers/No-Image-Placeholder.svg.png",
                upload_to="recipes/covers/%Y/%m/%d",
            ),
        ),
    ]
