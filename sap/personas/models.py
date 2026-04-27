from django.db import models


class Domicilio(models.Model):
    calle = models.CharField(max_length=255)
    no_calle = models.CharField(max_length=20)
    pais = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Domicilio'
        verbose_name_plural = 'Domicilios'
        ordering = ['-id']

    def __str__(self):
        return f'{self.calle} #{self.no_calle}, {self.pais}'


class Persona(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    domicilio = models.ForeignKey(
        Domicilio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='personas'
    )

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        ordering = ['-id']

    def __str__(self):
        return f'{self.nombre} {self.apellido} — {self.email}'

    @property
    def nombre_completo(self):
        return f'{self.nombre} {self.apellido}'