"""
PT: Views simples para a galeria espacial (site público).
EN: Simple views for the space gallery (public site).
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from galeria.models import Fotografia


def index(request):
    """PT: Página inicial com lista de fotos publicadas e busca por termo.
    EN: Home page listing published photos with a search term filter.

    - Usa Q objects para combinar filtros (publicada E (nome OU legenda contém termo)).
    - Ordena por data da imagem (mais antigas primeiro; ajuste para "-data_imagem" se quiser recentes primeiro).
    """
    termo = request.GET.get("q")

    if termo:
        fotografias = (
            Fotografia.objects
            .filter(
                Q(publicada=True) & (
                    Q(nome__icontains=termo) |
                    Q(legenda__icontains=termo)
                )
            )
            .order_by("data_imagem")
        )
    else:
        fotografias = Fotografia.objects.filter(publicada=True).order_by("data_imagem")

    return render(request, 'galeria/index.html', {'cards': fotografias})


def imagem(request, foto_id):
    """PT: Exibe página com detalhes de uma foto.
    EN: Displays the detail page for a photo.
    """
    fotografia = get_object_or_404(Fotografia, pk=foto_id)
    return render(request, 'galeria/imagem.html', {'fotografia': fotografia})


def atualizar_foto(request, foto_id):
    """PT: Formulário simples para atualizar metadados e arquivo de imagem.
    EN: Simple form to update metadata and image file.
    """
    fotografia = get_object_or_404(Fotografia, pk=foto_id)

    if request.method == 'POST':
        # PT: Coleta dados do formulário; validações podem ser adicionadas.
        # EN: Collects form data; validations can be added.
        fotografia.nome = request.POST.get('nome')
        fotografia.legenda = request.POST.get('legenda')
        fotografia.descricao = request.POST.get('descricao')

        if request.FILES.get('imagem'):
            fotografia.imagem = request.FILES['imagem']

        fotografia.save()
        return redirect('index')

    return render(request, 'galeria/atualizar.html', {'fotografia': fotografia})
