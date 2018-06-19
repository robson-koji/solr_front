# -*- coding: utf-8 -*-
from django.db import models
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta, MO




class Pesquisa(models.Model):
    """
    Classe abstrata necessaria para utilizar o CBV no buscador.
    Na modelagem da parte do usuario e da indexacao, verificar se eh possivel
    excluir essa classe e utilizar outra real.
    """
    # fields = []
    fields = "__all__"
    pass



class RelatedCollectionsCheck(models.Model):
    """
    Armazena o status (data) da contagem das collections relacionadas e
    o status (data) da indexacao da sub-collection relacionada.

    Model utilizado para controlar a frequencia e status de atualizacao das
    informacoes de collections relacioadas.
    """
    hash_querybuilder = models.IntegerField(u'HashQuerybuilder', unique=True, help_text='Hash do texto da busca do querybuilder, apos o Join com a respectiva collection relacionada.' )
    join = models.TextField(u'Join entre as collections da busca realizada', max_length=64)
    qt_col1 = models.IntegerField(u'Quantidade do join na coluna 1',help_text='' )
    qt_col2 =  models.IntegerField(u'Quantidade do join na coluna 2',help_text='' )
    # top_col1 =
    # top_col2 =
    created_date = models.DateTimeField(u'Data de criação da busca')
    counted_date = models.DateTimeField(u'Última contagem da busca relacionada', null=True)
    indexed_date = models.DateTimeField(u'Última indexação da sub-collection', null=True)


    def recount(self, threshold_date=None):
        """
        Retorna se os dados indexados estao validos
        # Passar para o arquivo de configuracao da collection, ou via admin, como
        # configurar a data de expiracao da verificacao do recount.
        # Para o caso da BV que atualiza uma vez por semana aos finais de semana,
        # pega a data da ultima segunda-feira e caso a ultima atualizacao counted_date
        # seja anterior a atualizacao dos dados (ultima segunda-feira), reconta.
        """
        # Caso problema de inconsistencia no campo counted_data. (problemas em dev)
        if not isinstance(self.counted_date , datetime):
            return True


        # Utilizando esse threshold_date para a BV
        today = date.today()
        last_monday = today + relativedelta(weekday=MO(-1))

        if not threshold_date: threshold_date = last_monday
        if self.counted_date.date() < threshold_date:
            return True
        return False

        

    def reindex(self, threshold_date=None):
        # Caso problema de inconsistencia no campo indexed_date. (problemas em dev)
        if not isinstance(self.indexed_date , datetime):
            return True

        # Utilizando esse threshold_date para a BV
        today = date.today()
        last_monday = today + relativedelta(weekday=MO(-1))

        if not threshold_date: threshold_date = last_monday
        if self.indexed_date.date() < threshold_date:
            return True
        return False



    def save(self, **kwargs):
        if self.id:
            self.counted_date = datetime.now()
        else:
            self.created_date = datetime.now()
        return super(RelatedCollectionsCheck,self).save()
