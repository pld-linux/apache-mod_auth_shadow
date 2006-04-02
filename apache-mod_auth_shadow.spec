%define		mod_name	auth_shadow
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: authenticating against a /etc/shadow file
Summary(pl):	Modu� do apache: autoryzacja przez plik /etc/shadow
Name:		apache-mod_%{mod_name}
Version:	2.1
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/mod-auth-shadow/mod_auth_shadow-%{version}.tar.gz
# Source0-md5:	564f11a9d19ea546673644fdacb928e7
Patch0:		%{name}-make.patch
URL:		http://mod-auth-shadow.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
Obsoletes:	apache-mod_auth-shadow
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
mod_auth_shadow is an Apache module for authenticating users via an
/etc/shadow file.

When performing this task one encounters one fundamental difficulty:
the /etc/shadow file is supposed to be read/writeable only by root.
However, the webserver is supposed to run under a non-root user, such
as "http".

mod_auth_shadow addresses this difficulty by opening a pipe to an suid
root program, validate, which does the actual validation. When there
is a failure, validate writes an error message to the system log, and
waits three seconds before exiting.

%description -l pl
mod_auth_shadow to modu� Apache'a do uwierzytelniania u�ytkownik�w
poprzez plik /etc/shadow.

Przy wykonywaniu tego zadania jest jedna zasadnicza trudno��: plik
/etc/shadow mo�e by� odczytywany/zapisywany tylko przez roota. Jednak
serwer WWW ma dzia�a� z prawami u�ytkownika innego ni� root, takiego
jak "http".

mod_auth_shadow obchodzi ten problem poprzez otwieranie potoku do
programu z ustawionym atrybutem suid root - validate - wykonuj�cego
w�a�ciwe sprawdzanie has�a. W przypadku b��du validate zapisuje
komunikat do loga systemowego i czeka trzy sekundy przed zako�czeniem.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	INSTBINDIR=%{_sbindir} \
	APXS=%{apxs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sbindir},%{_sysconfdir}/httpd.conf}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install validate $RPM_BUILD_ROOT%{_sbindir}
echo 'LoadModule %{mod_name}_module modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%preun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc CHANGES INSTALL README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
%attr(4755,root,root) %{_sbindir}/validate
