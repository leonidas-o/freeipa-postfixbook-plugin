from ipaserver.plugins import user
from ipalib.parameters import Str
from ipalib.text import _
from .baseldap import add_missing_object_class

user.user.takes_params += (
    Str(
        'mailquota*',
        cli_name='mailquota',
        label=_('Mail quota'),
        doc=_(
            'Mail quota limit in kilobytes'
            'Allowed values are "", "none",'
            '"default", e.g. "1024 KB" (default is "default").'
        ),
        default='',
        autofill=False,
        pattern='^(|default|none|[0-9]+ KB)$',
        pattern_errmsg=''.join(
            'may only be "", "none", '
            '"default" or a number of kilobytes (e.g. 1024 KB)'
        ),
    ),
)

user.user.default_attributes.append('mailquota')


def useradd_precallback(self, ldap, dn, entry_attrs, attrs_list, *keys, **options):

    add_missing_object_class(ldap, u'postfixbookmailaccount', dn, entry_attrs, update=False)
    return dn


user.user_add.register_pre_callback(useradd_precallback)


def usermod_precallback(self, ldap, dn, entry_attrs, attrs_list, *keys, **options):

    add_missing_object_class(ldap, u'postfixbookmailaccount', dn)
    return dn


user.user_mod.register_pre_callback(usermod_precallback)