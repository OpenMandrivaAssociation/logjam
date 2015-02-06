%define use_xmms 0

Name:		logjam
Version:	4.6.2
Release:	2
Summary:	GTK2 client for LiveJournal
License:	GPLv2+
Group:		Networking/Other
URL:		http://logjam.danga.com/
Source0:	http://logjam.danga.com/download/logjam-%{version}.tar.bz2
Patch0:		logjam-4.4.1-fedora-desktop.patch
Patch1:		logjam-4.6.2-sfmt.patch
%if %{use_xmms}
BuildRequires:	xmms-devel
%endif
BuildRequires:	autoconf
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	aspell-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtkspell-2.0)
BuildRequires:	pkgconfig(libgtkhtml-3.14)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(sqlite)
Requires:	curl
Requires:	gtkspell

%description
This is the new GTK2 client for LiveJournal (http://www.livejournal.com).

%if %{use_xmms}
%package xmms
Summary:	LogJam helper binary
Group:		Graphical desktop/GNOME
Requires:	logjam
Requires:	xmms

%description xmms
This is a helper binary for LogJam which is used to get the
current music from XMMS.
%endif

%prep
%setup -q
%patch0 -p1 -b .desktop
%patch1 -p1 -b .sfmt

%build
autoconf
%configure2_5x \
	--with-sqlite3 \
%if %{use_xmms}
	--with-xmms
%endif

%make

%install
%makeinstall_std
# Rename locale dir, bugzilla 210206
# mv %{buildroot}%{_datadir}/locale/en_US.UTF-8 %{buildroot}%{_datadir}/locale/en_US

%find_lang %{name}

desktop-file-install	\
	--dir %{buildroot}%{_datadir}/applications	\
	%{buildroot}/%{_datadir}/applications/logjam.desktop

%files -f %{name}.lang
%doc doc/README COPYING doc/TODO
%{_bindir}/logjam
%{_mandir}/man*/logjam.1.*
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/logjam*

%if %{use_xmms}
%files xmms
%{_bindir}/logjam-xmms-client
%endif

