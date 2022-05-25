from ipaserver.plugins import user
from ipalib.parameters import Int
from ipalib.text import _

user.user.takes_params = user.user.takes_params + (
    Int(
        "mailgidnumber?",
        cli_name="mailgidnumber",
        label=_("Mail GID number"),
        doc=_(
            "GID required to access the mailbox"
        ),
        autofill=False,
    ),
)

user.user.default_attributes.append("mailgidnumber")


# pylint: disable-msg=unused-argument,invalid-name,line-too-long
def useradd_precallback(self, ldap, dn, entry, attrs_list, *keys, **options):
    
    entry["objectclass"].append("postfixbookmailaccount")
    return dn

user.user_add.register_pre_callback(useradd_precallback)


# pylint: disable-msg=unused-argument,invalid-name,line-too-long
def usermod_precallback(self, ldap, dn, entry, attrs_list, *keys, **options):
    
    if "objectclass" not in entry.keys():
        old_entry = ldap.get_entry(dn, ["objectclass"])
        entry["objectclass"] = old_entry["objectclass"]
    entry["objectclass"].append("postfixbookmailaccount")
    return dn


user.user_mod.register_pre_callback(usermod_precallback)