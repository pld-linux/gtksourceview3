#
# Conditional build:
%bcond_with 	glade	# install glade catalog
#
Summary:	Text widget that extends the standard GTK+ 3.x
Summary(pl.UTF-8):	Widget tekstowy rozszerzający standardowy z GTK+ 3.x
Name:		gtksourceview3
Version:	3.2.1
Release:	1
License:	GPL v2+ and LGPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gtksourceview/3.2/gtksourceview-%{version}.tar.xz
# Source0-md5:	745f155e3cc15e567c8c7a32b6fc31e1
URL:		http://www.gnome.org/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel >= 0.17
BuildRequires:  glib2-devel >= 1:2.28
BuildRequires:	gnome-common >= 2.24.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtk-doc >= 1.11
BuildRequires:	intltool >= 0.40.0
%if %{with glade}
BuildRequires:	libgladeui-devel >= 3.9.0
%endif
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	pkgconfig
BuildRequires:	rpm-pythonprov
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.28.0
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

%description apidocs
GtkSourceView API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API GtkSourceView.

%package devel
Summary:	Header files for GtkSourceView
Summary(pl.UTF-8):	Pliki nagłówkowe dla GtkSourceView
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtk+3-devel >= 3.0.0
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
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description -n glade3-gtksourceview
Glade3 catalog entry for GtkSourceView library.

%prep
%setup -q -n gtksourceview-%{version}

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gtk-doc \
	--enable-static \
	--with-html-dir=%{_gtkdocdir} \
	%{__enable glade glade-catalog} \
	--enable-providers \
	--disable-silent-rules
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
%attr(755,root,root) %ghost %{_libdir}/libgtksourceview-3.0.so.0
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
