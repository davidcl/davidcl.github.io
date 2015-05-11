Name:           scilab
Version:        5.3.3
Release:        1%{?dist}
Summary:        Scientific software package for numerical computations

Group:          Applications/Engineering
License:        CeCILL
URL:            http://www.scilab.org/
Source0:        http://www.scilab.org/download/%{version}/scilab-%{version}-src.tar.gz

Patch1:         0001-add-Fedora-JNI-path.patch
Patch2:         0002-Remove-saxon-dependency-wrong-version.patch
Patch3:         0003-add-missing-xmlgraphics-commons.patch
Patch4:         0004-Remove-Xcos-dependencies-check.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Dependencies are extracted from :
# http://wiki.scilab.org/Dependencies%20of%20Scilab%205.X

# Mandatory
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran

## for dynamic link features
Requires:       gcc
Requires:       gcc-c++
Requires:       gcc-gfortran

# Core
BuildRequires:  libxml2-devel
BuildRequires:  pcre-devel
BuildRequires:  ncurses-devel

Requires:       pcre
Requires:       ncurses

# Optimized numerical libraries
# see http://wiki.scilab.org/Linalg%20performances
BuildRequires:  atlas-sse3-devel
Requires:       atlas-sse3

# GUI/Console
BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  ant

Requires:       jpackage-utils
Requires:       java

BuildRequires:  flexdock
BuildRequires:  jogl
BuildRequires:  mesa-libGL-devel

Requires:       flexdock
Requires:       jogl
Requires:       mesa-libGL

BuildRequires:  jrosetta
Requires:       jrosetta

BuildRequires:  apache-commons-logging
BuildRequires:  javahelp2
BuildRequires:  jlatexmath
BuildRequires:  jlatexmath-fop
BuildRequires:  jgraphx
BuildRequires:  fop
BuildRequires:  jeuclid
BuildRequires:  batik
BuildRequires:  xmlgraphics-commons

Requires:       apache-commons-logging
Requires:       javahelp2
Requires:       jlatexmath
Requires:       jlatexmath-fop
Requires:       jgraphx
Requires:       fop
Requires:       jeuclid
Requires:       batik
Requires:       xmlgraphics-commons

# TCL/TK features
BuildRequires:  tcl-devel
BuildRequires:  tk-devel

Requires:       tcl
Requires:       tk

# Modelica
BuildRequires:  ocaml

# PDF generation disabled (need saxon == 6.5)
# BuildRequires:  saxon
BuildRequires:  docbook-style-xsl

# All optional dependencies are needed to provide a full-featured Scilab
BuildRequires:  gettext-devel
BuildRequires:  pvm
BuildRequires:  fftw-devel
BuildRequires:  matio-devel
BuildRequires:  suitesparse-devel
BuildRequires:  hdf5-devel
BuildRequires:  jhdf5

BuildRequires:  gettext
BuildRequires:  pvm
BuildRequires:  fftw
BuildRequires:  matio
BuildRequires:  suitesparse
BuildRequires:  hdf5
BuildRequires:  jhdf5

# Specific dependencies for packaging purpose
BuildRequires:  desktop-file-utils
Requires:       %{name}-doc%{?_isa} = %{version}-%{release}

%description
Scilab is the free software for numerical computation providing a powerful
computing environment for engineering and scientific applications. It
includes hundreds of mathematical functions. It has a high level programming
language allowing access to advanced data structures, 2-D and 3-D graphical
functions.

%package devel
Group:          Applications/Engineering
License:        CeCILL

Summary:        Scientific software package for numerical computations (include files)

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Scilab is the free software for numerical computation providing a powerful
computing environment for engineering and scientific applications. It
includes hundreds of mathematical functions. It has a high level programming
language allowing access to advanced data structures, 2-D and 3-D graphical
functions.

This package provide include files for Scilab.

%package doc
Group:          Documentation
License:        CeCILL

Summary:        Scientific software package (documentation files)

%description doc
Scilab is the free software for numerical computation providing a powerful
computing environment for engineering and scientific applications. It
includes hundreds of mathematical functions. It has a high level programming
language allowing access to advanced data structures, 2-D and 3-D graphical
functions.

This package provide documentation files for Scilab.

%package tests
Group:          Applications/Engineering
License:        CeCILL

Summary:        Provides test files for Scilab

Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       testng

%description tests
Scilab is the free software for numerical computation providing a powerful
computing environment for engineering and scientific applications. It
includes hundreds of mathematical functions. It has a high level programming
language allowing access to advanced data structures, 2-D and 3-D graphical
functions.

This package provide test files for Scilab.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%configure PVM_ROOT=%{_datadir}/pvm3 \
           LDFLAGS="$LDFLAGS -L%{_libdir}/atlas-sse3"

make %{?_smp_mflags}
make %{?_smp_mflags} doc

%install
make %{?_smp_mflags} install DESTDIR=%{buildroot}
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
%find_lang %{name}

# Remove more advanced repl, user should use CLI options instead
rm -fr %{buildroot}%{_datadir}/applications/%{name}-*.desktop
# Remove la files
rm -fr %{buildroot}%{_libdir}/%{name}/*.la

# Add localized help files to scilab-doc.lang
# adapted from find-lang.sh
# always provide the english help to handle missing localized help pages
find %{buildroot}%{_datadir}/%{name}/modules/helptools/jar -type f -o -type l|sed '
s:'"%{buildroot}"'::
s:\(.*/'"%{name}"'_\)\([^\._]\+\)\(.*\.jar$\):%lang(\2) \1\2\3:
s:^\([^%].*\)::
s:%lang(en) ::
s:%lang(C) ::
/^$/d' >%{name}-doc.lang

# Fail with GTK look and feel error (may be due to openjdk)
#%check
#make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README_Unix COPYING license.txt
%{_bindir}/*
%{_libdir}/%{name}/*.so
%{_libdir}/%{name}/*.so.*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
# part of scilab-devel
%exclude %{_datadir}/%{name}/contrib
%exclude %{_datadir}/%{name}/tools
%exclude %{_datadir}/%{name}/modules/*/macros/*.sci
# part of scilab-doc
%exclude %{_datadir}/%{name}/modules/helptools/jar/%{name}_*.jar
%exclude %{_datadir}/%{name}/modules/*/examples
%exclude %{_datadir}/%{name}/modules/*/help
%exclude %{_datadir}/%{name}/modules/*/javadoc
# part of scilab-tests
%exclude %{_datadir}/%{name}/modules/*/tests

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/%{name}/contrib
%{_datadir}/%{name}/tools
%{_datadir}/%{name}/modules/*/macros/*.sci

%files doc -f %{name}-doc.lang
%defattr(-,root,root,-)
%{_datadir}/doc/%{name}-*
%{_datadir}/%{name}/modules/*/examples
%{_datadir}/%{name}/modules/*/help
%{_datadir}/%{name}/modules/*/javadoc

%files tests
%defattr(-,root,root,-)
%{_datadir}/%{name}/modules/*/tests

%changelog
* Thu Sep  8 2011 <c.david86@gmail.com> 5.3.3-1
- Update to scilab 5.3.3
- Remove not necessary patches
- Build a full featured version (with all dependencies)
- Split tests from main package
* Sat Nov 14 2009 <mycae(a!t)yahoo.com> 5.2.0-1.beta1
- Update to scilab 5.2.0-beta-1
* Thu Mar 05 2009 <mycae(a!t)yahoo.com> 5.1-2
- Added patch to fix scilab bug 4052
- Minor changes to de-lint spec file
- Change java-1.6 to java for requires & buildrequires 
- Move .so back to main, as scilab 5.1 won't run without them (many java exceptions)
- Patch scilab binary launcher script to correct lib search dirs
* Sat Feb 21 2009 <mycae(a!t)yahoo.com> 5.1-1
- Update to new scilab release (5.1)
- Add more build requires
- Use fedora sparse libraries
* Sat Jan 03 2009 <mycae(a!t)yahoo.com> 5.0.3-2
- Fix up Requires & BuildRequires
- Work around static lib installation (disable static libs issue?)
- Trash zero length files during install
- Added missing ldconfig in post/postun
- Fix up file ownership to prevent duplicate owners
- Fix up file permissions (644->755) on executable scripts
- Fix so .so files are in -devel, .so.* are in main
* Mon Dec 29 2008 <mycae(a!t)yahoo.com> 5.0.3-1
- Update to new scilab release (5.0.3)
- Add devel section for .h files
- Disable static libs
- Fix documentation build (added jeuclid-core)
- Fix many rpmlint warnings (devel mainly.)
* Sun Nov 23 2008 <mycae(a!t)yahoo.com> 5.0.1-2
- Fix files section
- Remove pkg-config file.
- remove windows_tools dir
- Add parallel building for those with smp_mflags
- Set make target to "all" rather than blank
- Add doc files
* Sat Nov 22 2008 <mycae(a!t)yahoo.com> 5.0.1-1
- First release 

