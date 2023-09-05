%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-ouster-ros
Version:        0.10.4
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS ouster_ros package

License:        BSD
Source0:        %{name}-%{version}.tar.gz

Requires:       curl
Requires:       jsoncpp
Requires:       libcurl-devel
Requires:       libtins-devel
Requires:       ros-rolling-geometry-msgs
Requires:       ros-rolling-launch
Requires:       ros-rolling-launch-ros
Requires:       ros-rolling-ouster-msgs
Requires:       ros-rolling-pcl-conversions
Requires:       ros-rolling-pcl-ros
Requires:       ros-rolling-rclcpp
Requires:       ros-rolling-rclcpp-components
Requires:       ros-rolling-rclcpp-lifecycle
Requires:       ros-rolling-rosidl-default-runtime
Requires:       ros-rolling-sensor-msgs
Requires:       ros-rolling-std-msgs
Requires:       ros-rolling-std-srvs
Requires:       ros-rolling-tf2-ros
Requires:       spdlog-devel
Requires:       ros-rolling-ros-workspace
BuildRequires:  curl
BuildRequires:  eigen3-devel
BuildRequires:  jsoncpp-devel
BuildRequires:  libcurl-devel
BuildRequires:  libtins-devel
BuildRequires:  pcl-devel
BuildRequires:  ros-rolling-ament-cmake
BuildRequires:  ros-rolling-geometry-msgs
BuildRequires:  ros-rolling-ouster-msgs
BuildRequires:  ros-rolling-pcl-conversions
BuildRequires:  ros-rolling-pcl-ros
BuildRequires:  ros-rolling-rclcpp
BuildRequires:  ros-rolling-rclcpp-components
BuildRequires:  ros-rolling-rclcpp-lifecycle
BuildRequires:  ros-rolling-rosidl-default-generators
BuildRequires:  ros-rolling-sensor-msgs
BuildRequires:  ros-rolling-std-msgs
BuildRequires:  ros-rolling-std-srvs
BuildRequires:  ros-rolling-tf2-eigen
BuildRequires:  ros-rolling-tf2-ros
BuildRequires:  spdlog-devel
BuildRequires:  ros-rolling-ros-workspace
BuildRequires:  ros-rolling-rosidl-typesupport-fastrtps-c
BuildRequires:  ros-rolling-rosidl-typesupport-fastrtps-cpp
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}
Provides:       ros-rolling-rosidl-interface-packages(member)

%if 0%{?with_tests}
BuildRequires:  gtest-devel
%endif

%if 0%{?with_weak_deps}
Supplements:    ros-rolling-rosidl-interface-packages(all)
%endif

%description
Ouster ROS2 driver

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/rolling" \
    -DAMENT_PREFIX_PATH="/opt/ros/rolling" \
    -DCMAKE_PREFIX_PATH="/opt/ros/rolling" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
%license LICENSE
/opt/ros/rolling

%changelog
* Tue Sep 05 2023 Ussama Naal <ussama.naal@ouster.io> - 0.10.4-1
- Autogenerated by Bloom

