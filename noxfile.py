import os

import nox_poetry as nox


@nox.session(python="3.9")
def pre_commit(session: nox.Session):
    env = {"SKIP": "flake8"}

    session.install("pre-commit")
    session.run_always("pre-commit", "install")
    session.run("pre-commit", "run", "--all-files", env=env)


@nox.session(python="3.9")
def flake8(session: nox.Session):
    session.install(
        "flake8",
        "flake8-annotations",
        "flake8-docstrings",
        "flake8-import-order",
    )

    if os.getenv("GITHUB_ACTIONS"):
        session.run(
            "flake8",
            "midori",
            "tests",
            "--format=::error file=%(path)s,line=%(row)d,col=%(col)d::[flake8] %(code)s: %(text)s",
        )
    else:
        session.run("flake8", "midori", "tests")


@nox.session(python=["3.8", "3.9"])
def test(session: nox.Session):
    session.install("pytest", "pytest_mock", "coverage[toml]", ".")
    session.run("coverage", "run", "--branch", "-m", "pytest", "-vs")
    session.run("coverage", "report", "-m")
