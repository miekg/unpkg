Name:           uc
Version:        0.20.0
Release:        1.0
Summary:        Uncloud Cli
License:        ASL-2.0
URL:            https://uncloud.run
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  pkgconfig(systemd)
%{?systemd_ordering}

%description
Lightweight clustering and container orchestration tool that lets you deploy and
manage web apps across cloud VMs and bare metal with minimised cluster management overhead.
https://github.com/psviderski/uncloud

%define _topdir %(echo $PWD)/

%prep

%build
%ifarch aarch64
curl -L https://github.com/psviderski/uncloud/releases/download/v%{version}/%{name}_linux_arm64.tar.gz > %{name}.tar.gz
%endif
%ifarch x86_64
curl -L https://github.com/psviderski/uncloud/releases/download/v%{version}/%{name}_linux_amd64.tar.gz > %{name}.tar.gz
%endif
tar xf %{name}.tar.gz

%install
install -D -m 0755 %{name}        %{buildroot}/%{_bindir}/%{name}

%files
%{_bindir}/%{name}

%post

%preun

%postun
