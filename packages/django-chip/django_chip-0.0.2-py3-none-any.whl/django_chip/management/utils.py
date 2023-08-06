import os
import sys

from django_extensions.management.signals import post_command, pre_command


def _make_writeable(filename):
    """
    Make sure that the file is writable. Useful if our source is
    read-only.
    """
    import stat
    if sys.platform.startswith('java'):
        # On Jython there is no os.access()
        return
    if not os.access(filename, os.W_OK):
        st = os.stat(filename)
        new_permissions = stat.S_IMODE(st.st_mode) | stat.S_IWUSR
        os.chmod(filename, new_permissions)


def signalcommand(func):
    """Python decorator for management command handle defs that sends out a pre/post signal."""

    def inner(self, *args, **kwargs):
        pre_command.send(self.__class__, args=args, kwargs=kwargs)
        ret = func(self, *args, **kwargs)
        post_command.send(self.__class__, args=args, kwargs=kwargs, outcome=ret)
        return ret
    return inner
