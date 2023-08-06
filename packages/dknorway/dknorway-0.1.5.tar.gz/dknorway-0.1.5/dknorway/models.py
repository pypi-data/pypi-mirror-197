"""
Models used for looking up poststed from postnr.
Updated by ./posten_postnrimport.py
"""

# pylint: disable=no-init,too-few-public-methods,old-style-class


from django.db import models


class Fylke(models.Model):
    """Model for Norwegian 'fylke'.
    """
    nr = models.CharField(max_length=2, primary_key=True)
    navn = models.CharField(max_length=40)
    active = models.BooleanField(default=True)
    note = models.CharField(max_length=255, null=True, blank=True)

    @classmethod
    def for_postnr(cls, postnr):
        """Returns the ``Fylke`` object for ``postnr``.
        """
        try:
            return PostSted.objects.get(postnummer=postnr).kommune.fylke
        except PostSted.DoesNotExist:
            raise cls.DoesNotExist

    def __str__(self):
        return self.navn

    class Meta:
        "Meta options for :model:`Fylke`."
        verbose_name_plural = 'Fylker'
        ordering = ['nr']
        app_label = 'dknorway'
    

class Kommune(models.Model):
    "Model for all kommuner in Norway."
    kode = models.CharField(max_length=4)
    navn = models.CharField(max_length=30)
    active = models.BooleanField(default=True)
    note = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.navn} ({self.fylke})'

    @property
    def fylke(self):
        "Which fylke does the Kommune belong to?"
        return Fylke.objects.get(nr=self.kode[:2])

    class Meta:
        "Meta options for :model:`Kommune`."
        verbose_name_plural = 'Kommuner'
        ordering = ['kode']
        app_label = 'dknorway'
    

class PostSted(models.Model):
    "A poststed as defined by the Norwegian postal service."
    postnummer = models.CharField(max_length=4)
    poststed = models.CharField(max_length=35)
    kommune = models.ForeignKey(Kommune, null=True, blank=True, on_delete=models.CASCADE)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    active = models.BooleanField(default=True)
    note = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.postnummer} {self.poststed}'

    @staticmethod
    def get(nr):
        "Convenience function to get the :model:`PostSted` from postnr."
        try:
            ps = PostSted.objects.get(postnummer=nr)
            return ps.poststed
        except PostSted.DoesNotExist:
            return ''
        
    class Meta:
        "Meta options for `model`:PostSted."
        verbose_name_plural = 'Poststed'
        app_label = 'dknorway'
