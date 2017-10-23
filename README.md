erlang builder
==============

This Erlang/OTP builder is a system based on Docker to build the Debian packages for Erlang/OTP keeping in mind:

- The packages are generated as `otp-VSN` (i.e. `otp-18.2`, `otp-20.0`) to be possible to have more than one version installed in the system.
- The versions are configured with `update-alternatives` system.
- The `epmd` is configured as a service to be started only one per host.
- All in only one package. Easy to install, upgrade and remove.

If you want to propose changes you can fork and create a pull request, create an issue with a request/question and/or make a donation to support this and other similar projects.

Enjoy!
