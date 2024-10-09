from django.db import models

# Create your models here.
class Visita(models.Model):
    ip = models.GenericIPAddressField() # IP do visitante
    visitas = models.PositiveBigIntegerField(default=1) # contador de visitas
    ultima_visita = models.DateTimeField(auto_now=True) # Ultima vez que o visitante acessou
    cidade = models.CharField(max_length=100, null=True, blank=True)
    regiao = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.ip} - {self.visitas} visitas'