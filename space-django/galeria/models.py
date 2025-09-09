"""
PT: Modelos da aplicação de galeria de fotos do espaço.
EN: Models for the space gallery application.
"""

from django.db import models
from datetime import datetime


class Fotografia(models.Model):
    """PT: Representa uma fotografia com metadados e arquivo de imagem.
    EN: Represents a photograph with metadata and image file.
    """

    # PT: Categorias possíveis (usadas para filtros/etiquetas)
    # EN: Allowed categories (used for filters/labels)
    OPCOES_CATEGORIA = [
        ("NEBULOSA", "Nebulosa"),
        ("GALÁXIA", "Galáxia"),
        ("PLANETA", "Planeta"),
        ("ESTRELA", "Estrela"),
    ]

    # PT: Título da foto | EN: Photo title
    nome = models.CharField(max_length=100, null=False, blank=False)
    # PT: Subtítulo/legenda curta | EN: Short caption/subtitle
    legenda = models.CharField(max_length=150, null=False, blank=False)
    # PT: Categoria da imagem | EN: Image category
    categoria = models.CharField(max_length=100, choices=OPCOES_CATEGORIA, default="")
    # PT: Descrição longa opcional | EN: Optional long description
    descricao = models.TextField(null=True, blank=True)
    # PT: Arquivo da imagem; armazenado em pasta por data | EN: Image file; stored by date path
    imagem = models.ImageField(upload_to='fotos/%Y/%m/%d/', blank=True)
    # PT: Data/hora associada à imagem | EN: Datetime associated to the image
    data_imagem = models.DateTimeField(default=datetime.now, blank=False)
    # PT: Controle de publicação | EN: Publish toggle
    publicada = models.BooleanField(default=False)

    def __str__(self) -> str:
        """PT: Exibe o nome no admin e no shell. EN: Displays the name in admin/shell."""
        return self.nome
