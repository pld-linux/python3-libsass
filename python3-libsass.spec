#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

Summary:	Sass for Python: A straightforward binding of libsass for Python
Summary(pl.UTF-8):	Sass dla Pythona - bezpośrednie wiązanie libsass dla Pythona
Name:		python3-libsass
Version:	0.23.0
Release:	3
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/sass/libsass-python/releases
Source0:	https://github.com/sass/libsass-python/archive/%{version}/libsass-python-%{version}.tar.gz
# Source0-md5:	3d628c3b4c1aff475db694b48de1f322
Patch0:		libsass-python-sphinx-extlinks.patch
URL:		https://sass-lang.com/libsass-python
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	python3 >= 1:3.8
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-werkzeug >= 0.9
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg-3 >= 1.3
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides a simple Python extension module sass which is
binding LibSass (written in C/C++ by Hampton Catlin and Aaron Leung).

%description -l pl.UTF-8
Ten pakiet dostarcza prosty moduł rozszerzenia Pythona sass, będący
wiązaniem LibSass (napisanej w C/C++ przez Hamptona Catlina i Aarona
Leunga).

%package apidocs
Summary:	API documentation for Python sass module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona sass
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python sass module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona sass.

%prep
%setup -q -n libsass-python-%{version}
%patch -P0 -p1

%build
export SYSTEM_SASS=1
%py3_build

%if %{with tests}
# test_build_sass and test_output_style tests build libsass itself using network
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
%{__python3} -m pytest sasstests.py -k 'not test_build_sass and not test_output_style'
%endif

%if %{with doc}
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

export SYSTEM_SASS=1
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/sasstests.py
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/__pycache__/sasstests.*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%attr(755,root,root) %{_bindir}/pysassc
%attr(755,root,root) %{py3_sitedir}/_sass.abi3.so
%attr(755,root,root) %{py3_sitedir}/pysassc.py
%attr(755,root,root) %{py3_sitedir}/sass.py
%attr(755,root,root) %{py3_sitedir}/__pycache__/pysassc.cpython-*.py[co]
%attr(755,root,root) %{py3_sitedir}/__pycache__/sass.cpython-*.py[co]
%attr(755,root,root) %{py3_sitedir}/sassutils
%attr(755,root,root) %{py3_sitedir}/libsass-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,frameworks,sassutils,*.html,*.js}
%endif
