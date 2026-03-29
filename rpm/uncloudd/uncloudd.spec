Name:           uncloud
Version:        0.17.1
Release:        1.0
Summary:        Uncloud Daemon
License:        ASL-2.0
URL:            https://uncloud.run
Source0:        %{name}-%{version}.tar.gz
Source1:        uncloud.service
Source2:        docker-daemon.json
Requires:       docker
BuildRequires:  pkgconfig(systemd)
%{?systemd_ordering}

%description
Lightweight clustering and container orchestration tool that lets you deploy and
manage web apps across cloud VMs and bare metal with minimised cluster management overhead.
https://github.com/psviderski/uncloud

%define services uncloud.service
%define _topdir %(echo $PWD)/

%prep

%build
%ifarch aarch64
curl -L https://github.com/psviderski/uncloud/releases/download/v%{version}/uncloudd_linux_arm64.tar.gz > %{name}.tar.gz
%endif
%ifarch x86_64
curl -L https://github.com/psviderski/uncloud/releases/download/v%{version}/uncloudd_linux_amd64.tar.gz > %{name}.tar.gz
%endif
tar xf %{name}.tar.gz

%install
cp %{_topdir}uncloud.service %{buildroot}/../uncloud.service
cp %{_topdir}%{name}d.conf %{buildroot}/../%{name}d.conf
cp %{_topdir}docker-daemon.json %{buildroot}/../docker-daemon.json

install -D -m 0755 %{name}d         %{buildroot}/%{_bindir}/%{name}d
install -D -m 0644 uncloud.service  %{buildroot}/%{_unitdir}/uncloud.service

install -D -m 0640 docker-daemon.json  %{buildroot}%{_sysconfdir}/docker/docker-daemon.json
install -D -m 0640 %{name}d.conf       %{buildroot}/usr/lib/sysusers.d/%{name}d.conf

%files
%{_bindir}/%{name}d
%{_unitdir}/uncloud.service
%{_sysconfdir}/docker/docker-daemon.json
/usr/lib/sysusers.d/%{name}d.conf

%post
%systemd_post uncloud.service

%preun
%systemd_preun uncloud.service

%postun
%systemd_postun_with_restart uncloud.service
