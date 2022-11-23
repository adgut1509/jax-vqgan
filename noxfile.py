import nox

SUPPORTED_PY_VERSIONS = ["3.8", "3.9", "3.10"]
nox.options.sessions = ["test", "test_extended", "lint", "coverage", "mypy", "docs", "lint_nb"]


def _deps(session: nox.Session) -> None:
    session.install("--upgrade", "setuptools", "pip", "wheel")


def _install_dev_packages(session):
    session.install("-r", "requirements.txt")


def _install_test_dependencies(session):
    session.install("pytest==7.2.0", "pytest-cov==4.0.0", "pytest-mock==3.10.0")


def _install_doc_dependencies(session):
    session.install("mkdocs==1.3.1", "mkdocstrings==0.19.0")


@nox.session(python=SUPPORTED_PY_VERSIONS)
def test(session: nox.Session) -> None:
    """Pytesting."""
    _deps(session)
    _install_dev_packages(session)
    _install_test_dependencies(session)

    session.run("pytest", "-m", "not training_long", "tests")


@nox.session(python=SUPPORTED_PY_VERSIONS)
def test_extended(session: nox.Session) -> None:
    """Pytesting. Extended version."""
    _deps(session)
    _install_dev_packages(session)
    _install_test_dependencies(session)

    session.run("pytest", "tests")


@nox.session(python=SUPPORTED_PY_VERSIONS)
def coverage(session: nox.Session) -> None:
    """Coverage analysis."""
    _deps(session)
    _install_dev_packages(session)
    _install_test_dependencies(session)
    session.run("coverage", "erase")
    session.run(
        "coverage",
        "run",
        "--source",
        "modules",
        "--append",
        "-m",
        "pytest",
        "-m",
        "not training_long",
        "tests",
    )
    session.run("coverage", "report", "--fail-under=1", "--ignore-errors")  # 90
    session.run("coverage", "erase")


@nox.session(python=SUPPORTED_PY_VERSIONS)
def mypy(session: nox.Session) -> None:
    """Type check."""
    _deps(session)
    session.install("mypy==0.982")
    """Run mypy."""
    session.run("mypy", "--ignore-missing-imports", "modules", "tests")


@nox.session(python=SUPPORTED_PY_VERSIONS)
def lint(session: nox.Session) -> None:
    """Lint install."""
    _deps(session)
    session.install("flake8==5.0.4")
    """Run mypy."""
    session.run(
        "flake8",
        "--count",
        "--select=F",
        "--show-source",
        "--statistics",
        "--max-line-length=100",
    )


@nox.session(python=SUPPORTED_PY_VERSIONS)
def lint_nb(session: nox.Session) -> None:
    """Lint notebooks."""
    _deps(session)
    session.install(
        "flake8==5.0.4", "black==22.3.0", "isort==5.10.1", "nbqa==1.1.0", "nbconvert==7.2.5"
    )
    """Run mypy."""
    session.run("nbqa", "black", "notebooks")
    session.run("nbqa", "flake8", "--max-line-length=100", "notebooks")
    session.run("nbqa", "isort", "notebooks")
    session.run(
        "jupyter",
        "nbconvert",
        "--clear-output",
        "--inplace",
        "notebooks/visualize.ipynb",
        "notebooks/optimize.ipynb",
    )


@nox.session(python=SUPPORTED_PY_VERSIONS)
def docs(session: nox.Session) -> None:
    """Build documentation."""
    _install_doc_dependencies(session)
    session.run("mkdocs", "build", "--clean")
