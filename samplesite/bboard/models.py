from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError


def func():
    return ""


class Rubric(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Ad(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name="ZAGOLOVOK",
        help_text="Nazvanie objekta",
        default='func',
        unique=True,
        db_index=True,
        null=True,
        blank=True,
    )
    content = models.TextField(
        blank=True,
        null=True,
    )
    price = models.FloatField(
        null=True,
        blank=True,
    )
    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    rubric = models.ForeignKey(
        Rubric,
        on_delete=models.PROTECT,
        related_name='entries',
        to_field='name',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'REKLAMA'
        verbose_name_plural = 'REKLAMI'
        unique_together = ('title', 'published')

    def __str__(self):
        return "{} {}".format(self.title, self.published)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        print("SAVE METHOD EXECUTION")
        super(Ad, self).save(force_insert, force_update, using, update_fields)
        # Do things after creating

    def delete(self, using=None, keep_parents=False):
        print("DELETE METHOD EXECUTION")
        super(Ad, self).delete(using, keep_parents)
        # Do things after delete

    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Set content for your object')
        if self.price and self.price < 0:
            errors['price'] = ValidationError('Set positive price for your object')

        if errors:
            raise ValidationError(errors)


class Spare (models.Model):
    name = models.CharField(max_length=30)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        print("SAVE METHOD EXECUTION")
        super(Spare, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        print("DELETE METHOD EXECUTION")
        super(Spare, self).delete(using, keep_parents)
        # Do things after delete


class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        print("SAVE METHOD EXECUTION")
        super(Machine, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        print("DELETE METHOD EXECUTION")
        super(Machine, self).delete(using, keep_parents)
