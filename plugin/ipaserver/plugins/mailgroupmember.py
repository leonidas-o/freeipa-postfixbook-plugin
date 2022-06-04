from ipaserver.plugins import user
from ipalib.parameters import Str
from ipalib.text import _
from .baseldap import add_missing_object_class

user.user.takes_params = user.user.takes_params + (
    Str(
        "mailgroupmember*",
        cli_name="mailgroupmember",
        label=_("Mail group member"),
        doc=_(
            "Name of a mail distribution list"
        ),
        autofill=False,
    ),
)

user.user.default_attributes.append("mailgroupmember")


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