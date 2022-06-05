from ipaserver.plugins import user
from ipalib.parameters import Int
from ipalib.text import _
from .baseldap import add_missing_object_class

user.user.takes_params += (
    Int(
        'mailgidnumber?',
        cli_name='mailgidnumber',
        label=_('Mail GID number'),
        doc=_(
            'GID required to access the mailbox'
        ),
        autofill=False,
    ),
)

user.user.default_attributes.append('mailgidnumber')


def useradd_precallback(self, ldap, dn, entry_attrs, attrs_list, *keys, **options):
    
    add_missing_object_class(ldap, u'postfixbookmailaccount', dn, entry_attrs, update=False)
    return dn


user.user_add.register_pre_callback(useradd_precallback)


def usermod_precallback(self, ldap, dn, entry_attrs, attrs_list, *keys, **options):
    
    add_missing_object_class(ldap, u'postfixbookmailaccount', dn)
    return dn


user.user_mod.register_pre_callback(usermod_precallback)