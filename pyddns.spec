%include %{_rpmconfigdir}/macros.python

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
Source1:        %{name}-sysuser.conf
Source2:        %{name}.env
BuildArch:      noarch

BuildRequires:  python3 >= 3.6
BuildRequires:  python3-setuptools >= 40
BuildRequires:  python3-oslo-config >= 6.0.0

Requires:       python3 >= 3.6
Requires:       python-netaddr >= 1.0.0
Requires:       python3-psutil >= 5.0
Requires:       python3-oslo-config >= 6.0.0
Requires:       python3-oslo-stevedore >= 2.0.0
Requires:       python3-requests >= 2.0.0
Requires:       python3-tldextract >= 3.0.0


%description
A simple ddns util

%prep
%setup -q -n %{name}-%{version}
rm -rf %{name}.egg-info

%build
# build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
# generator config
%{__python} config-generator.py

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# folders
%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{name}
%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{name}/ddns
%{__mkdir} -p %{buildroot}%{_sharedstatedir}/%{name}

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
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_sysusersdir}/pyddns.conf
install -p -m 644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/pyddns


%preun
systemctl stop ddns.timer


%files
%defattr(-,root,root,-)
# dir
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/plugins
%dir %{py_sitedir}/%{name}-%{version}-*.egg-info/
%{py_sitedir}/%{name}-%{version}-*.egg-info/*
# files
%{_bindir}/ddns
%{_unitdir}/ddns.service
%{_unitdir}/ddns.timer
%{py_sitedir}/%{name}/*
%config(noreplace) %{_sysconfdir}/%{name}/ddns.conf
%doc README.md
%doc doc/*
# private path
%defattr(-,ddns,ddns,-)
%dir %{_sharedstatedir}/%{name}


%changelog
* Sat Mar 18 2024 Lolizeppelin <lolizeppelin@gmail.com> - 1.0.0
- Initial Package