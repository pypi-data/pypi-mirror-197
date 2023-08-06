"""Top-level module for wtforglib Library."""
import json
from pathlib import Path
from tempfile import TemporaryFile
from typing import Optional, Tuple

import yaml

from wtforglib.errors import raise_filenotfound
from wtforglib.kinds import Fspec, StrAnyDict


def load_yaml_file(
    filenm: Fspec,
    missing_ok: bool = True,
) -> StrAnyDict:
    """Loads a yaml file.

    Parameters
    ----------
    filenm : Fspec
        The yaml file to load
    missing_ok : bool optional default True
        When False and file does not exist raises FileNotFound exeception

    Returns
    -------
    StrAnyDict
        Representing contents of filenm
    """
    ypath = Path(filenm)
    yaml_result = {}
    if ypath.exists() and ypath.is_file():
        with open(ypath, "r") as yfile:
            yaml_result = yaml.safe_load(yfile)
    elif not missing_ok:  # pragma no cover
        raise_filenotfound(ypath)
    return yaml_result


def write_yaml_file(
    filenm: Fspec,
    src_data: StrAnyDict,
    encoding: str = "utf-8",
) -> bool:
    """Writes src_data to a file in a yaml format.

    Parameters
    ----------
    filenm : Fspec
        The yaml filename to write to
    src_data : StrAnyDict
        The data to write to a file
    encoding : str Optional
        encoding default 'utf-8'

    Returns
    -------
        bool
            True if file exists else False
    """
    ypath = Path(filenm)
    with open(ypath, "w") as outf:
        yaml.dump(src_data, outf, encoding=encoding)
    return ypath.exists()


def load_json_file(
    filenm: Fspec,
    missing_ok: bool = True,
) -> StrAnyDict:
    """Loads a json file.

    Parameters
    ----------
    filenm : Fspec
        The yaml file to load
    missing_ok : bool optional default True
        When False and file does not exist raises FileNotFound exeception

    Returns
    -------
    StrAnyDict
        Representing contents of filenm
    """
    jpath = Path(filenm)
    rtn: StrAnyDict = {}
    if jpath.exists() and jpath.is_file():
        with open(jpath, "r") as jfile:
            rtn = json.load(jfile)
    elif not missing_ok:  # pragma no cover
        raise_filenotfound(jpath)
    return rtn


def write_json_file(
    filenm: Fspec,
    src_data: StrAnyDict,
    indent: int = 2,
) -> bool:
    """Writes src_data to a file in a json format.

    Parameters
    ----------
    filenm : Fspec
        The json filename to write to
    src_data : StrAnyDict
        The data to write to a file
    indent : int Optional
        The number of spaces to indent

    Returns
    -------
        bool
            True if file exists else False
    """
    jpath = Path(filenm)
    with open(jpath, "w") as outf:
        outf.write(json.dumps(src_data, indent=2))
    return jpath.exists()


def ensure_directory(target: Fspec, perm: int = 0o755) -> bool:
    """Creates a directory if it doesn't exist.

    Parameters
    ----------
    target : Fspec
        The path to the target directory
    perm : int Optional
        The mode to use if creationg needed

    Returns
    -------
    bool
        True if directory exists

    Raises
    ------
    NotADirectoryError
        if target exists, but not a directory
    """
    dp = Path(target)
    if dp.is_dir():
        return True
    if dp.exists():
        raise NotADirectoryError(
            'Pathname "{0}" is not a directory.'.format(str(target)),
        )
    dp.mkdir(mode=perm, parents=True)
    return True


def _verify_directory_write(dpath: Fspec) -> Optional[Exception]:
    """Verify that the given directory is writable.

    Parameters
    ----------
    dpath : Fspec
        Pathlike object specifying the directory

    Returns
    -------
    Optional[Exception]
        The exception when caught
    """
    error: Optional[Exception] = None
    try:
        tfile = TemporaryFile(dir=dpath)
        tfile.close()
    except Exception as ex:
        error = ex
    return error


def verify_directory(dspec: Fspec, ex: bool = False) -> Tuple[bool, str]:
    """Verify that a directory exits and is writable.

    Parameters
    ----------
    dspec : Fspec
        Pathlike object specifying the directory
    ex : bool, optional
        When True exceptions are raised, by default False

    Returns
    -------
    Tuple[bool, str]
        When ex is False the status is returned

    Raises
    ------
    error
        NotADirectoryError, FileNotFoundError or other exception is raised on failure
        when ex is True
    """
    dpath = Path(dspec)
    dstr = str(dpath)
    error: Optional[Exception] = None
    if dpath.exists():
        if dpath.is_dir():
            error = _verify_directory_write(dpath)
        else:
            error = NotADirectoryError("'{0}' is not a directory".format(dstr))
    else:
        error = FileNotFoundError("Directory not found: {0}".format(dpath))
    if error:
        if ex:
            raise error
    return (error is None, str(error))
