import os
import sys
import shutil
from django.conf import settings

from django.core.management.base import BaseCommand

from django_chip.management.utils import _make_writeable


class Command(BaseCommand):
    help = "Create django deploy config."

    def add_arguments(self, parser):
        # parser.add_argument('sample', nargs='+')
        pass

    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR
        copy_template('deploy_template', base_dir, **options)


def copy_template(template_name, copy_to, **options):
    """Copy the specified template directory to the copy_to location"""
    import django_chip

    template_dir = os.path.join(django_chip.__path__[0], 'tmpl', template_name)
    project_name = os.path.split(copy_to)[-1]
    
    # walk the template structure and copies it
    for d, subdirs, files in os.walk(template_dir):
        relative_dir = d[len(template_dir) + 1:]

        if relative_dir and not os.path.exists(os.path.join(copy_to, relative_dir)):
            os.mkdir(os.path.join(copy_to, relative_dir))
        for i, subdir in enumerate(subdirs):
            if subdir.startswith('.'):
                del subdirs[i]
        for f in files:
            if f.endswith(('.pyc', '.pyo')) or f.startswith(('.DS_Store', '__pycache__')):
                continue
            path_old = os.path.join(d, f)
            path_new = os.path.join(copy_to, relative_dir, f)[:-5]
            if os.path.exists(path_new):
                path_new = os.path.join(copy_to, relative_dir, f)[:-5]
                if os.path.exists(path_new):
                    continue
            
            with open(path_old, 'r') as fp_orig:
                data = fp_orig.read()
                data = data.replace('{{ project_name }}', project_name)
                
                with open(path_new, 'w') as fp_new:
                    fp_new.write(data)
            try:
                shutil.copymode(path_old, path_new)
                _make_writeable(path_new)
            except OSError:
                sys.stderr.write("Notice: Couldn't set permission bits on %s. You're probably using an uncommon filesystem setup. No problem.\n" % path_new)