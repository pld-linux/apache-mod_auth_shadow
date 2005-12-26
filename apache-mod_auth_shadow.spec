%define		mod_name	auth-shadow
%define		orig_name	auth_shadow
%define		ver		1.3
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: authenticating against a /etc/shadow file
Summary(pl):	Modu³ do apache: autoryzacja przez plik /etc/shadow
Name:		apache-mod_%{mod_name}
Version:	%{ver}
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.jdimedia.nl/igmar/mod_%{mod_name}/files/mod_%{orig_name}-%{version}.tar.gz
# Source0-md5:	46164ccb94489415021a041daa8a3ded
Patch0:		%{name}-path.patch
URL:		http://www.jdimedia.nl/igmar/mod_auth-shadow/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
Apache module: authenticating against a /etc/shadow file

%description -l pl
Modu³ do apache: autoryzacja przez plik /etc/shadow

%prep
%setup -q -n mod_%{orig_name}-%{version}
%patch0 -p1

%build
%{__cc} -o validate validate.c -lcrypt
%{apxs} -c mod_%{orig_name}.c -o mod_%{mod_name}.so -lz

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sbindir},%{_sysconfdir}/httpd.conf}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install validate $RPM_BUILD_ROOT%{_sbindir}
echo 'LoadModule auth_shadow_module modules/mod_auth_shadow.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc CHANGES README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
%attr(4755,root,root) %{_sbindir}/*
