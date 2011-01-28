Summary:	Library for manipulating Apple Property Lists
Summary(pl.UTF-8):	Biblioteka do manipulowania Apple Property Lists
Name:		libplist
Version:	1.3
Release:	4
License:	LGPL v2+
Group:		Libraries
Source0:	http://cloud.github.com/downloads/JonathanBeck/libplist/%{name}-%{version}.tar.bz2
# Source0-md5:	0f48f4da8ddba5d7e186307622bf2c62
URL:		http://www.libimobiledevice.org/
BuildRequires:	cmake >= 2.8.2-2
BuildRequires:	glib2-devel >= 1:2.14.1
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel >= 1:2.6.30
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	swig-python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Library for manipulating Apple Property Lists in binary and XML
format.

%description -l pl.UTF-8
Biblioteka do manipulowania Apple Property Lists w formacie binarnym i
XML.

%package devel
Summary:	Header files for libplist library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libplist
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.14.1
Requires:	libxml2-devel >= 1:2.6.30

%description devel
Header files for libplist library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libplist.

%package -n python-plist
Summary:	libplist Python bindings
Summary(pl.UTF-8):	Wiązania libplist dla Pythona
Group:		Development/Languages/Python

%description -n python-plist
libplist Python bindings.

%description -n python-plist -l pl.UTF-8
Wiązania libplist dla Pythona.

%prep
%setup -q

%build
install -d build
cd build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/plutil*
%attr(755,root,root) %{_libdir}/libplist++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libplist++.so.1
%attr(755,root,root) %{_libdir}/libplist.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libplist.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libplist++.so
%attr(755,root,root) %{_libdir}/libplist.so
%{_includedir}/plist
%{_pkgconfigdir}/libplist++.pc
%{_pkgconfigdir}/libplist.pc

%files -n python-plist
%defattr(644,root,root,755)
%dir %{py_sitedir}/plist
%attr(755,root,root) %{py_sitedir}/plist/_plist.so
%{py_sitedir}/plist/*.py[co]
