#
# Conditional build:
%bcond_without	cython		# Python modules (Cython based)
%bcond_without	python3		# Python 3 module
%bcond_without	static_libs	# static libraries

%if %{without cython}
%undefine	with_python3
%endif
Summary:	Library for manipulating Apple Property Lists
Summary(pl.UTF-8):	Biblioteka do manipulowania Apple Property Lists
Name:		libplist
Version:	2.2.0
Release:	4
License:	LGPL v2.1+
Group:		Libraries
# Source0Download: https://libimobiledevice.org/
Source0:	https://github.com/libimobiledevice/libplist/releases/download/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	63cc49401521662c94cd4107898c744c
Patch0:		%{name}-sh.patch
URL:		https://libimobiledevice.org/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.600
%if %{with cython}
BuildRequires:	python-Cython >= 0.17.0
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	python-modules >= 1:2.3
%if %{with python3}
BuildRequires:	python3-Cython >= 0.17.0
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
%endif
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

%package -n python-plist
Summary:	Python 2 bindings for libplist
Summary(pl.UTF-8):	Wiązania libplist dla Pythona 2
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-plist
Python 2 bindings for libplist.

%description -n python-plist -l pl.UTF-8
Wiązania libplist dla Pythona 2.

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
%patch0 -p1

touch cython/*.py[xh]

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
install -d build
cd build
../%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	%{!?with_cython:--without-cython}

# make -j1 due:
# make[2]: *** No rule to make target '../src/libplist.la', needed by 'libplist++.la'.  Stop.
%{__make} -j1
cd ..

%if %{with python3}
topdir=$(pwd)
install -d build-py3
cd build-py3
../%configure \
	PYTHON=%{__python3} \
	--disable-silent-rules

%{__make} -C cython \
	top_builddir="${topdir}/build"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by .pc
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%if %{with cython}
install -d $RPM_BUILD_ROOT%{_includedir}/plist/cython
cp -p cython/plist.pxd $RPM_BUILD_ROOT%{_includedir}/plist/cython/plist.pxd
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/plist.la \
	%{?with_static_libs:$RPM_BUILD_ROOT%{py_sitedir}/plist.a}

%if %{with python3}
%{__make} -C build-py3/cython install \
	DESTDIR=$RPM_BUILD_ROOT \
	top_builddir="$(pwd)/build"

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/plist.la \
	%{?with_static_libs:$RPM_BUILD_ROOT%{py3_sitedir}/plist.a}
%endif
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
%attr(755,root,root) %{_libdir}/libplist-2.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libplist-2.0.so.3
%{_mandir}/man1/plistutil.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libplist-2.0.so
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
%attr(755,root,root) %{_libdir}/libplist++-2.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libplist++-2.0.so.3

%files c++-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libplist++-2.0.so
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
%files -n python-plist
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/plist.so

%if %{with cython}
%files -n python3-plist
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/plist.so
%endif

%files -n python-plist-devel
%defattr(644,root,root,755)
%{_includedir}/plist/cython
%endif
