%global debug_package %{nil}
%define _release 1

Name:           pyddns
Version:        1.0.0
Release:        %{_release}%{?dist}
Summary:        ddns utils
Group:          Development/Libraries
License:        MIT
URL:            http://github.com/Lolizeppelin/%{name}
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3 >= 3.6
BuildRequires:  python3-setuptools >= 40
BuildRequires:  python3-oslo-config >= 6.0.0

Requires:       python3 >= 3.6
Requires:       python3-netaddr >= 0.10.0
Requires:       python3-psutil >= 5.0
Requires:       python3-oslo-config >= 6.0.0
Requires:       python3-stevedore >= 2.0.0
Requires:       python3-requests >= 2.0.0
Requires:       python3-tldextract >= 3.0.0


%description
A simple ddns util

%prep
%setup -q -n %{name}-%{version}
rm -rf %{name}.egg-info

%build
sed -i '0,/VERSION/s//%{version}/' setup.cfg
sed -i '0,/VERSION/s//%{version}/' PKG-INFO
# build
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
# generator config
%{__python3} config-generator.py

%install
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

# folders
%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{name}
%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{name}/ddns

# config file
%{__install} -D -m 0640 -p etc/%{name}/ddns.conf -t %{buildroot}%{_sysconfdir}/%{name}
%{__install} -D -m 0640 -p etc/%{name}/plugins/dnspod.conf -t %{buildroot}%{_sysconfdir}/%{name}/plugins

# service file
%{__install} -D -m 0644 -p ddns.service %{buildroot}%{_unitdir}/ddns.service
%{__install} -D -m 0644 -p ddns.timer %{buildroot}%{_unitdir}/ddns.timer

# bin file
for l in bin/*;do
    %{__install} -D -m 0755 $l -t %{buildroot}%{_bindir}
done;

# sys user
install -p -m 644 -D %{name}.env %{buildroot}%{_sysconfdir}/sysconfig/pyddns


%pre
if [ "$1" = "1" ] ; then
    useradd -r -M -s /sbin/nologin -d /var/lib/pyddns -c "ddns account" ddns > /dev/null 2>&1
fi


%preun
systemctl stop ddns.timer


%postun
if [ "$1" = "0" ] ; then
    /usr/sbin/userdel ddns > /dev/null 2>&1
fi


%files
%defattr(-,ddns,ddns,-)
# dir
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/plugins
# config
%config(noreplace) %{_sysconfdir}/%{name}/ddns.conf
%config(noreplace) %{_sysconfdir}/%{name}/plugins/dnspod.conf
%config(noreplace) %{_sysconfdir}/sysconfig/pyddns
%defattr(-,root,root,-)
%dir %{python3_sitelib}/%{name}-%{version}-*.egg-info/
%{python3_sitelib}/%{name}-%{version}-*.egg-info/*
# files
%{_bindir}/pyddns
%{_unitdir}/ddns.service
%{_unitdir}/ddns.timer
%{python3_sitelib}/%{name}/*
%doc README.md
%doc doc/*


%changelog
* Wed May 22 2024 Lolizeppelin <lolizeppelin@gmail.com> - 1.0.0
- Initial Package