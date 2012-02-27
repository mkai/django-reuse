from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey


def prefetch_related(qs):
    """
    A method to bulk-fetch all generic related items.

    Similar to select_related(), but for generic foreign keys.

    Note: this iterates over the queryset (thereby evaluating it), so this method
    should only be called when there will be no further modification (filtering etc.)
    on the queryset.

    From: http://djangosnippets.org/snippets/1773/
    Based on http://www.djangosnippets.org/snippets/984/
    Firstly improved at http://www.djangosnippets.org/snippets/1079/

    """
    qs = qs._clone()

    gfk_fields = [g for g in qs.model._meta.virtual_fields if isinstance(g, GenericForeignKey)]
    
    ct_map = {}
    item_map = {}
    data_map = {}
    
    for item in qs:
        for gfk in gfk_fields:
            ct_id_field = qs.model._meta.get_field(gfk.ct_field).column
            #print "ct_id=%s" % getattr(item, ct_id_field)
            #print "item_id=%s" % getattr(item, gfk.fk_field)
            #print "%s %s" % (ct_id_field, getattr(item, ct_id_field))
            fk_field = getattr(item, gfk.fk_field)
            if fk_field:
                fk_field = int(fk_field)  # if left out, dict key will be type unicode?
            ct_map.setdefault((getattr(item, ct_id_field)), {})[fk_field] = (gfk.name, item.pk)
        item_map[item.pk] = item

    for (ct_id), items_ in ct_map.items():
        if (ct_id):
            ct = ContentType.objects.get_for_id(ct_id)
            for o in ct.model_class().objects.select_related().filter(id__in=items_.keys()):
                # if not items_.get(o.pk):
                #     print('%s (%s) not in items_' % (o.pk, type(o.pk)))
                #     continue
                (gfk_name, item_id) = items_[o.pk]
                data_map[(ct_id, o.pk)] = o

    for item in qs:
        for gfk in gfk_fields:
            if (getattr(item, gfk.fk_field) != None):
                ct_id_field = qs.model._meta.get_field(gfk.ct_field).column
                fk_field = getattr(item, gfk.fk_field)
                if fk_field:
                    fk_field = int(fk_field)  # TODO: may not always be correct
                lookup_key = (getattr(item, ct_id_field), fk_field)
                if not data_map.get(lookup_key):
                    # print('actstream gfk.py: %s not in data_map' % str(lookup_key))
                    continue
                prefetched_obj = data_map[lookup_key]
                setattr(item, gfk.name, prefetched_obj)

    return qs
