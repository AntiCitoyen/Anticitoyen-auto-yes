Name:           auto-yes
Version:        @VERSION@
Release:        1%{?dist}
Summary:        Automatically answers "1" (Yes) to "Do you want to proceed?" prompts
License:        MIT
URL:            https://github.com/AntiCitoyen/Anticitoyen-auto-yes
Source0:        Anticitoyen-auto-yes-%{version}.tar.gz
BuildArch:      noarch
Requires:       expect
Requires:       procps-ng

%description
auto-yes wraps a command (auto-yes <command>) or a whole terminal
(auto-yes-shell) and types "1" + Enter when a confirmation menu matching a
pattern of /etc/auto-yes/patterns.conf appears. The terminal stays fully
interactive. Answers wait for the screen to stay quiet, are logged, and can be
paused in every open terminal (auto-yes --pause).

Warning: this silently confirms ANY prompt matching a configured pattern,
including from destructive commands. Keep the pattern list narrow.

%prep
%autosetup -n Anticitoyen-auto-yes-%{version}

%build

%install
packaging/install.sh %{buildroot}
rm -r %{buildroot}/usr/share/licenses

%files
%license LICENSE
%doc README.md
%{_bindir}/auto-yes
%{_bindir}/auto-yes-shell
%{_bindir}/auto-yes-configurer-gnome-terminal
%dir %{_sysconfdir}/auto-yes
%config(noreplace) %{_sysconfdir}/auto-yes/patterns.conf
%{_datadir}/auto-yes/
%{_mandir}/man1/auto-yes*.1*
