# Conditional build:
%bcond_with	tests		# build without tests
#
%define		kdeframever	5.111
%define		qtver		5.15.2
%define		kfname		kpeople
Summary:	Provides access to all contacts and the people who hold them
Name:		kf5-%{kfname}
Version:	5.111.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	752b237ce4e2ae195822078f8fdff23b
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
%if %{with tests}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
%endif
BuildRequires:	cmake >= 3.16
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	kf5-kcoreaddons-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Provides access to all contacts and the people who hold them.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%{?with_tests:%ninja_build -C build test}


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5 --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kfname}5.lang
%defattr(644,root,root,755)
%doc README.md
%{_datadir}/qlogging-categories5/kpeople.categories
%attr(755,root,root) %{_libdir}/libKF5People.so.*.*.*
%ghost %{_libdir}/libKF5People.so.5
%attr(755,root,root) %{_libdir}/libKF5PeopleBackend.so.*.*.*
%ghost %{_libdir}/libKF5PeopleBackend.so.5
%attr(755,root,root) %{_libdir}/libKF5PeopleWidgets.so.*.*.*
%ghost %{_libdir}/libKF5PeopleWidgets.so.5
%dir %{_libdir}/qt5/qml/org/kde/people
%{_libdir}/qt5/qml/org/kde/people/qmldir
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/people/libKF5PeopleDeclarative.so
%{_datadir}/qlogging-categories5/kpeople.renamecategories

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF5People.so
%{_libdir}/libKF5PeopleBackend.so
%{_libdir}/libKF5PeopleWidgets.so
%{_includedir}/KF5/KPeople
%{_libdir}/cmake/KF5People
%{_libdir}/qt5/mkspecs/modules/qt_KPeople*.pri
