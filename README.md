erlang builder
==============

This Erlang/OTP builder is a system based on Docker to build the Debian packages for Erlang/OTP keeping in mind:

- The packages are generated as `otp-VSN` (i.e. `otp-18.2`, `otp-20.0`) to be possible to have more than one version installed in the system.
- The versions are configured with `update-alternatives` system.
- The `epmd` is configured as a service to be started only one per host.
- All in only one package. Easy to install, upgrade and remove.

If you want to propose changes you can fork and create a pull request, create an issue with a request/question and/or make a donation to support this and other similar projects.

Docker images corresponding to the Debian releases supported (see https://wiki.debian.org/DebianReleases)

9. erlang_stretch
10. erlang_buster
11. erlang_bullseye
12. erlang_bookworm
13. erlang_trixie

You can create each of these images running the script:

```
./build_image.sh trixie
```

These images must be required during the build process.

The build process is now depending on a python script:

```
mkdir -p debian/13/pool
mkdir input
git clone https://github.com/erlang/otp

DEBIAN_VSN=13 ./build_otp.py
```

As you can see it depends on three directories that must be available:

- `debian/XX/pool` based on the Debian release, it's the output where the deb packages are going to be placed.
- `input` is the directory for the source code for Erlang, the system will be creating tarball files according to the different tags.
- `otp` is the source code for Erlang. The script will check the tags, the source code downloaded and the packages generated to conclude what are the following steps to do.

Enjoy!
