from ipaserver.plugins import user
from ipalib.parameters import Str
from ipalib.text import _
from .baseldap import add_missing_object_class

user.user.takes_params += (
    Str(
        'mailalias+',
        cli_name='mailalias',
        label=_('Mail alias'),
        doc=_(
            'RFC822 Mailbox - mail alias'
        ),
        default="test@test.de",
        autofill=True,
        pattern='^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$',
        pattern_errmsg=''.join(
            'may only be "", '
            'or a valid email address (e.g. user@domain.com)'
        ),
    ),
)

user.user.default_attributes.append('mailalias')


def useradd_precallback(self, ldap, dn, entry_attrs, attrs_list, *keys, **options):

    add_missing_object_class(ldap, u'postfixbookmailaccount', dn, entry_attrs, update=False)
    add_missing_object_class(ldap, u'postfixbookmailforward', dn, entry_attrs, update=False)
    return dn


user.user_add.register_pre_callback(useradd_precallback)


def usermod_precallback(self, ldap, dn, entry_attrs, attrs_list, *keys, **options):

    add_missing_object_class(ldap, u'postfixbookmailaccount', dn)
    add_missing_object_class(ldap, u'postfixbookmailforward', dn)
    return dn


user.user_mod.register_pre_callback(usermod_precallback)