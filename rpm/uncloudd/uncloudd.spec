Name:           uncloud
Version:        0.20.0
Release:        1.0
Summary:        Uncloud Daemon
License:        ASL-2.0
URL:            https://uncloud.run
Source0:        %{name}-%{version}.tar.gz
Source1:        uncloud.service
Source2:        docker-daemon.json
Requires:       docker
Recommends:     uc
BuildRequires:  pkgconfig(systemd)
%{?systemd_ordering}

%description
Lightweight clustering and container orchestration tool that lets you deploy and
manage web apps across cloud VMs and bare metal with minimised cluster management overhead.
https://github.com/psviderski/uncloud

%define services uncloud.service
%define _topdir %(echo $PWD)/
%define _url https://github.com/miekg/uncloudplus/releases/download/nightly/

%prep

%build
%ifarch aarch64
curl -L %{_url}/%{name}d_linux_arm64.tar.gz > %{name}.tar.gz
%endif
%ifarch x86_64
curl -L %{_url}/%{name}d_linux_amd64.tar.gz > %{name}.tar.gz
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
mkdir /var/lib/uncloud && chown uncloud:uncloud /var/lib/uncloud
# selinux: allow uncloud to mount these paths in the container
chcon -Rt container_file_t /var/lib/uncloud
chcon -Rt container_file_t /run/uncloud
chcon  -t container_file_t /var/run/docker.sock

%preun
%systemd_preun uncloud.service

%postun
%systemd_postun_with_restart uncloud.service
