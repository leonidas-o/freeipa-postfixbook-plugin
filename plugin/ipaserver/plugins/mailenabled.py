from ipaserver.plugins import user
from ipalib.parameters import Bool
from ipalib.text import _
from .baseldap import add_missing_object_class

user.user.takes_params += (
    Bool(
        'mailenabled?',
        cli_name='mailenabled',
        label=_('Mail enabled'),
        doc=_(
            'Whether or not a mail is enabled for this user (default is false).'
        ),
        autofill=False,
    ),
)

user.user.default_attributes.append('mailenabled')


def useradd_precallback(self, ldap, dn, entry_attrs, attrs_list, *keys, **options):

    add_missing_object_class(ldap, u'postfixbookmailaccount', dn, entry_attrs, update=False)
    return dn


user.user_add.register_pre_callback(useradd_precallback)


def usermod_precallback(self, ldap, dn, entry_attrs, attrs_list, *keys, **options):

    add_missing_object_class(ldap, u'postfixbookmailaccount', dn)
    return dn


user.user_mod.register_pre_callback(usermod_precallback)