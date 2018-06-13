import json


def get_navigate_fields(request):
    """ Para cada elemento da arvore, retorna os campos solicitados """

    if not 'navigation' in request.session:
        return {}

    navigate_fieds = []

    def get_rec_navigate_fields(dict, collection):

        # import pdb; pdb.set_trace()

        navigate_fieds.append({'title':dict['title'], 'description':dict['description'], 'label':unicode(dict['label']), 'id':dict['id'], 'collection':unicode(collection), 'tree':unicode(dict['tree'])})
        for vertice in dict['tree']:
            # import pdb; pdb.set_trace()
            # analisa recursivamente os vertices da navegacao.
            get_rec_navigate_fields(vertice,vertice['collection'])

    # Pega na sessao o objeto navigation.
    navigation = request.session['navigation']

    #import pdb; pdb.set_trace()
    # inicia captura dos fields dos vertices contidos na navegacao.
    get_rec_navigate_fields(navigation[navigation.keys()[0]], navigation.keys()[0])

    return {'navigate_fieds':navigate_fieds}





def navigation_tree(request):
    """ Retorna arvore de navegacao """

    if not 'navigation' in request.session:
        return {}


    # import pdb; pdb.set_trace()
    navigation_tree = []

    # import pdb; pdb.set_trace()
    def get_rec_navigate_fieds(dict, collection, parent_id):
        my_dict = {'title':dict['title'], 'description':dict['description'], 'label':dict['label'], 'id':dict['id'], 'collection':dict['collection'], 'parent_id':parent_id }
        navigation_tree.append(json.dumps(my_dict))

        # import pdb; pdb.set_trace()
        for vertice in dict['tree']:
            # analisa recursivamente os vertices da navegacao.
            get_rec_navigate_fieds(vertice, dict['collection'], dict['id'])

    # Pega na sessao o objeto navigation.
    navigation = request.session['navigation']



    # inicia captura dos fields dos vertices contidos na navegacao.
    get_rec_navigate_fieds(navigation[navigation.keys()[0]], navigation.keys()[0], "null")

    # import pdb; pdb.set_trace()

    return {'navigation_tree':navigation_tree}
