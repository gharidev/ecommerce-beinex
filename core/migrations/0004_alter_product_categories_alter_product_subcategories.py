# Generated by Django 4.1 on 2022-08-20 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_category_options_alter_subcategory_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, to='core.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='subcategories',
            field=models.ManyToManyField(blank=True, to='core.subcategory'),
        ),
    ]
