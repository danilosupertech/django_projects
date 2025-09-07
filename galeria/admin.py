from django.contrib import admin
from galeria.models import Fotografia

class ListandoFotos(admin.ModelAdmin):
    list_display = ('id', 'publicada','nome', 'legenda', 'categoria')
    list_display_links = ('id', 'nome')
    list_filter = ('categoria',)
    list_editable = ('publicada',)
    search_fields = ('nome', 'legenda', 'categoria')
    list_per_page = 10
    
    
# Register your models here.
admin.site.register(Fotografia, ListandoFotos)
