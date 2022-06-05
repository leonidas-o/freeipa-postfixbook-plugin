# freeipa-postfixbook-plugin

A module for FreeIPA to add 'postfix-book' schema.


<br><br>

## Development Environment

To setup a development environment, it's recommended to create a VM and install all freeIPA dependencies.
If the schema needs to be extended, bring it into a correct format (used `ol-schema-migrate.pl` script - https://directory.fedoraproject.org/docs/389ds/scripts.html)

### Dependencies
```bash
sudo su -
# freeIPA dependencies
dnf module enable idm:DL1
dnf module install idm:DL1/server
```

### Installation
```bash
sudo su -
# UI
mkdir /usr/share/ipa/ui/js/plugins/postfixbook
cd /usr/share/ipa/ui/js/plugins/postfixbook
# Either create one or all needed .js files
# Don't forget the main `postfixbook.js` which
# loads the other .js sub-plugins
vi postfixbook.js

# Schema
cd /usr/share/ipa/schema.d
vi 75-postfixbook.ldif

# CLI
# Either create one or all needed .py files
cd /usr/lib/python3.6/site-packages/ipaserver/plugins
vi mailenabled.py

# IPA Install
ipa-server-install
```


### Troubleshooting
While troubleshooting, you can update your plugin. To avoid any caching issues delete the cached python files:
```bash
cd /usr/lib/python3.6/site-packages/ipaserver/plugins
rm __pycache__/mail*
ipa-server-upgrade
# when checking __pycache__, mail* file(s) should be re-compiled
ls -la __pycache__
```

You can also uninstall FreeIPA and start again:
```bash
ipa-server-install --uninstall
ipa-server-install
```

Some useful commands to evaluate the extension process:
```bash
# login
kinit admin

# Check if schema was extended
# objectclasses
ldapsearch -o ldif-wrap=no -D 'cn=Directory Manager' -W -x -s base -b 'cn=schema' objectclasses | grep -i mail
# attributeTypes
ldapsearch -o ldif-wrap=no -D 'cn=Directory Manager' -W -x -s base -b 'cn=schema' attributetypes | grep -i mail

# Check if IPA sees the changes for your user
ipa user-show
# Return all entries
ldapsearch -o ldif-wrap=no -b "dc=MYDOMAIN,dc=com" "(objectclass=*)"
# Search For a Specific User
ldapsearch -b "dc=MYDOMAIN,dc=com" "(uid=myuser)"
ldapsearch -b "dc=MYDOMAIN,dc=com" "(cn=USERS_FIRSTNAME USERS_LASTNAME)"
```



<br><br>

## RPM Packages

Prepare VM for package build:
```bash
# build tools
dnf -y install rpm-build rpmdevtools
```

As regular user create the packages:
```bash
# setup env and build
mkdir -p ~/workspace/
cd workspace
git clone git@github.com:leonidas-o/freeipa-postfixbook-plugin.git
cd freeipa-postfixbook-plugin
git archive --prefix freeipa-postfixbook-plugin-0.9.0/ -o freeipa-postfixbook-plugin-0.9.0.tar.gz HEAD
rpmdev-setuptree
mv freeipa-postfixbook-plugin-0.9.0.tar.gz ~/rpmbuild/SOURCES/
rpmbuild -ba freeipa-postfixbook-plugin.spec
```


<br><br>

## Container Image

Prepare VM for container image build:
```bash
# podman
dnf -y install podman
```

To use this plugin an own container image should be created using the freeipa-server image as base:
```Dockerfile
FROM my-registry/freeipa/freeipa-server:rocky-8-4.9.8
# Copy rpm packages into container
COPY python3-ipa-postfixbook-server-0.9.0-1.el8.noarch.rpm \
    freeipa-postfixbook-plugin-0.9.0-1.el8.noarch.rpm \
    /tmp/
# Install rpm packages
# To use `dnf` you need `/data/etc/pki` and `/tmp/var/tmp`
RUN mkdir -p /data/etc/pki /tmp/var/tmp \
    && cp -rp /data-template/etc/pki/ca-trust /data/etc/pki \
    && dnf install -y /tmp/python3-ipa-postfixbook-server-0.9.0-1.el8.noarch.rpm \
    && dnf install -y /tmp/freeipa-postfixbook-plugin-0.9.0-1.el8.noarch.rpm \
    && dnf clean all
```

Copy RPM packages to a clean workspace directory with the above mentioned Dockerfile:
```bash
cd ~/workspace/freeipa-postfixbook-docker
cp ~/rpmbuild/RPMS/noarch/* .
# build the image
podman build --tls-verify=false -f Dockerfile -t my-registry/freeipa/freeipa-server:rocky-8-pfb-4.9.8 .
podman image ls
podman login --tls-verify=false my-registry
podman push --tls-verify=false my-registry/freeipa/freeipa-server:rocky-8-pfb-4.9.8
```
> If having `curl: (77) error setting certificate verify locations` error when using `dnf install`
> in a Dockerfile's `RUN` command, see: https://github.com/freeipa/freeipa-container/issues/305 and 
> https://github.com/freeipa/freeipa-container/issues/457 for further information and workarounds.



<br><br>

## Useful Links
- https://github.com/freeipa/freeipa/blob/master/doc/guide/guide.org#extending-existing-object%3E
- 