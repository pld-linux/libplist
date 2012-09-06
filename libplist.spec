#
# Conditional build:
%bcond_without	swig	# build with Swig
%bcond_without	cython	# build with Cython

Summary:	Library for manipulating Apple Property Lists
Summary(pl.UTF-8):	Biblioteka do manipulowania Apple Property Lists
Name:		libplist
Version:	1.8
Release:	4
License:	LGPL v2+
Group:		Libraries
#Source0-Download: http://www.libimobiledevice.org/
Source0:	http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	2a9e0258847d50f9760dc3ece25f4dc6
URL:		http://www.libimobiledevice.org/
BuildRequires:	cmake >= 2.8.2-2
BuildRequires:	glib2-devel >= 1:2.14.1
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel >= 1:2.6.30
BuildRequires:	pkgconfig
%{?with_cython:BuildRequires:	python-Cython}
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.600
%{?with_swig:BuildRequires:	swig-python}
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

%build
install -d build
cd build
%cmake \
	-DENABLE_SWIG=%{!?with_swig:NO}%{?with_swig:YES} \
	-DENABLE_CYTHON=%{!?with_cython:NO}%{?with_cython:YES} \
	../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

# cmake sucks, fix perms
%if %{with cython}
chmod a+x $RPM_BUILD_ROOT%{py_sitedir}/plist.so
cp -p cython/plist.pxd $RPM_BUILD_ROOT%{py_sitedir}
%endif
%if %{with swig}
chmod a+x $RPM_BUILD_ROOT%{py_sitedir}/plist/_plist.so
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
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

%if %{with cython} || %{with swig}
%files -n python-plist
%defattr(644,root,root,755)
%if %{with cython}
%attr(755,root,root) %{py_sitedir}/plist.so
%{py_sitedir}/plist.pxd
%endif
%if %{with swig}
%dir %{py_sitedir}/plist
%attr(755,root,root) %{py_sitedir}/plist/_plist.so
%{py_sitedir}/plist/*.py[co]
%endif
%endif
