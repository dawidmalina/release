%global KUBE_VERSION 1.3.9
%global FLANNEL_VERSION 0.6.2
%global ETCD_VERSION 2.3.7
%global RPM_RELEASE 0

Name: kubelet
Version: %{KUBE_VERSION}
Release: %{RPM_RELEASE}
Summary: Container cluster management
License: ASL 2.0

URL: https://kubernetes.io
Source0: https://storage.googleapis.com/kubernetes-release/release/v%{KUBE_VERSION}/bin/linux/amd64/kubelet
Source1: kubelet.service

BuildRequires: curl
Requires: iptables >= 1.4.21
Requires: socat
Requires: util-linux
Requires: ethtool

%description
The node agent of Kubernetes, the container cluster manager.

%package -n kubectl

Summary: Command-line utility for interacting with a Kubernetes cluster.

%description -n kubectl
Command-line utility for interacting with a Kubernetes cluster.

%package -n kube-proxy

Summary: Command-line utility for interacting with a Kubernetes cluster.

%description -n kube-proxy
Command-line utility for interacting with a Kubernetes cluster.

%package -n flannel
Version: %{FLANNEL_VERSION}

Summary: Flannel is virtual network that gives a subnet to each host for use with container runtimes.

%description -n flannel
Command-line utility for interacting with a Kubernetes cluster.

%package -n etcd
Version: %{ETCD_VERSION}

Summary: Etcd is a distributed, consistent key-value store for shared configuration and service discovery.

%description -n etcd
Command-line utility for interacting with a Kubernetes cluster.

%prep
# Assumes the builder has overridden sourcedir to point to directory
# with this spec file. (where these files are stored) Copy them into
# the builddir so they can be installed.
#
# Example: rpmbuild --define "_sourcedir $PWD" -bb kubelet.spec
#
cp -p %{_sourcedir}/kubelet.service %{_builddir}/
cp -p %{_sourcedir}/kube-proxy.service %{_builddir}/
cp -p %{_sourcedir}/flanneld.service %{_builddir}/
cp -p %{_sourcedir}/etcd.service %{_builddir}/

# NOTE: Uncomment if you have these binaries in the directory you're building from.
# This is a useful temporary hack for faster Docker builds when working on the spec.
# Implies you also comment out the curl commands below.
#cp -p %{_sourcedir}/kubelet %{_builddir}/
#cp -p %{_sourcedir}/kubectl %{_builddir}/
#cp -p %{_sourcedir}/kubeadm %{_builddir}/


%install

curl -L --fail "https://storage.googleapis.com/kubernetes-release/release/v%{KUBE_VERSION}/bin/linux/amd64/kubelet" -o kubelet
curl -L --fail "https://storage.googleapis.com/kubernetes-release/release/v%{KUBE_VERSION}/bin/linux/amd64/kubectl" -o kubectl
curl -L --fail "https://storage.googleapis.com/kubernetes-release/release/v%{KUBE_VERSION}/bin/linux/amd64/kube-proxy" -o kube-proxy
curl -L --fail "https://github.com/coreos/flannel/releases/download/v%{FLANNEL_VERSION}/flanneld-amd64" -o flanneld
curl -L --fail "https://github.com/coreos/etcd/releases/download/v%{ETCD_VERSION}/etcd-v%{ETCD_VERSION}-linux-amd64.tar.gz" -o etcd.tar.gz
tar -xzf etcd.tar.gz
cp -v etcd-v%{ETCD_VERSION}-linux-amd64/etcd etcd
cp -v etcd-v%{ETCD_VERSION}-linux-amd64/etcdctl etcdctl
rm -rf etcd.tar.gz etcd-v%{ETCD_VERSION}-linux-amd64

install -m 755 -d %{buildroot}%{_bindir}
install -m 755 -d %{buildroot}%{_sysconfdir}/systemd/system/
install -m 755 -d %{buildroot}%{_sysconfdir}/kubernetes/manifests/
install -m 755 -d %{buildroot}/var/lib/kubelet/
install -p -m 755 -t %{buildroot}%{_bindir}/ kubelet
install -p -m 755 -t %{buildroot}%{_bindir}/ kubectl
install -p -m 755 -t %{buildroot}%{_bindir}/ kube-proxy
install -p -m 755 -t %{buildroot}%{_bindir}/ flanneld
install -p -m 755 -t %{buildroot}%{_bindir}/ etcd
install -p -m 755 -t %{buildroot}%{_bindir}/ etcdctl
install -p -m 755 -t %{buildroot}%{_sysconfdir}/systemd/system/ kubelet.service
install -p -m 755 -t %{buildroot}%{_sysconfdir}/systemd/system/ kube-proxy.service
install -p -m 755 -t %{buildroot}%{_sysconfdir}/systemd/system/ flanneld.service
install -p -m 755 -t %{buildroot}%{_sysconfdir}/systemd/system/ etcd.service


%files
%{_bindir}/kubelet
%{_sysconfdir}/systemd/system/kubelet.service
%{_sysconfdir}/kubernetes/manifests/

%files -n kube-proxy
%{_bindir}/kube-proxy
%{_sysconfdir}/systemd/system/kube-proxy.service

%files -n flannel
%{_bindir}/flanneld
%{_sysconfdir}/systemd/system/flanneld.service

%files -n etcd
%{_bindir}/etcd
%{_bindir}/etcdctl
%{_sysconfdir}/systemd/system/etcd.service

%files -n kubectl
%{_bindir}/kubectl

%doc


%changelog
* Tue Sep 20 2016 dgoodwin <dgoodwin@redhat.com> - 1.4.0-0
- Add kubectl and kubeadm sub-packages.
- Rename to kubernetes-cni.
- Update versions of CNI.

* Wed Jul 20 2016 dgoodwin <dgoodwin@redhat.com> - 1.3.4-1
- Initial packaging.
