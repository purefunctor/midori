"""Nox Configuration."""
import os
from pathlib import Path
import shutil

import nox_poetry as nox


@nox.session(name="pre-commit", python="3.9")
def pre_commit(session: nox.Session) -> None:
    """Run pre-commit hooks excluding flake8."""
    env = {"SKIP": "flake8"}

    session.install("pre-commit")
    session.run_always("pre-commit", "install")
    session.run("pre-commit", "run", "--all-files", env=env)


@nox.session(python="3.9")
def flake8(session: nox.Session) -> None:
    """Lint code using flake8."""
    session.install(
        "flake8",
        "flake8-annotations",
        "flake8-docstrings",
        "flake8-import-order",
    )

    if os.getenv("GITHUB_ACTIONS"):
        format = (
            "::error file=%(path)s,line=%(row)d,col=%(col)d::[flake8] "
            "%(code)s: %(text)s"
        )
        session.run(
            "flake8",
            f"--format={format}",
            *session.posargs,
        )
    else:
        session.run("flake8", *session.posargs)


@nox.session(python=["3.8", "3.9"])
def test(session: nox.Session) -> None:
    """Generate test coverage data."""
    args = session.posargs or ["-vs"]

    session.install("pytest", "pytest_mock", "coverage[toml]", ".")

    try:
        session.run("coverage", "run", "--branch", "--parallel", "-m", "pytest", *args)
    finally:
        if session.interactive:
            session.notify("coverage", posargs=[])


@nox.session(name="coverage", python="3.9")
def coverage(session: nox.Session) -> None:
    """Combine and report coverage data."""
    args = session.posargs or ["report"]

    if not session.posargs and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")

    session.run("coverage", *args)


@nox.session(name="mypy", python=["3.8", "3.9"])
def mypy(session: nox.Session) -> None:
    """Type check code using mypy."""
    args = session.posargs or ["midori", "tests", "docs/conf.py"]
    session.install("mypy", "pytest", ".")
    session.run("mypy", *args)


@nox.session(name="docs-build", python="3.9")
def docs_build(session: nox.Session) -> None:
    """Build documentation."""
    args = session.posargs or ["docs", "docs/_build"]
    session.install("sphinx", "sphinx-click", "sphinx-rtd-theme", ".")

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-build", *args)


@nox.session(name="docs-live", python="3.9")
def docs_live(session: nox.Session) -> None:
    """Build documentation with live reloading."""
    args = session.posargs or ["--open-browser", "docs", "docs/_build"]
    session.install("sphinx", "sphinx-autobuild", "sphinx-rtd-theme", ".")

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-autobuild", *args)
