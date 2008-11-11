# TODO
# - Source1 contains X11R6 paths and the scripts inside should be reviewed for
#   security issues
Summary:	xdm - X Display Manager with support for XDMCP, host chooser
Summary(pl.UTF-8):	XDM - zarządca ekranów z obsługą XDMCP i wybieraniem hostów
Summary(ru.UTF-8):	Менеджер дисплея X
Summary(uk.UTF-8):	Менеджер дисплею X
Name:		xorg-app-xdm
Version:	1.1.8
Release:	3
License:	MIT
Group:		X11/Applications
Source0:	http://xorg.freedesktop.org/releases/individual/app/xdm-%{version}.tar.bz2
# Source0-md5:	cc1816bc62a3722ad509373b0b7f30fe
Source1:	ftp://ftp.pld-linux.org/software/xinit/xdm-xinitrc-0.2.tar.bz2
# Source1-md5:	0a15b1c374256b5cad7961807baa3896
Source2:	xdm.pamd
Source3:	xdm.init
Source4:	xdm.sysconfig
Patch0:		%{name}-Xsession.patch
Patch1:		%{name}-pam_tty.patch
Patch2:		%{name}-config.patch
Patch3:		%{name}-xaw.patch
URL:		http://xorg.freedesktop.org/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	cpp
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRequires:	pkgconfig >= 1:0.19
BuildRequires:	xorg-lib-libXau-devel
BuildRequires:	xorg-lib-libXaw-devel
BuildRequires:	xorg-lib-libXdmcp-devel
BuildRequires:	xorg-lib-libXft-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXpm-devel
BuildRequires:	xorg-lib-libXt-devel >= 1.0.0
BuildRequires:	xorg-lib-xtrans-devel
BuildRequires:	xorg-util-util-macros >= 0.99.2
Requires(post,preun):	/sbin/chkconfig
Requires:	mktemp
Requires:	pam >= 0.99.7.1
Requires:	rc-scripts
Requires:	xorg-app-xconsole
Requires:	xorg-app-xrdb
Requires:	xorg-app-xsetroot
Requires:	xorg-app-sessreg
Requires:	xorg-lib-libXt >= 1.0.0
Requires:	xterm
Provides:	XDM
Provides:	xdm = %{version}-%{release}
Obsoletes:	X11-xdm < 1:7.0.0
Obsoletes:	XFree86-xdm < 1:7.0.0
Obsoletes:	xdm < 1:7.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Xdm manages a collection of X displays, which may be on the local host
or remote servers. The design of xdm was guided by the needs of X
terminals as well as the X Consortium standard XDMCP, the X Display
Manager Control Protocol.

%description -l pl.UTF-8
Xdm zarządza zestawem ekranów X, które mogą być lokalne lub na
zdalnych serwerach. Został zaprojektowany zgodnie z potrzebami X
terminali oraz standardem X Consortium XDMCP.

%description -l ru.UTF-8
Менеджер дисплея X.

%description -l uk.UTF-8
Менеджер дисплею X.

%prep
%setup -q -n xdm-%{version} -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	DEF_SYSTEM_PATH="/usr/local/sbin:/usr/sbin:/sbin:/usr/local/bin:/usr/bin:/bin" \
	DEF_USER_PATH="/usr/local/bin:/usr/bin:/bin" \
	--disable-static \
	--with-bw-pixmap=xdm-pld-logo-bw.xpm \
	--with-color-pixmap=xdm-pld-logo.xpm \
	--with-default-vt=vt9 \
	--with-pixmapdir=%{_sysconfdir}/X11/xdm/pixmaps \
	--with-xdmauthdir=/var/lib/xdm \
	--with-xdmconfigdir=%{_sysconfdir}/X11/xdm \
	--with-xdmscriptdir=%{_sysconfdir}/X11/xdm

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/lib/xdm

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	appdefaultdir=%{_datadir}/X11/app-defaults

rm -f $RPM_BUILD_ROOT%{_libdir}/X11/xdm/libXdmGreet.la

# set up PLD xdm config
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/X11/xdm/{*Console,Xaccess,Xsession,Xsetup*}
install xdm-xinitrc-*/pixmaps/* $RPM_BUILD_ROOT%{_sysconfdir}/X11/xdm/pixmaps
install xdm-xinitrc-*/{*Console,Xaccess,Xsession,Xsetup*} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xdm

install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/xdm
install -D %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/xdm
install -D %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/xdm
install -d $RPM_BUILD_ROOT/etc/security
:> $RPM_BUILD_ROOT/etc/security/blacklist.xdm

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add xdm
if [ -f /var/lock/subsys/xdm ]; then
	echo "Run \"/sbin/service xdm restart\" to restart xdm." >&2
	echo "WARNING: it will terminate all sessions opened from xdm!" >&2
else
	echo "Run \"/sbin/service xdm start\" to start xdm." >&2
fi

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del xdm
	%service xdm stop
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README
%attr(755,root,root) %{_bindir}/xdm
%attr(755,root,root) %{_bindir}/xdmshell
%{_datadir}/X11/app-defaults/Chooser
%dir %{_libdir}/X11/xdm
%attr(755,root,root) %{_libdir}/X11/xdm/libXdmGreet.so
%attr(755,root,root) %{_libdir}/X11/xdm/chooser
%dir %{_sysconfdir}/X11/xdm
# scripts
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/xdm/GiveConsole
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/xdm/TakeConsole
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/xdm/Xreset
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/xdm/Xsession
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/xdm/Xsetup_0
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/xdm/Xstartup
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/xdm/Xwilling
# configs
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/xdm/Xaccess
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/xdm/Xresources
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/xdm/Xservers
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/xdm/xdm-config
# pixmaps
%{_sysconfdir}/X11/xdm/pixmaps
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/xdm
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.xdm
%attr(754,root,root) /etc/rc.d/init.d/xdm
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/xdm
%dir /var/lib/xdm
%{_mandir}/man1/xdm.1x*
