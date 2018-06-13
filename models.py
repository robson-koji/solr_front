# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime



class Pesquisa(models.Model):
    """
    Classe abstrata necessaria para utilizar o CBV no buscador.
    Na modelagem da parte do usuario e da indexacao, verificar se eh possivel
    excluir essa classe e utilizar outra real.
    """
    # fields = []
    fields = "__all__"
    pass



class RelatedIndexing(models.Model):
    """
    Armazena o status da indexacao das collections relacionadas.
    """
    hash_querybuilder = models.IntegerField(u'HashQuerybuilder', unique=True, help_text='Hash do texto da busca do querybuilder, apos o Join com a respectiva collection relacionada.' )
    join = models.TextField(u'Join entre as collections da busca realizada', max_length=64)
    qt_col1 = models.IntegerField(u'Quantidade do join na coluna 1',help_text='' )
    qt_col2 =  models.IntegerField(u'Quantidade do join na coluna 2',help_text='' )
    # top_col1 =
    # top_col2 =
    created_date = models.CharField(u'Data de criação da busca', max_length=64)
    modified_date = models.CharField(u'Última atualização da busca', max_length=64)


    def date_valid(self):
        """
        Retorna se os dados indexados estao validos
        """
        # Implemnetar regra. Por enquanto nao existe, retornando sempre true.
        return True



    def save(self, **kwargs):
        if self.id:
            self.modified_date = datetime.now()
        else:
            self.created_date = datetime.now()
        return super(RelatedIndexing,self).save()
