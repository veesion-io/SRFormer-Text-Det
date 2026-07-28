# Publishing a release

Since 0.3.0 the package is a plain CPU-only sdist: no C/CUDA extension, no
torch needed at build time, and a single static semver version. Releasing is
two commands away.

## 1. Set the version

Bump `version=` in `setup.py` (single source of truth), respecting
[semver](https://semver.org/). Commit the bump.

Run the tests; if they don't pass you should not deploy a release (use a
pre-release/alpha instead of breaking stable).

## 2. Release

```bash
task release
```

This refuses to run on a dirty tree, prompts for the devpi password when the
session has expired (`veesion` user), tags `vX.Y.Z` from the setup.py
version, pushes the tag, rebuilds the sdist (`task build` also works
standalone) and uploads it to
`https://devpi.tooling.veesion.io/veesion/veesion`.

Consumers install it with:

```bash
pip install AdelaiDet==X.Y.Z \
    --extra-index-url https://devpi.tooling.veesion.io/veesion/veesion/+simple/
```

## Historical note

Up to 0.2.x the version was derived from the torch version found at build
time (`0.2.113` = torch 1.13) and per-python/torch wheels were built in
docker via `build_package.sh` (kept for reference). The 0.3.0 CPU-only
package made both mechanisms obsolete: the sdist installs anywhere the
(already installed) torch runs, with regular build isolation.
