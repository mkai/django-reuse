"""
shell_plus management command.

Like the 'shell' command but autoloads the models of all installed Django apps.
Stripped-down version of django_extensions/management/commands/shell_plus.py

"""
from optparse import make_option
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = "Like the 'shell' command but autoloads the models of all installed Django apps."
    requires_model_validation = True
    option_list = NoArgsCommand.option_list + (
        make_option('--dont-load', action='append', dest='dont_load', default=[],
                    help='Do not autoload the models in the given app. Can be used several times.'),
        make_option('--quiet-load', action='store_true', default=False, dest='quiet_load',
                    help='Do not display messages about which models were auto-loaded.'),
    )

    def handle_noargs(self, **options):
        # Run normal Python shell
        imported_objects = import_objects(options, self.style)
        import code
        code.interact(local=imported_objects)


def import_objects(options, style):
    from django.conf import settings
    from django.db.models.loading import get_models, get_apps

    imported_objects = {'settings': settings}
    dont_load = options.get('dont_load')  # optparse will set this to [] if it doesn't exist
    quiet_load = options.get('quiet_load')
    model_aliases = getattr(settings, 'SHELL_PLUS_MODEL_ALIASES', {})

    for app_mod in get_apps():
        app_models = get_models(app_mod)
        if not app_models:
            continue
        app_name = app_mod.__name__.split('.')[-2]
        if app_name in dont_load:
            continue
        app_aliases = model_aliases.get(app_name, {})
        model_labels = []

        for model in app_models:
            try:
                imported_object = getattr(__import__(app_mod.__name__, {}, {}, model.__name__), model.__name__)
                model_name = model.__name__
                if "%s.%s" % (app_name, model_name) in dont_load:
                    continue
                alias = app_aliases.get(model_name, model_name)
                imported_objects[alias] = imported_object
                if model_name == alias:
                    model_labels.append(model_name)
                else:
                    model_labels.append("%s (as %s)" % (model_name, alias))
            except AttributeError as e:
                if not quiet_load:
                    print(style.ERROR("Failed to import '%s' from '%s' reason: %s" % (model.__name__, app_name, str(e))))
                continue
        if not quiet_load:
            print(style.SQL_COLTYPE("From '%s' autoload: %s" % (app_mod.__name__.split('.')[-2], ", ".join(model_labels))))

    return imported_objects
