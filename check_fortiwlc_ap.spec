# set package name
%define appName check_fortiwlc_ap

# destination/install folder
%define destdir /opt/monitoring/icinga

%define icingadest /etc/icinga2/conf.d/check_commands

Summary:   Icinga checkcommand AP connectin status
Name:      %{appName}
Version:   1.1
Release:   1%{?dist}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
License:  GPL
Source0:  check_fortiwlc_ap.py
Source1:  check_fortiwlc_ap.conf

# dependancies
Requires: python
Requires: pynag
Requires: python-requests

# require additional resources
Requires(pre): icinga2

Provides: %{name}

%description
Check command check_fortiwlc_ap is added
and configured to icinga2 .Check command check_fortiwlc_ap
connects to Fortinet WLC and returns status of AP.


%build

%prep

%install
# install application
rm -rf %{buildroot}

# put package contents to /opt/monitoring/icinga
install -p -D -m 755 %_sourcedir/check_fortiwlc_ap.py %{buildroot}%{destdir}/check_fortiwlc_ap.py
install -p -D -m 644 %_sourcedir/check_fortiwlc_ap.conf  %{buildroot}%{icingadest}/check_fortiwlc_ap.conf


%clean
rm -rf %{buildroot}

%preun

%postun

%files
%defattr(-,root,root,-)
%{icingadest}
%{destdir}

%changelog
* Wed Feb 06 2019 itfri2 - 20190206-1-1
- Change path of icinga2 check command

* Mon Jan 11 2019 itfri2 - 20190111-1
- First draft of the spec file

