from ipaserver.plugins import user
from ipalib.parameters import Bool
from ipalib import _
from .baseldap import add_missing_object_class

user.user.takes_params = user.user.takes_params + (
    Bool(
        "mailenabled?",
        cli_name="mailenabled",
        label=_("Mail enabled"),
        doc=_(
            "Whether or not a mail is enabled for this user (default is false)."
        ),
        default=False,
        autofill=False,
    ),
)

user.user.default_attributes.append("mailenabled")


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