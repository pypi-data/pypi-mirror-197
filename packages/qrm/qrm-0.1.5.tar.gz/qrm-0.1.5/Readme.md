# QrM - Qt5 based file explorer for reMarkable

Use a Qt5 based UI to ~manage~ view, upload, delete content of/to your
reMarkable I/II via SSH.

[Project page](https://projects.om-office.de/frans/qrm)


## Usage

Run `qrm` to connect to and see a list of content on a (WiFi enabled and switched on)
reMarkable device.

Run `qrm config-auth <KEY>=<VALUE> ...` to configure stuff, e.g.

```
qrm config-auth host=192.168.178.13 password='s0rry_Pl4in+ex+!'
```

Run `qrm [ls|list]` to list content on the connected device

Run `qrm [upload|push] <FILE> [<FILE>]` to copy stuff onto the connected device

Run `qrm reboot` to .. you know..


### ToDo for v1.0

* Allow hostnames instead of IP addresses
* Make use of shared keys and configuration in `~/.ssh/config`
* Support drag&drop to add content in UI
* Support deletion

## Installation

```
pip3 install [--user] qrm
```


## Development & Contribution

```
# provide dependencies, consider also using pyenv
pip3 install -U poetry pre-commit

git clone --recurse-submodules https://projects.om-office.de/frans/qrm.git

cd qrm

# activate a pre-commit gate keeper
pre-commit install

# if you need a specific version of Python inside your dev environment
poetry env use ~/.pyenv/versions/3.10.4/bin/python3

poetry install
```

## License

For all code contained in this repository the rules of GPLv3 apply unless
otherwise noted. That means that you can do what you want with the source
code as long as you make the files with their original copyright notice
and all modifications available.

See [GNU / GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html) for details.


## Read

*(nothing here yet)*
