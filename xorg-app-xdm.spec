Summary:	xdm - X Display Manager with support for XDMCP, host chooser
Summary(pl):	XDM - zarz±dca ekranÛw z obs≥ug± XDMCP i wybieraniem hostÛw
Summary(ru):	Ì≈Œ≈ƒ÷≈“ ƒ…”–Ã≈— X
Summary(uk):	Ì≈Œ≈ƒ÷≈“ ƒ…”–Ã≈¿ X
Name:		xorg-app-xdm
Version:	0.99.4
Release:	0.1
License:	MIT
Group:		X11/Applications
Source0:	http://xorg.freedesktop.org/releases/X11R7.0-RC3/app/xdm-%{version}.tar.bz2
# Source0-md5:	8ea0b887baf9d702c883f8e85fb100b8
URL:		http://xorg.freedesktop.org/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	cpp
BuildRequires:	pam-devel
BuildRequires:	pkgconfig >= 1:0.19
BuildRequires:	xorg-lib-libXaw-devel
BuildRequires:	xorg-lib-libXdmcp-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXpm-devel
BuildRequires:	xorg-lib-xtrans-devel
BuildRequires:	xorg-util-util-macros >= 0.99.2
Requires:	xorg-app-sessreg
Provides:	XDM
Provides:	xdm = %{version}-%{release}
Obsoletes:	X11-xdm
Obsoletes:	XFree86-xdm
Obsoletes:	entrance
Obsoletes:	gdm
Obsoletes:	kdm
Obsoletes:	wdm
Obsoletes:	xdm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Xdm manages a collection of X displays, which may be on the local host
or remote servers. The design of xdm was guided by the needs of X
terminals as well as the X Consortium standard XDMCP, the X Display
Manager Control Protocol.

%description -l pl
Xdm zarz±dza zestawem ekranÛw X, ktÛre mog± byÊ lokalne lub na
zdalnych serwerach. Zosta≥ zaprojektowany zgodnie z potrzebami X
terminali oraz standardem X Consortium XDMCP.

%description -l ru
Ì≈Œ≈ƒ÷≈“ ƒ…”–Ã≈— X.

%description -l uk
Ì≈Œ≈ƒ÷≈“ ƒ…”–Ã≈¿ X.

%prep
%setup -q -n xdm-%{version}

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/X11/xdm/libXdmGreet.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_bindir}/xdm
%attr(755,root,root) %{_bindir}/xdmshell
%{_libdir}/X11/app-defaults/Chooser
%dir %{_libdir}/X11/xdm
%attr(755,root,root) %{_libdir}/X11/xdm/libXdmGreet.so
%attr(755,root,root) %{_libdir}/X11/xdm/GiveConsole
%attr(755,root,root) %{_libdir}/X11/xdm/TakeConsole
%{_libdir}/X11/xdm/Xaccess
%attr(755,root,root) %{_libdir}/X11/xdm/Xreset
%{_libdir}/X11/xdm/Xresources
%{_libdir}/X11/xdm/Xservers
%attr(755,root,root) %{_libdir}/X11/xdm/Xsession
%attr(755,root,root) %{_libdir}/X11/xdm/Xsetup_0
%attr(755,root,root) %{_libdir}/X11/xdm/Xstartup
%attr(755,root,root) %{_libdir}/X11/xdm/Xwilling
%attr(755,root,root) %{_libdir}/X11/xdm/chooser
%{_libdir}/X11/xdm/pixmaps
%{_libdir}/X11/xdm/xdm-config
%{_mandir}/man1/xdm.1x*
