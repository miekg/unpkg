Name:           uncloud-corrosion
Version:        0.2.2
Release:        1.0
Summary:        Uncloud gossip-based distributed store
License:        ASL-2.0
URL:            https://uncloud.run
Source0:        %{name}-%{version}.tar.gz
Source1:        corrosion.service
BuildRequires:  pkgconfig(systemd), systemd-rpm-macros
%{?systemd_ordering}

%description
Corrosion is a Rust program that propagates a SQLite database with a gossip protocol.

%define services corrosion.service
%define _topdir %(echo $PWD)/

%prep

%build
curl -L https://github.com/psviderski/corrosion/releases/download/v%{version}/corrosion-%{_arch}-unknown-linux-gnu.tar.gz > %{name}.tar.gz
tar xf %{name}.tar.gz && mv corrosion %{name}

%install
cp %{_topdir}uncloud-corrosion.service %{buildroot}/../uncloud-corrosion.service

install -D -m 0755 %{name }                  %{buildroot}/%{_bindir}/%{name}
install -D -m 0644 uncloud-corrosion.service %{buildroot}/%{_unitdir}/uncloud-corrosion.service

%files
%{_bindir}/%{name}
%{_unitdir}/uncloud-corrosion.service

%post
%systemd_post uncloud-corrosion.service

%preun
%systemd_preun uncloud-corrosion.service

%postun
%systemd_postun_with_restart uncloud-corrosion.service
