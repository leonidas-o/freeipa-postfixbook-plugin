# freeipa-postfixbook-plugin

A module for FreeIPA to add 'postfix-book' schema.

## RPM Packages
To setup a development environment, it's recommended to create a VM and install all freeIPA dependencies.
If the schema needs to be extended e.g. with postfix-book.schema. Bring it into a correct format (used `ol-schema-migrate.pl` script - https://directory.fedoraproject.org/docs/389ds/scripts.html)

Setup VM:
```bash
sudo su -
# freeIPA dependencies
dnf module enable idm:DL1
dnf module install idm:DL1/server
# build tools
dnf -y install rpm-build rpmdevtools
# podman
dnf -y install podman
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


## Docker Image

To use this plugin an own docker image should be created using the freeipa-server image as base:
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
