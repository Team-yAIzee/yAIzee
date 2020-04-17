Resources directory
=====================

This is the resources directory. It currently has only the
purpose to hold the JSON configuration files.

Environment-specific configuration
-----------------------------------

For the application to work in different environments and
setups of the camera as well as with different computing
systems (e.g., screen resolution may differ), the
environment-specific configurations are, instead of being
hard-coded inside the Python files, stored in the file
`config.json`. This file is therefore to be excluded from Git
version control. A default configuration, as used in the
initial setup, can be found in `defaultconf.json`. This file
may then be copied to `config.json` and be adjusted as
necessary. To obtain the configuration values as a
dictionary, use the function obtain_configuration from
`configuration.py`.