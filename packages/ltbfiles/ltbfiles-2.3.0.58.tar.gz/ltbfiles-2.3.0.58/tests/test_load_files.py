from datetime import datetime, timezone, timedelta
import pytest
import numpy as np
import pandas as pd
import ltbfiles


@pytest.mark.parametrize('sort', (True, False))
def test_load_ary(ary_file, sort):
    y,x,o,head = ltbfiles.read_ltb_ary(ary_file, sort)
    assert len(y) == len(x)
    assert len(y) == len(o)
    assert head['filename'] == ary_file
    x_sorted = np.sort(x)
    assert sort == (x_sorted == x).all()


def test_load_ary_docstr():
    docstr = ltbfiles.read_ltb_ary.__doc__
    assert docstr is not None
    assert "y,x,o,head" in docstr


def test_load_spectra_is_object(ary_file):
    result = ltbfiles.read_ltb_ary(ary_file)
    assert isinstance(result, ltbfiles.Spectra)
    assert isinstance(result.Y, np.ndarray)
    assert isinstance(result.o, np.ndarray)
    assert isinstance(result.x, np.ndarray)
    assert isinstance(result.head, dict)


@pytest.mark.parametrize('sort', (True, False))
def test_load_aryx(files_dir, sort):
    filename = files_dir / "noise.aryx"
    y,x,o,head = ltbfiles.read_ltb_aryx(filename, sort)
    assert len(y) == len(x)
    assert len(y) == len(o)
    assert head['filename'] == filename
    x_sorted = np.sort(x)
    assert sort == (x_sorted == x).all()


def test_load_aryx_time_zone(files_dir):
    filename = files_dir / "whitelight.aryx"
    spec = ltbfiles.read_ltb_aryx(filename)
    assert spec.head['measure']['ISOFormat'][-1] == "Z"
    timestamp = pd.to_datetime(spec.head['measure']['ISOFormat'])
    naive_time_str = f"{spec.head['measure']['Date']} {spec.head['measure']['TimeStamp']}"
    tz = timezone(timedelta(hours=+2), name="CEST")
    from_naive = datetime.strptime(naive_time_str, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=tz)
    assert timestamp == from_naive


def test_load_aryx_docstr():
    docstr = ltbfiles.read_ltb_aryx.__doc__
    assert docstr is not None
    assert "y,x,o,head" in docstr


@pytest.mark.parametrize('file', ('steel.ary','noise.aryx'))
def test_load_multi_spec(files_dir, file):
    filenames = [files_dir / file] * 2
    data, wl, o, head = ltbfiles.load_files(filenames)
    assert 2 == data.shape[1]
    assert 1 == len(wl.shape)
    assert 1 == len(o.shape)
    assert data.shape[0] == len(wl)
    assert 2 == len(head)
    increasing = all(x1<x2 for x1, x2 in zip(wl, wl[1:]))
    assert increasing
    names_recovered = [part['filename'] for part in head]
    assert names_recovered == filenames


@pytest.mark.parametrize('file', ('steel.ary','noise.aryx'))
def test_load_files_single(files_dir, file):
    filenames = files_dir / file
    data, wl, o, head = ltbfiles.load_files([filenames])
    assert 1 == data.shape[1]
    assert 1 == len(wl.shape)
    assert 1 == len(o.shape)
    assert data.shape[0] == len(wl)
    assert 1 == len(head)
    names_recovered = [part['filename'] for part in head]
    assert names_recovered[0] == filenames


def test_load_files_docstr():
    docstr = ltbfiles.load_files.__doc__
    assert docstr is not None
    assert "Y,x,o,head" in docstr


@pytest.mark.parametrize("file", [["foo.bar"], "foo.bar"])
def test_load_files_wrong_type(file):
    with pytest.raises(Exception) as excinfo:
        ltbfiles.load_files(file)
    assert "Unknown file extension '.bar'" == excinfo.value.args[0]


def test_find_spectra_in_folder(files_dir):
    filelist = ltbfiles.find_spectra_in_folder(files_dir)
    assert 3 == len(filelist)


def test_find_spectra_in_folder_selected(files_dir):
    filelist = ltbfiles.find_spectra_in_folder(files_dir, ['.aryx'])
    assert 2 == len(filelist)


@pytest.mark.parametrize(('ext','num'), [('.ary',1), ('.aryx',2)])
def test_load_folder(files_dir, ext, num):
    loaded = ltbfiles.load_folder(files_dir, [ext])
    assert loaded is not None
    assert isinstance(loaded, ltbfiles.Spectra)
    assert isinstance(loaded.Y, np.ndarray)
    assert loaded.Y.shape[1] == num
    assert len(loaded.head) == num
    assert isinstance(loaded.head[0], dict)


def test_load_folder_no_spec(files_dir):
    loaded = ltbfiles.load_folder(files_dir, ['.foo'])
    assert loaded is None


def test_load_non_matching_folder(files_dir):
    with pytest.raises(Exception) as excinfo:
        ltbfiles.load_folder(files_dir)
    assert str(files_dir) in excinfo.value.args[0]


def test_load_rawx(files_dir):
    filename = files_dir / 'deuterium.rawx'
    img, head = ltbfiles.read_ltb_rawx(filename)
    assert (2048, 512) == img.shape
    assert isinstance(head, dict)
    assert 2 == len(head)
