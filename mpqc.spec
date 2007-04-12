%define name 	mpqc
%define version 2.3.1
%define release %mkrel 1

%define	major	7
%define	libname	%mklibname SC %major

%define __libtoolize /bin/true

Summary: 	Ab-inito chemistry program
Name: 		%name
Version: 	%version
Release: 	%release
License: 	GPL
Group: 		Sciences/Chemistry
Source: 	http://prdownloads.sourceforge.net/mpqc/%name-%version.tar.bz2
URL: 		http://mpqc.org/
BuildRoot: 	%{_tmppath}/%name-buildroot
BuildRequires: 	flex bison liblapack-devel liblapack gcc-gfortran tk libblas-devel mpich2-devel doxygen automake1.9
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

%package -n %libname-devel
Summary:        Main libraries for %name
Group:          Development/C++
Requires:	%libname = %version
Provides:	libSC-devel

%description -n %{libname}-devel
This package contains the library needed to run programs dynamically linked
with %libname, the scientific computing toolkit, based on mpqc computational
chemistry package from Sandia Labs.

%prep
%setup -q

%build
%configure2_5x --enable-shared --enable-threads
%make
cd doc
make
make man1
make man3

%install
rm -fr %buildroot
echo hello
make install installroot=$RPM_BUILD_ROOT
make install_devel installroot=$RPM_BUILD_ROOT
cp -r doc/man %buildroot/%_datadir

# Menu
mkdir -p %buildroot/%{_menudir}
cat > %buildroot/%{_menudir}/molrender <<EOF
?package(molrender): command="%{_bindir}/tkmolrender" needs="X11" \
icon="sciences_section.png" section="Applications/Sciences/Chemistry" \
title="Molrender" longtitle="Molecular Rendering GUI" xdg="true"
EOF

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Molrender
Comment=%{Summary}
Exec=%{_bindir}/tkmolrender
Icon=sciences_section
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Sciences-Chemistry;Science;Chemistry;
Encoding=UTF-8
EOF

%multiarch_binaries %buildroot%_bindir/sc-config

%clean
rm -rf %buildroot

%post -n molrender
%{update_menus}

%postun -n molrender
%{clean_menus}

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc CHANGES CITATION COPYING COPYING.LIB LICENSE README
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
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
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
%{_menudir}/molrender
%{_datadir}/applications/mandriva-%{name}.desktop
%{_mandir}/man1/molrender*



