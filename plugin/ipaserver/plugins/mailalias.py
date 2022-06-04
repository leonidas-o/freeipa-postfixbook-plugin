from ipaserver.plugins import user
from ipalib.parameters import Str
from ipalib.text import _
from .baseldap import add_missing_object_class

user.user.takes_params = user.user.takes_params + (
    Str(
        "mailalias*",
        cli_name="mailalias",
        label=_("Mail alias"),
        doc=_(
            "RFC822 Mailbox - mail alias"
        ),
        autofill=False,
        pattern="^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$",
        pattern_errmsg="".join(
            'may only be "", '
            'or a valid email address (e.g. user@domain.com)'
        ),
    ),
)

user.user.default_attributes.append("mailalias")


# pylint: disable-msg=unused-argument,invalid-name,line-too-long
def useradd_precallback(self, ldap, dn, entry, attrs_list, *keys, **options):

    #entry["objectclass"].append("postfixbookmailaccount")
    add_missing_object_class(ldap, 'postfixbookmailaccount', dn)
    return dn


user.user_add.register_pre_callback(useradd_precallback)


# pylint: disable-msg=unused-argument,invalid-name,line-too-long
def usermod_precallback(self, ldap, dn, entry, attrs_list, *keys, **options):

    #if "objectclass" not in entry.keys():
    #    old_entry = ldap.get_entry(dn, ["objectclass"])
    #    entry["objectclass"] = old_entry["objectclass"]
    #entry["objectclass"].append("postfixbookmailaccount")
    add_missing_object_class(ldap, 'postfixbookmailaccount', dn)
    return dn


user.user_mod.register_pre_callback(usermod_precallback)