import pytest
import sidpy
import SciFiReaders as sr
from pywget import wget
import os

#TODO: Change this file to be a simpel 2x2 force curve file acquired on one of teh Veros, and put it in SciFiDatasets repo.
#This file is way too large at the moment

@pytest.fixture
def arhdf5_file():
    file_path = 'PTO_SS_00.h5'
    wget.download('https://www.dropbox.com/scl/fi/r4dcstilxsdg8un2nl7g0/PTO_SS_00.h5?rlkey=y4gmc0zq1vpvm8hzrigk5quy3&dl=1', out=file_path)
    yield file_path
    os.remove(file_path)

def test_load_test_arhdf5_file(arhdf5_file):
    data_translator = sr.ARhdf5Reader(arhdf5_file)
    datasets = data_translator.read(verbose=False)
    test_data = datasets[1:6]
    assert len(test_data) == 5, f"Length of dataset should be 5 but is instead {len(test_data)}"
    channel_names = ['Defl', 'Amp', 'Phase', 'Phas2', 'Freq']
    channel_units = ['m', 'm', 'deg', 'deg', 'Hz']
    channel_labels = [['x (m)', 'y (m)', 'z (s)'], ['x (m)', 'y (m)', 'z (s)'], ['x (m)', 'y (m)', 'z (s)'], ['x (m)', 'y (m)', 'z (s)'], ['x (m)', 'y (m)', 'z (s)']]
    for ind, dataset in enumerate(test_data):
        assert isinstance(dataset, sidpy.sid.dataset.Dataset), f"Dataset No. {ind} not read in as sidpy dataset but was instead read in as {type(dataset)}"
        assert dataset.shape[0] == 64, f"Dataset[{ind}] is of size 64 but was read in as {dataset.shape[0]}"
        assert isinstance(dataset._axes[0], sidpy.sid.dimension.Dimension), "Dataset should have dimension type of sidpy Dimension, but is instead {}".format(type(dataset._axes))
        assert dataset.quantity == channel_names[ind], "Dataset having inconsistent channel names"
        assert dataset.units == channel_units[ind], "Dataset having inconsistent unit names"
        assert dataset.labels == channel_labels[ind], "Dataset having inconsistent channel labels"
