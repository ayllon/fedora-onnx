Name:       python-onnx
Version:    1.12.0
Release:    1%{?dist}
Summary:    Open standard for machine learning interoperability
License:    ASL 2.0
URL:        https://github.com/onnx/onnx
Source0:    https://github.com/onnx/onnx/archive/v%{version}/%{name}-%{version}.tar.gz
# Add what is missing to run tox, disable tests that require network
Patch0:     onnx-tox.patch
# Do not install script oriented towards onnx contributors
Patch1:     onnx-disable-test-tools.patch

# Architecture not supported: lots of "unsupported adapters" errors
ExcludeArch:    s390x

BuildRequires:  cmake >= 3.13
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  zlib-devel
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-pybind11
BuildRequires:  protobuf-lite-devel

%global _description %{expand:
%{name} provides an open source format for AI models, both deep learning and
traditional ML. It defines an extensible computation graph model, as well as
definitions of built-in operators and standard data types.}

%description %_description

%package -n python3-onnx
Summary:        %{summary}

%description -n python3-onnx %_description

%prep
%autosetup -p1 -n onnx-%{version}

%generate_buildrequires
%pyproject_buildrequires -t

%build
export CMAKE_ARGS="-DONNX_USE_LITE_PROTO=ON -DONNX_USE_PROTOBUF_SHARED_LIBS=ON"
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files onnx

%check
%tox

%files -n python3-onnx -f %{pyproject_files}
%{_bindir}/check-model
%{_bindir}/check-node

%changelog
* Wed Nov 23 2022 Alejandro Alvarez Ayllon <aalvarez@fedoraproject.org> - 1.12.0-1
- Release 1.12.0

