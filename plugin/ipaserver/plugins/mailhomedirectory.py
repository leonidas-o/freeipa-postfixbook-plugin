from ipaserver.plugins import user
from ipalib.parameters import Str
from ipalib.text import _
from .baseldap import add_missing_object_class

user.user.takes_params += (
    Str(
        'mailhomedirectory?',
        cli_name='mailhomedirectory',
        label=_('Mail home directory'),
        doc=_(
            'The absolute path to the mail user home directory'
        ),
        autofill=False,
    ),
)

user.user.default_attributes.append('mailhomedirectory')


def useradd_precallback(self, ldap, dn, entry_attrs, attrs_list, *keys, **options):

    add_missing_object_class(ldap, u'postfixbookmailaccount', dn, entry_attrs, update=False)
    return dn


user.user_add.register_pre_callback(useradd_precallback)


def usermod_precallback(self, ldap, dn, entry_attrs, attrs_list, *keys, **options):

    add_missing_object_class(ldap, u'postfixbookmailaccount', dn)
    return dn


user.user_mod.register_pre_callback(usermod_precallback)