%define name 	mpqc
%define version 2.3.1
%define release %mkrel 7

%define	major		7
%define	libname		%mklibname SC %major
%define develname	%mklibname SC -d


Summary: 	Ab-inito chemistry program
Name: 		%name
Version: 	%version
Release: 	%release
License: 	GPL
Group: 		Sciences/Chemistry
Source: 	http://prdownloads.sourceforge.net/mpqc/%name-%version.tar.bz2
URL: 		http://mpqc.org/
Patch0:		mpqc-2.3.1-linkage.patch
BuildRoot: 	%{_tmppath}/%name-buildroot
BuildRequires: 	flex bison lapack-devel
BuildRequires:	gcc-gfortran tk blas-devel mpich2-devel doxygen
BuildRequires:	autoconf
BuildConflicts:	gcc3.3-g77

%description
MPQC is the Massively Parallel Quantum Chemistry Program. It computes 
properties of atoms and molecules from first principles using the time 
independent Schrödinger equation. It runs on a wide range of architectures 
ranging from individual workstations to symmetric multiprocessors to 
massively parallel computers. Its design is object oriented, using the C++ 
programming language.

If you want to use this program on a distributed (parallel) network, you'll 
also have to install the libmpich package.

%package data
Summary:	Atom info and basis sets from MPQC
Group:		Sciences/Chemistry

%description data
Atom info and basis sets from MPQC.

%package html
Summary:	HTML documentation for MPQC
Group:		Sciences/Chemistry

%description html
This package contains the full documentation for MPQC that can be viewed
with a graphical browser like Mozilla.
 
%package -n molrender
Summary:	Graphical molecular rendering program
Group:		Sciences/Chemistry

%description -n molrender
This package graphically renders 3D molecules based on the output of 
computational chemistry packages like mpqc.

%package -n %libname
Summary:	Main libraries for %name
Group:		System/Libraries
Requires:	%name-data

%description -n %{libname}
This package contains the library needed to run programs dynamically linked 
with %libname, the scientific computing toolkit, based on mpqc computational 
chemistry package from Sandia Labs.

%package -n %{develname}
Summary:        Main libraries for %name
Group:          Development/C++
Requires:	%libname = %version
Provides:	libSC-devel
Provides:	SC-devel
Obsoletes:	%{mklibname SC 7 -d}

%description -n %{develname}
This package contains the library needed to run programs dynamically linked
with %libname, the scientific computing toolkit, based on mpqc computational
chemistry package from Sandia Labs.

%prep
%setup -q
%patch0 -p0 -b .link

%build
sed -i -e 's,prefix\/lib,prefix\/%{_lib},g' configure.in
autoconf
%configure2_5x --enable-shared --enable-threads
%make
cd doc
make
make man1
make man3

%install
rm -fr %{buildroot}
echo hello
make install installroot=%{buildroot}
make install_devel installroot=%{buildroot}
cp -r doc/man %buildroot/%{_datadir}

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Molrender
Comment=Ab-inito chemistry program
Exec=%{_bindir}/tkmolrender
Icon=sciences_section
Terminal=false
Type=Application
Categories=Science;Chemistry;
EOF

%multiarch_binaries %{buildroot}%{_bindir}/sc-config

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n molrender
%{update_menus}
%endif

%if %mdkversion < 200900
%postun -n molrender
%{clean_menus}
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc CHANGES CITATION LICENSE README
%{_bindir}/mpqc
%{_bindir}/chkmpqcout
%{_bindir}/scls
%{_bindir}/scpr
%{_bindir}/*run
%{_mandir}/man1/mpqc*
%{_mandir}/man1/scls*
%{_mandir}/man1/scpr*

%files data
%defattr(-,root,root)
%{_datadir}/%name

%files html
%defattr(-,root,root)
%doc doc/html

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_bindir}/sc-*
%{multiarch_bindir}/sc-config
%{_libdir}/lib*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_includedir}/*
%{_mandir}/man1/sc-*
%{_mandir}/man3/*

%files -n molrender
%defattr(-,root,root)
%{_bindir}/molrender
%{_bindir}/tkmolrender
%{_datadir}/applications/mandriva-%{name}.desktop
%{_mandir}/man1/molrender*
