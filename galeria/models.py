from django.db import models
from datetime import datetime

class Fotografia(models.Model):
    
    OPCOES_CATEGORIA = [
        ("NEBULOSA", "Nebulosa"),
        ("GALÁXIA", "Galáxia"),
        ("PLANETA", "Planeta"),
        ("ESTRELA", "Estrela"),
        ]
    
    nome = models.CharField(max_length=100, null=False, blank=False)
    legenda = models.CharField(max_length=150, null=False, blank=False)
    categoria = models.CharField(max_length=100, choices=OPCOES_CATEGORIA, default="")
    descricao = models.TextField(null=True, blank=True)
    imagem = models.ImageField(upload_to='fotos/%Y/%m/%d/', blank=True)
    data_imagem = models.DateTimeField(default=datetime.now, blank=False)
    publicada = models.BooleanField(default=False)
    
  
    def __str__(self):
        return self.nome