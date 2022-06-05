from ipaserver.plugins import user
from ipalib.parameters import Str
from ipalib.text import _
from .baseldap import add_missing_object_class

user.user.takes_params += (
    Str(
        'mailforwardingaddress*',
        cli_name='mailforwardingaddress',
        label=_('Mail forwarding address'),
        doc=_(
            'Address(es) to forward all incoming messages to.'
        ),
        autofill=False,
        pattern='^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$',
        pattern_errmsg=''.join(
            'may only be "", '
            'or a valid email address (e.g. user@domain.com)'
        ),
    ),
)

user.user.default_attributes.append('mailforwardingaddress')


def useradd_precallback(self, ldap, dn, entry_attrs, attrs_list, *keys, **options):

    add_missing_object_class(ldap, u'postfixbookmailforward', dn, entry_attrs, update=False)
    return dn


user.user_add.register_pre_callback(useradd_precallback)


def usermod_precallback(self, ldap, dn, entry_attrs, attrs_list, *keys, **options):

    add_missing_object_class(ldap, u'postfixbookmailforward', dn)
    return dn


user.user_mod.register_pre_callback(usermod_precallback)