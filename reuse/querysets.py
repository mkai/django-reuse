from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey


class GFKQuerySet(QuerySet):
    """
    A QuerySet with a fetch_generic_relations() method to bulk fetch
    all generic related items.  Similar to select_related(), but for
    generic foreign keys.

    From: http://djangosnippets.org/snippets/1773/
    Based on http://www.djangosnippets.org/snippets/984/
    Firstly improved at http://www.djangosnippets.org/snippets/1079/

    """
    def fetch_generic_relations(self):
        qs = self._clone()

        gfk_fields = [g for g in self.model._meta.virtual_fields 
                      if isinstance(g, GenericForeignKey)]

        ct_map = {}
        item_map = {}
        data_map = {}

        for item in qs:
            for gfk in gfk_fields:
                ct_id_field = self.model._meta.get_field(gfk.ct_field).column
                # print "ct_id=%s" % getattr(item, ct_id_field)
                # print "item_id=%s" % getattr(item, gfk.fk_field)
                # print "%s %s" % (ct_id_field, getattr(item, ct_id_field))
                ct_map.setdefault(
                    (getattr(item, ct_id_field)), {}
                    )[getattr(item, gfk.fk_field)] = (gfk.name, item.id)
            item_map[item.id] = item

        for (ct_id), items_ in ct_map.items():
            if (ct_id):
                ct = ContentType.objects.get_for_id(ct_id)
                mgr = ct.model_class().objects.select_related()
                for o in mgr.filter(id__in=items_.keys()).all():
                    (gfk_name, item_id) = items_[o.id]
                    data_map[(ct_id, o.id)] = o

        for item in qs:
            for gfk in gfk_fields:
                if (getattr(item, gfk.fk_field) != None):
                    ct_id_field = self.model._meta.get_field(gfk.ct_field).column
                    setattr(item, gfk.name, data_map[(getattr(item, ct_id_field), 
                        getattr(item, gfk.fk_field))])

        return qs
