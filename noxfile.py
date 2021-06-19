"""Nox Configuration."""
import os
from pathlib import Path
import shutil
import sys
from textwrap import dedent

import nox

try:
    from nox_poetry import Session, session
except ImportError:
    message = f"""
    Install `nox-poetry` to run sessions!

    {sys.executable} -m pip install nox-poetry
    """
    raise SystemExit(dedent(message))


nox.needs_version = ">= 2021.6.12"
nox.options.sessions = (
    "pre-commit",
    "flake8",
    "mypy",
    "test",
    "docs-build",
)


@session(name="pre-commit", python="3.9")
def pre_commit(session: Session) -> None:
    """Run pre-commit hooks excluding flake8."""
    env = {"SKIP": "flake8"}

    session.install("pre-commit")
    session.run_always("pre-commit", "install")
    session.run("pre-commit", "run", "--all-files", env=env)


@session(python="3.9")
def flake8(session: Session) -> None:
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


@session(python=["3.8", "3.9"])
def test(session: Session) -> None:
    """Generate test coverage data."""
    args = session.posargs or ["-vs"]

    session.install("pytest", "pytest_mock", "coverage[toml]", ".")

    try:
        session.run("coverage", "run", "--branch", "--parallel", "-m", "pytest", *args)
    finally:
        if session.interactive:
            session.notify("coverage", posargs=[])


@session(name="coverage", python="3.9")
def coverage(session: Session) -> None:
    """Combine and report coverage data."""
    args = session.posargs or ["report"]

    if not session.posargs and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")

    session.run("coverage", *args)


@session(name="mypy", python=["3.8", "3.9"])
def mypy(session: Session) -> None:
    """Type check code using mypy."""
    args = session.posargs or ["midori", "tests", "docs/conf.py"]
    session.install("mypy", "pytest", ".")
    session.run("mypy", *args)


@session(name="docs-build", python="3.9")
def docs_build(session: Session) -> None:
    """Build documentation."""
    args = session.posargs or ["docs", "docs/_build"]
    session.install("sphinx", "sphinx-rtd-theme", ".")

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
