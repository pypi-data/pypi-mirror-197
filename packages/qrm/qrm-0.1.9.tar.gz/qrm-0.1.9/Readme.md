# QrM - Qt5 based file explorer for reMarkable

Use a Qt5 based UI to ~manage~ view, upload, delete content of/to your
reMarkable I/II via SSH.

[Project page](https://projects.om-office.de/frans/qrm)


## Usage

Once configured run `qrm` to start up a UI, connect to and see a list of content on a (WiFi enabled
and switched on) reMarkable device. Drag and drop EPUB and PDF files onto the window to make them
available on the device.

Run `qrm [ls|list]` to list content on the connected device

Run `qrm [upload|push] <FILE> [<FILE>]` to copy stuff onto the connected device

Run `qrm info` to see configuration and stuff

Run `qrm reboot` to .. you know..

Run `qrm config-auth <KEY>=<VALUE> ...` to configure stuff, e.g.

Please note that currently reMarkable will not recognize file modifications done via SSH - to make
new files available you'll have to reboot the device. Run `qrm reboot` or press the `Reboot` button
to do this via SSH (or reboot it manually).


### Configuration

In the UI just enter your credentials, they're getting saved automatically.

The command line interface allows persistant configuration using the `config-auth` sub-command:

```
qrm config-auth host=192.168.178.13 password='s0rry_Pl4in+ex+!'
```

Please note that currently only connection via IP address (rather than hostname) and plaintext
password is working. This is subject to change ("of course").


## ToDo for v1.0

* Allow hostnames instead of IP addresses
* Make use of shared keys and configuration in `~/.ssh/config`
* Support drag&drop to add content in UI
* Support deletion
* Support Pdf
* Support web pages via Pdf


## Future features

* Download and manage notes
* Make backups
* Other convenience stuff via SSH, e.g. installing software


## Installation

```
pip3 install [--user] [--upgrade] qrm
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
