#
# Conditional build:
%bcond_with 	glade	# install glade catalog
%bcond_without	vala	# do not build Vala API

Summary:	Text widget that extends the standard GTK+ 3.x
Summary(pl.UTF-8):	Widget tekstowy rozszerzający standardowy z GTK+ 3.x
Name:		gtksourceview3
Version:	3.24.11
Release:	4
License:	LGPL v2+ (library), GPL v2+ (some language specs files)
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gtksourceview/3.24/gtksourceview-%{version}.tar.xz
# Source0-md5:	b748da426a7d64e1304f0c532b0f2a67
Patch0:		build.patch
URL:		https://wiki.gnome.org/Projects/GtkSourceView
BuildRequires:	autoconf >= 2.64
BuildRequires:	autoconf-archive >= 2015.09.25
BuildRequires:	automake >= 1:1.13
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.19.4
BuildRequires:	glib2-devel >= 1:2.48.0
BuildRequires:	gobject-introspection-devel >= 1.42.0
BuildRequires:	gtk+3-devel >= 3.20.0
BuildRequires:	gtk-doc >= 1.25
BuildRequires:	itstool
%if %{with glade}
BuildRequires:	libgladeui-devel >= 3.9.0
%endif
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	pkgconfig
BuildRequires:	rpm-pythonprov
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
BuildRequires:	xz
Requires:	glib2 >= 1:2.48.0
Requires:	gtk+3 >= 3.20.0
Requires:	libxml2 >= 1:2.6.31
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GtkSourceView is a text widget that extends the standard GTK+ 3.x text
widget GtkTextView. It improves GtkTextView by implementing syntax
highlighting and other features typical of a source editor.

%description -l pl.UTF-8
GtkSourceView to widget tekstowy rozszerzający standardowy widget
tekstowy GtkTextView z GTK+ 3.x. Ulepsza GtkTextView poprzez
zaimplementowanie podświetlania składni i innych możliwości typowych
dla edytora źródeł.

%package apidocs
Summary:	GtkSourceView API documentation
Summary(pl.UTF-8):	Dokumentacja API GtkSourceView
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
GtkSourceView API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API GtkSourceView.

%package devel
Summary:	Header files for GtkSourceView
Summary(pl.UTF-8):	Pliki nagłówkowe dla GtkSourceView
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.48.0
Requires:	gtk+3-devel >= 3.20.0
Requires:	libxml2-devel >= 1:2.6.31

%description devel
Header files for GtkSourceView.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla GtkSourceView.

%package static
Summary:	Static GtkSourceView library
Summary(pl.UTF-8):	Statyczna biblioteka GtkSourceView
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GtkSourceView library.

%description static -l pl.UTF-8
Statyczna biblioteka GtkSourceView.

%package -n glade3-gtksourceview
Summary:	Glade3 catalog entry for GtkSourceView library
Summary(pl.UTF-8):	Wpis katalogu Glade3 dla biblioteki GtkSourceView
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	libgladeui >= 3.9.0

%description -n glade3-gtksourceview
Glade3 catalog entry for GtkSourceView library.

%description -n glade3-gtksourceview -l pl.UTF-8
Wpis katalogu Glade3 dla biblioteki GtkSourceView.

%package -n vala-gtksourceview
Summary:	GtkSourceView API for Vala language
Summary(pl.UTF-8):	API GtkSourceView dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
BuildArch:	noarch

%description -n vala-gtksourceview
GtkSourceView API for Vala language.

%description -n vala-gtksourceview -l pl.UTF-8
API GtkSourceView dla języka Vala.

%prep
%setup -q -n gtksourceview-%{version}
%patch -P0 -p1

# force new version from autoconf-archive (original one uses non-POSIX ${V:N} syntax)
%{__rm} m4/ax_compiler_flags_cflags.m4

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable glade glade-catalog} \
	--enable-gtk-doc \
	--disable-silent-rules \
	--enable-static \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang gtksourceview-3.0

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f gtksourceview-3.0.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgtksourceview-3.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgtksourceview-3.0.so.1
%{_datadir}/gtksourceview-3.0
%{_libdir}/girepository-1.0/GtkSource-3.0.typelib

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gtksourceview-3.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgtksourceview-3.0.so
%{_includedir}/gtksourceview-3.0
%{_pkgconfigdir}/gtksourceview-3.0.pc
%{_datadir}/gir-1.0/GtkSource-3.0.gir

%files static
%defattr(644,root,root,755)
%{_libdir}/libgtksourceview-3.0.a

%if %{with glade}
%files -n glade3-gtksourceview
%defattr(644,root,root,755)
%{_datadir}/glade3/catalogs/gtksourceview.xml
%endif

%if %{with vala}
%files -n vala-gtksourceview
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gtksourceview-3.0.deps
%{_datadir}/vala/vapi/gtksourceview-3.0.vapi
%endif
