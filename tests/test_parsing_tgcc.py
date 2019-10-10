"""
.. module:: test_parsing_tgcc.py
   :copyright: Copyright "Sep 21, 2019", Institute Pierre Simon Laplace
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: TGCC specific CPT parsing tests.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.fr>


"""
import hashlib

import pytest

import hermes_cpt as hcpt
from . import utils as tu



@pytest.mark.parametrize("file_suffix", ('01', '02', '03'))
def test_get_files(file_suffix):
    """Test opening target test CPT files.

    """
    cpt = tu.get_cpt_file(hcpt.HPC_TGCC, file_suffix)
    assert isinstance(cpt, str)


@pytest.mark.parametrize("file_suffix", ('01', '02', '03'))
def test_parse_files(file_suffix):
    """Test parsing a relatively simply CPT file.

    """
    fstream = tu.get_cpt_file(hcpt.HPC_TGCC, file_suffix)
    data = hcpt.parse(hcpt.HPC_TGCC, fstream)
    assert isinstance(data, list)
    assert data
    for consumption in data:
        for key in ['hpc', 'project', 'consumption_by_machine']:
            assert key in consumption


@pytest.mark.parametrize("file_suffix", ('01', '02', '03'))
def test_hash_files(file_suffix):
    """Test hashing a relatively simply CPT file.

    """
    fstream = tu.get_cpt_file(hcpt.HPC_TGCC, file_suffix)
    fhash = hashlib.md5(fstream).hexdigest()
    assert len(fhash) == 32
