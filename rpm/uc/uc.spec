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
%{name} docs --manual
%{name} completion zsh > _uc
%{name} completion bash > uc.bash

%install
install -D -m 0755 %{name}           %{buildroot}/%{_bindir}/%{name}
install -d -m 0755                   %{buildroot}%{_mandir}/man1
install -m 0644 %{buildroot}/../*.1  %{buildroot}%{_mandir}/man1
install -d -m 0755                   %{buildroot}/usr/share/zsh/vendor-completions
install -d -m 0755                   %{buildroot}/usr/share/bash-completion/completions
install -m 0644 %{buildroot}/../_uc      %{buildroot}/usr/share/zsh/vendor-completions
install -m 0644 %{buildroot}/../uc.bash  %{buildroot}/usr/share/bash-completion/completions

%files
%{_bindir}/%{name}
%{_mandir}/man1/*
/usr/share/zsh/vendor-completions/_uc
/usr/share/bash-completion/completions/uc.bash

%post

%preun

%postun
