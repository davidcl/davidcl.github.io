Name:           jhdf5
Version:        2.7
Release:        1%{?dist}
Summary:        Java HDF5 Object Package

Group:          Development/Libraries
License:        BSD with advertising
URL:            http://www.hdfgroup.org/hdf-java-html/
Source0:        http://www.hdfgroup.org/ftp/HDF5/hdf-java/src/hdf-java-%{version}-src.tar
Source1:        hdfview.xml
Source2:        hdfview.desktop

Patch1:         0001-add-a-generic-linux-host.patch
Patch2:         0002-add-H4_-prefix-to-constants.patch
Patch3:         0003-use-system-linker-for-shared-library.patch
Patch4:         0004-remove-writable-prefix-check.patch
Patch5:         0005-update-config.sub-and-config.guess.patch
Patch6:         0006-update-configure.patch
Patch7:         0007-clean-hdfview.sh.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  hdf5-devel
# to use config.sub and config.guess
BuildRequires:  rpm-build

Requires:       jpackage-utils
Requires:       java
Requires:       hdf5

%description
HDF is a versatile data model that can represent very complex data objects
and a wide variety of meta-data. It is a completely portable file format
with no limit on the number or size of data objects in the collection.

This Java package implements HDF5 data objects in an 
object-oriented form. It provides a common Java API for accessing HDF5 files.

%package devel
Summary: JHDF5 development files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: hdf5-devel

%description devel
JHDF5 development headers and libraries.

%package -n jhdf
Summary:        Java HDF Object Package
Group:          Development/Libraries

BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  hdf-devel

Requires:       jpackage-utils
Requires:       java

%description -n jhdf
HDF is a versatile data model that can represent very complex data objects
and a wide variety of meta-data. It is a completely portable file format
with no limit on the number or size of data objects in the collection.

This Java package implements HDF data objects in an 
object-oriented form. It provides a common Java API for accessing HDF files.

%package -n hdfview
Summary:        Java HDF Object viewer
Group:          Applications/File

BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  hdf5-devel
BuildRequires:  hdf-devel

# for convert
BuildRequires:  ImageMagick
# for desktop-file-install
BuildRequires:  desktop-file-utils

Requires:       jpackage-utils
Requires:       java
Requires:       hdf
Requires:       hdf5
Requires:       jhdf
Requires:       jhdf5

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

BuildArch:      noarch

%description -n hdfview
HDF is a versatile data model that can represent very complex data objects
and a wide variety of meta-data. It is a completely portable file format
with no limit on the number or size of data objects in the collection.

This package provides a HDF4/HDF5 viewer.


%prep
%setup -q -n hdf-java
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

# remove shipped jars
rm $(find -name \*.jar)

%build

%configure --with-jdk=%{java_home}/include,%{java_home}/lib \
        --with-hdf5=%{_includedir},%{_libdir} \
        --with-hdf4=%{_includedir}/hdf,%{_libdir}/hdf \
        --without-h4toh5 \
        --without-libsz \
        --with-libz=%{_includedir},%{_libdir} \
        --with-libjpeg=%{_includedir},%{_libdir}

# Make JNI (libjhdf.so libjhdf5.so) and
# make only required jars (not netcdf nor fits related packages)
make %{?_smp_mflags} natives
make %{?_smp_mflags} jhdf-packages jhdf5-packages \
                     jhdfobj-packages jhdfview-packages

%install

# jhdf5 jars
mkdir -p %{buildroot}%{_libdir}/jhdf5
install -pm 0644 lib/jhdf5.jar %{buildroot}%{_libdir}/jhdf5/jhdf5.jar
install -pm 0644 lib/jhdf5obj.jar %{buildroot}%{_libdir}/jhdf5/jhdf5obj.jar
install -pm 0644 lib/jhdfobj.jar %{buildroot}%{_libdir}/jhdf5/jhdfobj.jar

# jhdf5 lib
install -dm 755 %{buildroot}%{_libdir}/jhdf5
install -m 744 lib/linux/libjhdf5.so %{buildroot}%{_libdir}/jhdf5

# jhdf jars
mkdir -p %{buildroot}%{_libdir}/jhdf
install -pm 0644 lib/jhdf.jar %{buildroot}%{_libdir}/jhdf/jhdf.jar
install -pm 0644 lib/jhdf4obj.jar %{buildroot}%{_libdir}/jhdf/jhdf4obj.jar
install -pm 0644 lib/jhdfobj.jar %{buildroot}%{_libdir}/jhdf/jhdfobj.jar

# jhdf lib
install -dm 755 %{buildroot}%{_libdir}/jhdf
install -m 744 lib/linux/libjhdf.so %{buildroot}%{_libdir}/jhdf

# hdfview
mkdir -p %{buildroot}%{_javadir}
install -pm 0644 lib/jhdfview.jar %{buildroot}%{_javadir}/jhdfview.jar

mkdir -p %{buildroot}%{_bindir}
install -m 755 bin/hdfview.sh %{buildroot}%{_bindir}/hdfview

# Create and install hicolor icons.
for i in 16 22 32 48 ; do
  mkdir -p icons/${i}x${i}/apps

  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/mimetypes

  convert -resize ${i}x${i} ncsa/hdf/view/icons/hdf_large.gif \
    icons/${i}x${i}/apps/hdfview.png

  install -pm 0644 icons/${i}x${i}/apps/hdfview.png \
    %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/hdfview.png

  install -pm 0644 icons/${i}x${i}/apps/hdfview.png \
    %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/mimetypes/application-x-hdf.png

done

# .desktop file
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install                                    \
        --dir %{buildroot}%{_datadir}/applications      \
        %{SOURCE2}

# mime types
mkdir -p %{buildroot}%{_datadir}/mime/packages
install -p -D -m 644 %{SOURCE1} \
        %{buildroot}%{_datadir}/mime/packages/hdfview.xml

%clean
rm -rf %{buildroot}

%post
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%defattr(-,root,root,-)
%doc COPYING Readme.txt
%{_libdir}/jhdf5/*.jar
%attr(755,root,root) %{_libdir}/jhdf5/libjhdf5.so

%files -n jhdf
%defattr(-,root,root,-)
%doc COPYING Readme.txt
%{_libdir}/jhdf/*.jar
%attr(755,root,root) %{_libdir}/jhdf/libjhdf.so

%files -n hdfview
%defattr(-,root,root,-)
%{_bindir}/hdfview
%{_datadir}/applications/hdfview.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/mime/packages/hdfview.xml
%{_javadir}/jhdfview.jar
%doc COPYING Readme.txt
%doc docs 

%changelog
* Tue Aug 16 2011 Clément David <c.david86@gmail.com> - 2.7-1
- Initial packaging

