erlang builder
==============

This Erlang/OTP builder is a system based on Docker to build the Debian packages for Erlang/OTP keeping in mind:

- The packages are generated as `otp-VSN` (i.e. `otp-18.2`, `otp-20.0`) to be possible to have more than one version installed in the system.
- The versions are configured with `update-alternatives` system.
- The `epmd` is configured as a service to be started only one per host.
- All in only one package. Easy to install, upgrade and remove.

If you want to propose changes you can fork and create a pull request, create an issue with a request/question and/or make a donation to support this and other similar projects.

Versions of Debian (see https://wiki.debian.org/DebianReleases)

6. Squeeze (end of life: 2016-02-29)
7. Wheezy (end of life: 2018-05-31)
8. Jessie (end of life: 2020-06-30)
9. Stretch (end of life: 2022-06-30)
10. Buster (old-stable)
11. Bullseye (stable)
12. Bookworm (testing)

Enjoy!
