knesset-data python module
==========================

[![Build Status](https://travis-ci.org/hasadna/knesset-data-python.svg?branch=master)](https://travis-ci.org/hasadna/knesset-data-python)

A python module that provides api to available Israeli Parliament (Knesset) data

Part of the [Knesset data project](https://github.com/hasadna/knesset-data/blob/master/README.md)

### Installation
* $ pip install knesset-data

#### Usage Example
* $ python
* >>> from knesset_data.dataservice.committees import Committee
* >>> committees = Committee.get_all_active_committees()
* >>> len(committees)
* 19
* >>> print committees[0].name
* ועדת הכנסת

### Contributing

Check out the [Knesset kata contribution guide](https://github.com/hasadna/knesset-data/blob/master/CONTRIBUTING.md)

### Project Administration

The project should be published to pypi for every release

#### Registering / authenticating with pypi

* Before publishing to pypi you should have a user on [pypi](https://pypi.python.org/pypi)
* Create ~/.pypirc file and paste the following (modify username / password):
```
[distutils]
index-servers=pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = <username>
password = <password>
```
* `chmod 400 ~/.pypirc`
* Ask an authorized user to authorize you to publish to pypi.

#### Publishing a release to pypi

* merge some pull requests
* create or update the latest draft release (https://github.com/hasadna/knesset-data-python/releases)
  * update the release notes, save draft
* edit [/python/setup.py](https://github.com/hasadna/knesset-data-python/edit/master/setup.py)
  * update the version to match the version in the GitHub draft release
* make sure you are publishing latest master
  * `$ cd knesset-data-python`
  * `knesset-data-python$ git checkout master`
  * `knesset-data-python$ git pull hasadna master`
* publish the version to pypi
  * `knesset-data-python$ ./setup.py sdist bdist_wheel upload`
* publish the release on GitHub

#### Updating Open Knesset dependency

After publishing a release you probably want to update it in Open-Knesset

In Open Knesset repository -

* edit [Open-Knesset/requirements.txt](https://github.com/hasadna/Open-Knesset/blob/master/requirements.txt)
* `knesset-data==1.2.0`
* test and open a pull request in Open Knesset
