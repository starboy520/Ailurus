%define name ailurus
%define version 10.05.91
%define unmangled_version 10.05.91
%define release 1
%define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")

Summary: makes Linux easier to use
Name: %{name}
Version: %{version}
Release: %{release}
Source: http://homerxing.fedorapeople.org/%{name}-%{unmangled_version}.tar.gz
License: GPLv2+
Group: Applications/System
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Homer Xing <homer.xing@gmail.com>
Requires: python pygtk2 notify-python vte rpm-python pygobject2 dbus-python wget unzip xterm
Url: http://ailurus.googlecode.com/
BuildRequires: python python-devel python-distutils-extra intltool sed

%description
Ailurus is an application which makes Linux easier to use.

Features:
* Help users learn some Linux skills
* Install some nice applications
* Display basic hardware information
* Clean APT/YUM cache
* Backup and recover APT/YUM status
* Change GNOME settings 

%prep
%setup -q -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install -O1 --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{python_sitelib}/ailurus/
%{_bindir}/ailurus
%doc %{_mandir}/man1/ailurus.1*
%{_datadir}/applications/ailurus.desktop
%{_datadir}/ailurus/
%{_datadir}/dbus-1/system-services/cn.ailurus.service
%{_sysconfdir}/dbus-1/system.d/cn.ailurus.conf
%{_datadir}/PolicyKit/policy/cn.ailurus.policy
%{_datadir}/polkit-1/actions/cn.ailurus.policy
%{_datadir}/locale/*/LC_MESSAGES/ailurus.mo
%{_datadir}/omf/ailurus
%{python_sitelib}/ailurus*.egg-info

%changelog
* Thu May 27 2010 Homer Xing <homer.xing@gmail.com> 10.05.91-1
- Initial package
