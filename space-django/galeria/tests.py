"""Testes de regressão para o comportamento público da galeria."""

from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse

from galeria.models import Fotografia


class IndexViewTests(TestCase):
    """Testes para a view pública ``index`` da galeria."""

    def _create_photo(self, **kwargs):
        """Cria uma instância de ``Fotografia`` com valores padrão semânticos.

        Os testes sobrescrevem apenas os atributos relevantes para o cenário,
        evitando repetição de dados obrigatórios e mantendo os objetos em um
        estado válido (por exemplo, marcados como publicados por padrão).
        """
        defaults = {
            "nome": "Nebulosa do Caranguejo",
            "legenda": "Registro do telescópio Hubble",
            "categoria": "NEBULOSA",
            "descricao": "Imagem icônica da nebulosa do caranguejo.",
            "publicada": True,
        }
        defaults.update(kwargs)
        return Fotografia.objects.create(**defaults)

    def test_index_lists_only_published_photos(self):
        """A página deve exibir apenas fotografias publicadas."""

        publicada = self._create_photo(nome="Via Láctea")
        self._create_photo(nome="Galáxia não publicada", publicada=False)

        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        cards = list(response.context["cards"])
        self.assertEqual(cards, [publicada])

    def test_index_search_filters_results(self):
        """A busca deve filtrar pelo nome ou legenda de forma case-insensitive."""

        antigo = self._create_photo(
            nome="Galáxia Andromeda",
            data_imagem=datetime.now() - timedelta(days=1),
        )
        outro = self._create_photo(nome="Constelação de Órion")

        response = self.client.get(reverse("index"), {"q": "andromeda"})

        cards = list(response.context["cards"])
        self.assertEqual(cards, [antigo])
        self.assertNotIn(outro, cards)

    def test_index_renders_placeholder_when_photo_has_no_image(self):
        """Deve mostrar a imagem padrão quando a fotografia não possui arquivo associado."""

        self._create_photo(nome="Nebulosa Fantasma", imagem="")

        response = self.client.get(reverse("index"))

        self.assertContains(response, "assets/imagens/galeria/sem-foto.png")
