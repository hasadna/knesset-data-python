knesset-data python module
==========================

[![Build Status](https://travis-ci.org/hasadna/knesset-data-python.svg?branch=master)](https://travis-ci.org/hasadna/knesset-data-python)

A python module that provides api to available Israeli Parliament (Knesset) data

This module provides low-level APIs to support other higher-level modules from the [Knesset data project](https://github.com/hasadna/knesset-data/blob/master/README.md)

### Installation
* $ pip install knesset-data

#### Usage Example
* $ python
* >>> from knesset_data.dataservice.committees import Committee
* >>> committees = list(Committee.get_all_active_committees())
* >>> len(committees)
* 19
* >>> print committees[0].name
* ועדת הכנסת

### Known issues / FAQ / Common problems
* [what logic should knesset-data-python be responsible for?](https://github.com/hasadna/knesset-data-python/issues/6)

### Contributing

See the [contribution guide](https://github.com/hasadna/knesset-data-python/blob/master/CONTRIBUTING.md)

### Project Administration

Travis publishes to pypi automatically on every published release (or tag)

#### Publishing a release

* merge some pull requests
* create or update the latest draft release (https://github.com/hasadna/knesset-data-python/releases)
  * update the release notes, save draft
* test / update the release
* when ready, publish the release on GitHub
* travis will automatically publish to pypi

#### Updating dependant projects

After publishing a release you probably want to update the dependency in dependant projects

In Open Knesset repository -

* edit [Open-Knesset/requirements.txt](https://github.com/hasadna/Open-Knesset/blob/master/requirements.txt)
* `knesset-data==1.2.0`
* test and open a pull request in Open Knesset

#### More details regarding travis publishing to pypi

The .travis.yml file contains encrypted variables, you add them using the travis cli client:

```
$ git config --local travis.slug hasadna/knesset-data-python
$ travis encrypt TRAVIS_PYPI_USER=(YOUR_PYPI_USER) TRAVIS_PYPI_PASS=(YOUR_PYPI_PASSWORD) --add
$ history -c
```

add the secure env var to .travis.yml

Check out .travis/after_success.sh to see how the publishing to pypi works
