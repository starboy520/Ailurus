%define name ailurus
%define version 10.03.2
%define unmangled_version 10.03.2
%define release 1

Summary: makes Linux easier to use
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://ailurus.googlecode.com/files/%{name}-%{unmangled_version}.tar.gz
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
* Help users study some Linux skills
* Install/remove some nice applications
* Enable/disable some third party repositories
* Display information about BIOS, motherboard, CPU and battery
* Show/Hide Computer, Home folder, Trash icon and Network icon on desktop
* Configure Nautilus thumbnail cache
* Configure Nautilus context menu
* Configure Window behavior
* Configure GNOME auto-start applications
* Show/Hide GNOME splash screen


%prep
%setup -q -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
sed -e 's/\.[0-9]$/&\*/' < INSTALLED_FILES > INSTALLED_FILES2 # fix manpage bug
mv INSTALLED_FILES2 INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog
* Mon Mar 22 2010 Homer Xing <homer.xing@gmail.com> 10.03.2-1
- Initial package

