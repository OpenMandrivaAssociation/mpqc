%define	major		7
%define	libname		%mklibname SC %{major}
%define develname	%mklibname SC -d

Summary:	Ab-inito chemistry program
Name:		mpqc
Version:	2.3.1
Release:	15
License:	GPLv2+
Group:		Sciences/Chemistry
Source0:	http://prdownloads.sourceforge.net/mpqc/%name-%version.tar.bz2
Patch0:		mpqc-2.3.1-gentoo-respect-ldflags.patch
Patch1:		mpqc-2.3.1-gentoo-as-needed.patch
URL:		http://mpqc.org/
BuildRequires:	flex bison lapack-devel
BuildRequires:	gcc-gfortran tk blas-devel mpich2-devel doxygen
BuildRequires:	autoconf
BuildConflicts:	gcc3.3-g77

%description
MPQC is the Massively Parallel Quantum Chemistry Program. It computes 
properties of atoms and molecules from first principles using the time 
independent SchrÃ¶dinger equation. It runs on a wide range of architectures 
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

%package -n %{libname}
Summary:	Main libraries for %{name}
Group:		System/Libraries
Requires:	%{name}-data

%description -n %{libname}
This package contains the library needed to run programs dynamically linked 
with %libname, the scientific computing toolkit, based on mpqc computational 
chemistry package from Sandia Labs.

%package -n %{develname}
Summary:	Main libraries for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	libSC-devel
Provides:	SC-devel

%description -n %{develname}
This package contains the library needed to run programs dynamically linked
with %libname, the scientific computing toolkit, based on mpqc computational
chemistry package from Sandia Labs.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%define _disable_ld_no_undefined 1

sed -i -e 's,prefix\/lib,prefix\/%{_lib},g' configure.in
autoconf
%configure2_5x --enable-shared --enable-threads
make
cd doc
%make
make man1
make man3

%check
#make check
#make testbuild
#make testrun

%install
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

# inelegant workaround to fix sc-config
sed -i -e 's:libSCdft.la libSCscf.la libSCwfn.la:libSCwfn.la libSCdft.la libSCscf.la:' %{buildroot}%{_bindir}/sc-config

%multiarch_binaries %{buildroot}%{_bindir}/sc-config

# To fix unstripped-binary-or-object error
chmod 0755 %{buildroot}%{_libdir}/lib*.so.%{major}*

%files
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
%{_datadir}/%name

%files html
%doc doc/html

%files -n %{libname}
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%{_bindir}/sc-*
%{multiarch_bindir}/sc-config
%{_libdir}/lib*.so
%{_libdir}/*.a
%{_includedir}/*
%{_mandir}/man1/sc-*
%{_mandir}/man3/*

%files -n molrender
%{_bindir}/molrender
%{_bindir}/tkmolrender
%{_datadir}/applications/mandriva-%{name}.desktop
%{_mandir}/man1/molrender*

