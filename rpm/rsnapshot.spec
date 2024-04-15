# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.32
# 

Name:       rsnapshot

# >> macros
# << macros
%define vimpluginname rsnapshot
%define vimplugindir %{_datadir}/vimfiles
%define vimpluginsubdirs after autoload colors compiler doc ftdetect ftplugin indent keymap macros plugin spell syntax

Summary:    A tool for backing up your data using rsync
Version:    1.4.5
Release:    0
Group:      Applications/Archiving
License:    GPLv2 and ASL 2.0
BuildArch:  noarch
URL:        https://rsnapshot.org/
Source0:    %{name}-%{version}.tar.gz
Source100:  rsnapshot.yaml
Source101:  rsnapshot-rpmlintrc
Requires:   rsync
Requires:   perl
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  rsync
BuildRequires:  lvm2
BuildRequires:  openssh-clients
BuildRequires:  systemd

%description
%{summary}.

rsnapshot is a filesystem snapshot utility based on rsync. rsnapshot makes
it easy to make periodic snapshots of local machines, and remote machines
over ssh. The code makes extensive use of hard links whenever possible, to
greatly reduce the disk space required.

The SailfishOS Chum package includes example configs and systemd timer units
to run it periodically. For them to work you must:

    1. Create a valid config file in ~/.config/rsnapshot/rsnapshot.conf
    2. Enable and start the rsnapshot-user.target

%if "%{?vendor}" == "chum"
Title: rsnapshot
Type: console-application
PackagedBy: nephros
Categories:
 - System
 - Utility
Custom:
  Repo: https://github.com/rsnapshot/rsnapshot
  PackagingRepo: https://github.com/sailfishos-chum/rsnapshot
PackageIcon: https://avatars.githubusercontent.com/u/10962189?s=200&v=4
Links:
  Homepage: %{url}
  Help: https://lists.sourceforge.net/lists/listinfo/rsnapshot-discuss
%endif


%package -n vim-rsnapshot
Summary:    Vim configuration for rsnapshot configuration files editing
Group:      Development/Tools
Requires:   vim-filesystem

%description -n vim-rsnapshot
%{summary}.

%prep
%setup -q -n %{name}-%{version}/rsnapshot

# >> setup
# << setup

%build
# >> build pre
sed -i '/^autoreconf/d' autogen.sh
./autogen.sh
# << build pre

%reconfigure --disable-static
make %{?_smp_mflags}

# >> build post
pushd ../sailfish-config
%cmake -DDEFAULTUSER_ENABLE=ON -DNEMO_ENABLE=ON .
%make_build
popd
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%make_install

# >> install post
# do not package documentation:
rm -rf %{buildroot}%{_docdir}
rm -rf %{buildroot}%{_mandir}

pushd ../sailfish-config
%make_install
popd

# vim plugin
pushd ../vim-rsnapshot
%__install -d %{buildroot}%{vimplugindir}
for d in %{vimpluginsubdirs}; do
if [ -d "$d" ]; then
cp -r "$d" %{buildroot}%{vimplugindir}/
fi
done

# << install post

%files
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/*
%config %{_sysconfdir}/rsnapshot/
%config %{_sysconfdir}/rsnapshot.conf.default
%config %{_sysconfdir}/rsnapshot.conf.sailfish_*
%config %{_userunitdir}/rsnapshot-user@.service
%config %{_userunitdir}/rsnapshot-user*.timer
%config %{_userunitdir}/rsnapshot-user.target
# >> files
# << files

%files -n vim-rsnapshot
%defattr(-,root,root,-)
%{vimplugindir}/*/%{vimpluginname}.vim
# >> files vim-rsnapshot
# << files vim-rsnapshot
