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
Patch0:		%{name}-path.patch
URL:		http://www.jdimedia.nl/igmar/mod_%{mod_name}/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel
Requires(post,preun):	%{apxs}
Requires:	apache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

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
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sbindir}}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install validate $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc CHANGES README
%attr(755,root,root) %{_pkglibdir}/*
%attr(4755,root,root) %{_sbindir}/*
