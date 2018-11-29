# -*- coding: utf-8 -*-


def create_one_dict(dic):
    dict_f = {}
    for k, v in dic.iteritems():
        if type(v) == dict:
            dict_x = create_one_dict(v)
            for xkey, xv in dict_x.iteritems():
                if xkey in dict_f.keys():
                    for i in xv:
                        dict_f[xkey] = list(set(dict_f[xkey]) + set(i))
                        # dict_f[xkey].append(i)
                else:
                    dict_f[xkey] = xv
        elif type(v) == list:
            if k in dict_f.keys():
                if len(dict_f[k]) > 0:
                    for i in dic[k]:
                        dict_f[k].append(i)
            else:
                dict_f[k] = v
        else:
            dict_f[k] = [v]
    return dict_f
