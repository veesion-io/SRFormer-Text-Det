# Publishing a release

## Set version
Put the version of the release in `setup.py` by respecting https://semver.org/.

Run the tests, if the tests doesn't pass you should not deploy a release but
maybe a pre-release or an alpha to avoid breaking stable release.

Don't forget to update the version number if needed before building. The version number is defined at 3 places:
* in the `setup.py` file at repository root.

Make a commit with the setup.py updated and tag it with the version: `vX.X.X`,
in body of the tag you can add the major changes of this release.

Don't forget to push tags

```
git tag v1.1.0
git push --tags
```

## Build package
Package will be build inside docker container
### For torch 1.13.1
run
`/build_package.sh torch113`

### For torch 1.8.1
run
`./build_package.sh torch18`

## Upload to devpi
At this point you can build and then publish it on devpi:
```
devpi use https://devpi.tooling.veesion.io
devpi login veesion
devpi use veesion/veesion
devpi upload --from-dir dist
```
