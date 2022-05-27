# This spec file provides facilities to build FreeIPA external plugins for
# Fedora, RHEL (EPEL) and Rocky Linux. Support for external plugins was added to FreeIPA in
# 4.4.1 (and backported to RHEL in IdM version 4.4.0) For Fedora 27 or later we
# package both Python 2 and Python 3 versions in parallel. Fedora 27 defaults
# to Python 3.
#
# This includes the following components:
# - main package (freeipa-postfixbook-plugin) that holds LDAP schema and JS code
# - server packages for Python 2
# - server packages for Python 3

%global debug_package %{nil}
%global plugin_name postfixbook

%if 0%{?fedora} > 26 || 0%{?rhel} > 7
%global ipa_python3_sitelib %{python3_sitelib}
%endif

Name:           freeipa-%{plugin_name}-plugin
Version:        0.9.0
Release:        1%{?dist}
Summary:        A module for FreeIPA to add 'postfix-book' schema

BuildArch:      noarch

License:        GPL
URL:            https://github.com/leonidas-o/freeipa-%{plugin_name}-plugin
Source0:        freeipa-%{plugin_name}-plugin-%{version}.tar.gz

# Python3 support was added in Fedora 27 with FreeIPA 4.6
%if 0%{?fedora} > 26 || 0%{?rhel} > 7
BuildRequires: python3-devel
BuildRequires: python3-ipaserver >= 4.6.0
%endif


# Enforce using Python 3 in Fedora 27
%if 0%{?fedora} > 26 || 0%{?rhel} > 7
Requires(post): python3-ipa-%{plugin_name}-server
Requires: python3-ipa-%{plugin_name}-server
%endif

%description
A module for FreeIPA to add 'postfix-book' schema


%if 0%{?fedora} > 26 || 0%{?rhel} > 7
%package -n python3-ipa-%{plugin_name}-server
Summary: Server side of a module for FreeIPA to add 'postfix-book' schema
License:        GPL
Requires: python3-ipaserver

%description  -n python3-ipa-%{plugin_name}-server
A module for FreeIPA to add 'postfix-book' schema
This package adds server-side support for Python 3 version of FreeIPA

%endif

%prep
%autosetup

%build
touch debugfiles.list

%install
rm -rf $RPM_BUILD_ROOT
%__mkdir_p %buildroot/%_datadir/ipa/schema.d
%__mkdir_p %buildroot/%_datadir/ipa/ui/js/plugins/%{plugin_name}

%if 0%{?fedora} > 26 || 0%{?rhel} > 7
sitelibs="$sitelibs %{ipa_python3_sitelib}"
%endif

for s in $sitelibs ; do
    %__mkdir_p %buildroot/$s/ipaserver/plugins

    for j in $(find plugin/ipaserver/plugins -name '*.py') ; do
        %__cp $j %buildroot/$s/ipaserver/plugins
    done
    
done

for j in $(find plugin/schema.d -name '*.ldif') ; do
    %__cp $j %buildroot/%_datadir/ipa/schema.d
done

for j in $(find plugin/ui/ -name '*.js') ; do
    %__cp $j %buildroot/%_datadir/ipa/ui/js/plugins/%{plugin_name}
done

%posttrans
%if 0%{?fedora} > 26 || 0%{?rhel} > 7
ipa_interp=python3
%endif
$ipa_interp -c "import sys; from ipaserver.install import installutils; sys.exit(0 if installutils.is_ipa_configured() else 1);" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    /usr/sbin/ipa-server-upgrade --quiet >/dev/null || :
    /bin/systemctl is-enabled ipa.service >/dev/null 2>&1
    if [  $? -eq 0 ]; then
        /bin/systemctl restart ipa.service >/dev/null 2>&1 || :
    fi
fi

%files
%license LICENSE
%_datadir/ipa/schema.d/*
%_datadir/ipa/ui/js/plugins/%{plugin_name}/*


%if 0%{?fedora} > 26 || 0%{?rhel} > 7
%files -n python3-ipa-%{plugin_name}-server
%ipa_python3_sitelib/ipaserver/plugins/*
%endif


%changelog
* Wed May 25 2022 Leonid Orsulic 0.9.0
- Initial release
