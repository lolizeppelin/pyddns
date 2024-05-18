%include %{_rpmconfigdir}/macros.python

%global debug_package %{nil}
%define proj_name pyddns
%define _release 1

Name:           %{proj_name}
Version:        1.0.0
Release:        %{_release}%{?dist}
Summary:        ddns utils
Group:          Development/Libraries
License:        MIT
URL:            http://github.com/Lolizeppelin/%{proj_name}
Source0:        %{proj_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python >= 3.6
BuildRequires:  python-setuptools >= 40

Requires:       python >= 3.6
Requires:       python-netaddr >= 1.0.0
Requires:       python-psutil >= 5.0
Requires:       python-oslo-config >= 6.0.0
Requires:       python-oslo-stevedore >= 2.0.0
Requires:       python-requests >= 2.0.0


%description
A simple ddns util

%prep
%setup -q -n %{proj_name}-%{version}
rm -rf %{proj_name}.egg-info

%build
# build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
# generator config
%{__python} config-generator.py

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/%{proj_name}
mkdir -p %{buildroot}%{_sharedstatedir}/%{proj_name}

%{__install} -D -m 0640 -p etc/%{proj_name}/ddns.conf -t %{buildroot}%{_sysconfdir}/%{proj_name}
%{__install} -D -m 0644 -p ddns.service %{buildroot}%{_unitdir}/ddns.service
%{__install} -D -m 0644 -p ddns.timer %{buildroot}%{_unitdir}/ddns.timer

for l in bin/*;do
    %{__install} -D -m 0755 $l -t %{buildroot}%{_bindir}
done;


%pre
if [ "$1" = "1" ] ; then
    getent group ddns >/dev/null || groupadd -f -g 874 -r ddns
    if ! getent passwd ddns >/dev/null ; then
        if ! getent passwd 874 >/dev/null ; then
          useradd -r -u 874 -g ddns -M -s /sbin/nologin -c "Ddns process user" ddns
        else
          useradd -r -g ddns -M -s /sbin/nologin -c "Ddns process user" ddns
        fi
    fi
fi



%preun
systemctl stop ddns.timer

%postun
if [ "$1" = "0" ] ; then
    /usr/sbin/userdel ddns > /dev/null 2>&1
fi



%files
%defattr(-,root,root,-)
# dir
%dir  %{_sysconfdir}/%{proj_name}/plugins
%dir %{py_sitedir}/%{proj_name}-%{version}-*.egg-info/
%{py_sitedir}/%{proj_name}-%{version}-*.egg-info/*
# files
%{_bindir}/ddns
%{_unitdir}/ddns.service
%{_unitdir}/ddns.timer
%{py_sitedir}/%{proj_name}/*
%config(noreplace) %{_sysconfdir}/%{proj_name}/ddns.conf
%doc README.md
# private path
%defattr(-,ddns,ddns,-)
%dir %{_sharedstatedir}/%{proj_name}


%changelog
* Fri Mar 15 2019 Lolizeppelin <lolizeppelin@gmail.com> - 1.0.0
- Initial Package