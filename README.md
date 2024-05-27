# ProxyConfiguration: A Simple Proxy Configuration Tool

[![made with ❤ in Python](https://img.shields.io/badge/made%20with%20❤%20in-Python-red.svg)](http://shields.io/#your-badge)
[![works on Linux](https://img.shields.io/badge/works%20on-Linux-orange.svg)](http://shields.io/#your-badge)

## Screenshot
![screenshot](/img/scrshot.png)

## Requirements

- Python 3.6+

To install Python 3, visit [python.org](https://www.python.org).

## About

This script removes the hassle of configuring a proxy manually by supporting system-wide proxy configuration. It is kept
as simple as possible and does not use any additional libraries other than those that come with Python 3.

Currently tested on Ubuntu 14.04 LTS, 16.04 LTS, 18.04 LTS, 22.04 LTS.

There are four options:

1. **Set proxy:** Takes input from the user and modifies the required files.
2. **Remove proxy:** Removes any proxy settings present in the files.
3. **View Proxy:** Displays the current proxy settings, if any.
4. **Restore default:** Restores the state before running this script for the first time.

## Example run

```sh
chmod +x proxy.py
```

``` sh
sudo ./proxy.py
``` 