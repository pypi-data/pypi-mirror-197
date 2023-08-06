from pathlib import Path
import globsters


def test_version():
    assert globsters.__version__ is not None
    import tomli

    Path("Cargo.toml").read_text()
    cargo_version = tomli.loads(Path("Cargo.toml").read_text())["package"]["version"]
    assert globsters.__version__ == cargo_version
    pyproject_version = tomli.loads(Path("pyproject.toml").read_text())["project"][
        "version"
    ]
    assert globsters.__version__ == pyproject_version


def test_single_globster():
    matcher = globsters.Globster("*.py")
    assert matcher.is_match("file.py")
    assert not matcher.is_match("file.txt")


def test_single_globster_callable():
    matcher = globsters.Globster("*.py")
    assert matcher("file.py")
    assert not matcher("file.txt")


def test_multiple_globsters():
    globset = globsters.Globsters(["*.py", "*.txt"])
    assert globset.is_match("file.py")
    assert globset.is_match("file.txt")
    assert not globset.is_match("file.exe")


def test_multiple_globsters_callable():
    globset = globsters.Globsters(["*.py", "*.txt"])
    assert globset("file.py")
    assert globset("file.txt")
    assert globset("path/to/a/file.txt")

    assert not globset("file.PY")
    assert not globset("file.TXT")
    assert not globset("file.TxT")
    assert not globset("file.exe")


def test_multiple_globsters_negative():
    globset = globsters.Globsters(["*.py", "!*.txt"])
    assert globset("file.py")
    assert globset("file.txt") is False
    assert not globset("path/to/a/file.txt")
    assert not globset("file.exe")


def test_multiple_globsters_case_insensitive():
    globset = globsters.Globsters(["*.py", "*.txt"], True)
    assert globset("file.py")
    assert globset("file.PY")
    assert globset("file.txt")
    assert globset("file.TXT")
    assert globset("file.TxT")
    assert not globset("file.exe")


def test_glob_paths():
    strings = [
        "/a",
        "/a/sub_aa",
        "/a/sub_aa/aaa",
        "/a/sub_aa/subsub",
        "/b",
        "/c",
    ]
    globber = globsters.globster(["/a/*", "!/a/*/*"], True)
    matches = [el for el in strings if globber(el)]
    assert matches == [
        "/a/sub_aa",
    ]


def dev():
    print(dir(globsters))

    matcher = globsters.Globster("*.py")

    isfile = matcher.is_match("file.py")  # True
    assert isfile
    print(isfile)
    is_not_file = matcher.is_match("file.txt")  # False
    print(is_not_file)
    assert not is_not_file


if __name__ == "__main__":
    dev()
