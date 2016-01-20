# TODO
# - python3 package
# - split C++ lib?
#
# Conditional build:
%bcond_without	cython	# build with Cython

Summary:	Library for manipulating Apple Property Lists
Summary(pl.UTF-8):	Biblioteka do manipulowania Apple Property Lists
Name:		libplist
Version:	1.11
Release:	1
License:	LGPL v2+
Group:		Libraries
# Source0Download: http://www.libimobiledevice.org/
Source0:	http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	82de65f38cb2f0a9fd0839679b46072b
URL:		http://www.libimobiledevice.org/
BuildRequires:	glib2-devel >= 1:2.14.1
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel >= 1:2.6.30
BuildRequires:	pkgconfig
%if %{with cython}
BuildRequires:	python-Cython
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
%endif
BuildRequires:	rpmbuild(macros) >= 1.600
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
Requires:	%{name} = %{version}-%{release}

%description -n python-plist
libplist Python bindings.

%description -n python-plist -l pl.UTF-8
Wiązania libplist dla Pythona.

%prep
%setup -q

touch cython/*.py[xh]

%build
%configure \
	--disable-static \
	--disable-silent-rules \
	%{!?with_cython:--without-cython}
# make -j1 due:
# make[2]: *** No rule to make target '../src/libplist.la', needed by 'libplist++.la'.  Stop.
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by .pc
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%if %{with cython}
cp -p cython/plist.pxd $RPM_BUILD_ROOT%{py_sitedir}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/plist.la
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_bindir}/plistutil
%attr(755,root,root) %{_libdir}/libplist++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libplist++.so.2
%attr(755,root,root) %{_libdir}/libplist.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libplist.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libplist++.so
%attr(755,root,root) %{_libdir}/libplist.so
%{_includedir}/plist
%{_pkgconfigdir}/libplist++.pc
%{_pkgconfigdir}/libplist.pc

%if %{with cython}
%files -n python-plist
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/plist.so
%{py_sitedir}/plist.pxd
%endif
