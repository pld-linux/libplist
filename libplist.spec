#
# Conditional build:
%bcond_without	cython		# Python 3 module (Cython based)
%bcond_without	static_libs	# static libraries

Summary:	Library for manipulating Apple Property Lists
Summary(pl.UTF-8):	Biblioteka do manipulowania Apple Property Lists
Name:		libplist
Version:	2.7.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
# Source0Download: https://github.com/libimobiledevice/libplist/releases
Source0:	https://github.com/libimobiledevice/libplist/releases/download/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	cca9faafe9c7bbec75287bc2d8121fec
Patch0:		%{name}-sh.patch
Patch1:		%{name}-link.patch
URL:		https://libimobiledevice.org/
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.043
%if %{with cython}
BuildRequires:	python3-Cython >= 3.0.0
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	rpm-pythonprov
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Library for manipulating Apple Property Lists in binary and XML
format.

%description -l pl.UTF-8
Biblioteka do manipulowania Apple Property Lists w formacie binarnym i
XML.

%package devel
Summary:	Header file for libplist library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki libplist
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header file for libplist library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki libplist.

%package static
Summary:	Static libplist library
Summary(pl.UTF-8):	Statyczna biblioteka libplist
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libplist library.

%description static -l pl.UTF-8
Statyczna biblioteka libplist.

%package c++
Summary:	C++ binding for libplist library
Summary(pl.UTF-8):	Wiązanie C++ do biblioteki libplist
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description c++
C++ binding for libplist library.

%description c++ -l pl.UTF-8
Wiązanie C++ do biblioteki libplist.

%package c++-devel
Summary:	Header files for libplist++ library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libplist++
Group:		Development/Libraries
Requires:	%{name}-c++ = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	libstdc++-devel

%description c++-devel
Header files for libplist++ library.

%description c++-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libplist++.

%package c++-static
Summary:	Static libplist++ library
Summary(pl.UTF-8):	Statyczna biblioteka libplist++
Group:		Development/Libraries
Requires:	%{name}-c++-devel = %{version}-%{release}

%description c++-static
Static libplist++ library.

%description c++-static -l pl.UTF-8
Statyczna biblioteka libplist++.

%package -n python3-plist
Summary:	Python 3 bindings for libplist
Summary(pl.UTF-8):	Wiązania libplist dla Pythona 3
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-plist
Python 3 bindings for libplist.

%description -n python3-plist -l pl.UTF-8
Wiązania libplist dla Pythona 3.

%package -n python-plist-devel
Summary:	Cython header file for Python libplist binding
Summary(pl.UTF-8):	Plik nagłówkowy Cythona dla wiązania Pythona do biblioteki libplist
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	python-Cython >= 0.17.0

%description -n python-plist-devel
Cython header file for Python libplist binding.

%description -n python-plist-devel -l pl.UTF-8
Plik nagłówkowy Cythona dla wiązania Pythona do biblioteki libplist.

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1

touch cython/*.py[xh]

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	ac_cv_path_CYTHON=/usr/bin/cython3 \
	PYTHON=%{__python3} \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	%{!?with_cython:--without-cython}

%{__make}
# -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by .pc
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%if %{with cython}
#install -d $RPM_BUILD_ROOT%{_includedir}/plist/cython
#cp -p cython/plist.pxd $RPM_BUILD_ROOT%{_includedir}/plist/cython/plist.pxd
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/plist.la
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	c++ -p /sbin/ldconfig
%postun	c++ -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_bindir}/plistutil
%{_libdir}/libplist-2.0.so.*.*.*
%ghost %{_libdir}/libplist-2.0.so.4
%{_mandir}/man1/plistutil.1*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libplist-2.0.so
%dir %{_includedir}/plist
%{_includedir}/plist/plist.h
%{_pkgconfigdir}/libplist-2.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libplist-2.0.a
%endif

%files c++
%defattr(644,root,root,755)
%{_libdir}/libplist++-2.0.so.*.*.*
%ghost %{_libdir}/libplist++-2.0.so.4

%files c++-devel
%defattr(644,root,root,755)
%{_libdir}/libplist++-2.0.so
%{_includedir}/plist/Array.h
%{_includedir}/plist/Boolean.h
%{_includedir}/plist/Data.h
%{_includedir}/plist/Date.h
%{_includedir}/plist/Dictionary.h
%{_includedir}/plist/Integer.h
%{_includedir}/plist/Key.h
%{_includedir}/plist/Node.h
%{_includedir}/plist/Real.h
%{_includedir}/plist/String.h
%{_includedir}/plist/Structure.h
%{_includedir}/plist/Uid.h
%{_includedir}/plist/plist++.h
%{_pkgconfigdir}/libplist++-2.0.pc

%if %{with static_libs}
%files c++-static
%defattr(644,root,root,755)
%{_libdir}/libplist++-2.0.a
%endif

%if %{with cython}
%files -n python3-plist
%defattr(644,root,root,755)
%{py3_sitedir}/plist.so

%files -n python-plist-devel
%defattr(644,root,root,755)
%{_includedir}/plist/cython
%endif
