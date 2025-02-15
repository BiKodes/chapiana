The Changelog
---------------

Commit Messages
~~~~~~~~~~~~~~~

Recommended format for the commit message:

    <type>(<scope>): <subject>

    <body>

    <footer>

Allowed <type> values:

- feat: New feature
- fix: Bug fix
- docs: Changes to documentation
- style: Formatting, missing semi colons, etc; no code change
- refactor: Refactoring production code
- test: Adding missing tests, refactoring tests; no production code change
- chore: Updating grunt tasks etc; no production code change
- revert: Undoing changes made in a previous commit
- perf: Changes regarding performance
- build: Indicates changes related to the build system
- ci: Changes regarding continuous integration setup or configuration
- deps: Changes related to dependencies

More details `here <https://karma-runner.github.io/0.10/dev/git-commit-msg.html>`_ (licensed under MIT licence).


Versioning
~~~~~~~~~~

Recommended versioning system: `Semantic Versioning <https://semver.org/>`_.

Given a version number MAJOR.MINOR.PATCH, increment the:

- MAJOR version when you make incompatible API changes,
- MINOR version when you add functionality in a backwards compatible manner, and
- PATCH version when you make backwards compatible bug fixes.

Additional labels for pre-release and build metadata are available as extensions to the `MAJOR.MINOR.PATCH` format.
