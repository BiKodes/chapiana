import os
import webbrowser

from invoke import task


def open_browser(path):
    try:
        from urllib import pathname2url
    except:
        from urllib.request import pathname2url
    webbrowser.open("file://" + pathname2url(os.path.abspath(path)))


@task
def clean_build(c):
    """
    Remove build artifacts.
    """
    c.run("rm -fr build/")
    c.run("rm -fr dist/")
    c.run("rm -fr *.egg-info")


@task
def clean_pyc(c):
    """
    Remove python file artifacts.
    """
    c.run("find . -name '*.pyc' -exec rm -f {} +")
    c.run("find . -name '*.pyo' -exec rm -f {} +")
    c.run("find . -name '*~' -exec rm -f {} +")


@task
def coverage(c):
    """
    check code coverage quickly with the default Python.
    """
    c.run("coverage run --source chapiana runtests.py tests")
    c.run("coverage report -m")
    c.run("coverage html")
    c.run("open htmlcov/index.html")


@task
def test_all(c):
    """
    Run tests on every python version with tox.
    """
    c.run("tox")


@task
def clean(c):
    """
    Remove python file and build artifacts.
    """
    clean_build(c)
    clean_pyc(c)


@task
def unittest(c):
    """
    Run unittests.
    """
    c.run("python3 manage.py test")


@task
def lint(c):
    """
    Check style with flake8.
    """
    c.run("flake8 chapiana tests")

@task
def format(c):
    """
    Fix linting errors.
    """
    c.run("isort && black")

@task
def changelog(c):
    """
    Create and update changelog
    """
    c.run("git-changelog --style conventional \
    --sections feat,fix,revert,refactor,perf,build,ci,deps,docs,style,test \
    --template path:CHANGELOG.md.jinja \
    --bump-latest \
    -o CHANGELOG.md")

@task(help={'bumpsize': 'Bump either for a "feature" or "breaking" change'})
def release(c, bumpsize=''):
    """
    Package and upload a release
    """
    clean(c)
    if bumpsize:
        bumpsize = '--' + bumpsize

    # c.run("bumpversion {bump} --no-input".format(bump=bumpsize))

    import src
    c.run("python3 setup.py sdist bdist_wheel")
    c.run("twine upload dist/* --verbose")

    c.run('git tag -a {version} -m "New version: {version}"'.format(version=src.__version__))
    c.run("git push --tags")
    c.run("git push origin master")

@task
def package(c):
    """
    Packaging chapiana and uploading to PyPI.
    """
    c.run("python3 pyproject.py sdist")
