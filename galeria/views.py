from django.shortcuts import render, get_object_or_404, redirect
from galeria.models import Fotografia



def index(request):
    
    # dados = {data_imagem
    #     1: {'nome': 'Imagem 1',
    #         'legenda': 'Descrição da Imagem 1 / Fotógrafo 1 / Satélite 1'},
    #     2: {'nome': 'Imagem 2',
    #         'legenda': 'Descrição da Imagem 2 / Fotógrafo 2 / Satélite 2'},
    #     3: {'nome': 'Imagem 3',
    #         'legenda': 'Descrição da Imagem 3 / Fotógrafo 3 / Satélite 3'},
    # }
    fotografias = Fotografia.objects.order_by('data_imagem').filter(publicada=True).all()
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
        #return redirect('imagem', foto_id=fotografia.id)
        return redirect('index')
        

    return render(request, 'galeria/atualizar.html', {'fotografia': fotografia})
