%define	name	logjam
%define	version	4.5.3
%define	release	%mkrel 1
%define use_xmms 1

Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		1
Summary:	GTK2 client for LiveJournal
License:	GPL
Group:		User Interface/Desktops
URL:		http://logjam.danga.com/
Source0:	http://logjam.danga.com/download/logjam-%{version}.tar.bz2
Requires:	curl >= 7.9, gtkspell
%if %{use_xmms}
BuildRequires:	xmms-devel
%endif
BuildRequires:	curl-devel, gtk2-devel, gtkspell-devel, libgtkhtml-3.14-devel
BuildRequires:	gettext, desktop-file-utils, aspell-devel, librsvg2-devel
BuildRequires:	libsoup-devel, sqlite-devel, gnutls-devel, libgcrypt-devel
BuildRequires:	autoconf, intltool
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch2:		logjam-4.4.1-backdated.patch
Patch3:		logjam-4.4.1-cleanups.patch
Patch4:		logjam-4.4.1-fedora-desktop.patch
Patch5:		logjam-4.5-patch8-manfix.patch
Patch6:		logjam-4.5.2-gtkhtml38.patch
Patch7:		logjam-4.4.1-ru.po.asp.patch
Patch8:		logjam-4.5.3-gtkspell.patch
Patch9:		http://people.freebsd.org/~novel/patches/non-freebsd/logjam_docklet_context_menu.diff

%description
This is the new GTK2 client for LiveJournal (http://www.livejournal.com).

%if %{use_xmms}
%package xmms
Summary:	LogJam helper binary
Group:		User Interface/Desktops
Requires:	logjam, xmms
BuildRequires:	xmms-devel

%description xmms
This is a helper binary for LogJam which is used to get the
current music from XMMS.
%endif

%prep
%setup -q
%patch2 -p1 -b .backdated
%patch3 -p1 -b .cleanups
%patch4 -p1 -b .desktop
%patch5 -p1 -b .manfix
%patch6 -p1 -b .gtkhtml38
%patch7 -p1 -b .ru.po
%patch8 -p1 -b .bz186906
%patch9 -p1 -b .docklet-context-menu

%build
autoconf
%configure --with-sqlite3 \
%if %{use_xmms}
	--with-xmms
%endif
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
# Rename locale dir, bugzilla 210206
# mv $RPM_BUILD_ROOT%{_datadir}/locale/en_US.UTF-8 $RPM_BUILD_ROOT%{_datadir}/locale/en_US
%find_lang %{name}
desktop-file-install --vendor fedora			\
  --dir $RPM_BUILD_ROOT%{_datadir}/applications		\
  --add-category X-Fedora				\
  --delete-original					\
  $RPM_BUILD_ROOT/%{_datadir}/applications/logjam.desktop

%files -f %{name}.lang
%defattr(-,root,root)
%doc doc/README COPYING doc/TODO
%{_bindir}/logjam
%{_mandir}/man*/logjam.1.lzma
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/logjam*

%if %{use_xmms}
%files xmms
%defattr(-,root,root)
%{_bindir}/logjam-xmms-client
%endif

%clean
rm -rf $RPM_BUILD_ROOT

