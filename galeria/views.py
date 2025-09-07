from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from galeria.models import Fotografia


from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from galeria.models import Fotografia


def index(request):
    termo = request.GET.get("q")

    if termo:
        fotografias = Fotografia.objects.filter(
            Q(publicada=True) & (
                Q(nome__icontains=termo) |
                Q(legenda__icontains=termo)
            )
        ).order_by("data_imagem")
    else:
        fotografias = Fotografia.objects.filter(
            publicada=True).order_by("data_imagem")

    return render(request, 'galeria/index.html', {'cards': fotografias})

def imagem(request, foto_id):
    fotografia = get_object_or_404(Fotografia, pk=foto_id)
    return render(request, 'galeria/imagem.html', {'fotografia': fotografia})


def atualizar_foto(request, foto_id):
    fotografia = get_object_or_404(Fotografia, pk=foto_id)

    if request.method == 'POST':
        fotografia.nome = request.POST.get('nome')
        fotografia.legenda = request.POST.get('legenda')
        fotografia.descricao = request.POST.get('descricao')

        if request.FILES.get('imagem'):
            fotografia.imagem = request.FILES['imagem']

        fotografia.save()
        return redirect('index')

    return render(request, 'galeria/atualizar.html', {'fotografia': fotografia})
