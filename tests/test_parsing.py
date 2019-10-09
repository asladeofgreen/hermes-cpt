"""
.. module:: test_parsing.py
   :copyright: Copyright "Sep 21, 2019", Institute Pierre Simon Laplace
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: Top level CPT parsing tests.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.fr>


"""
import inspect

import pytest

import hermes_cpt as hcpt



def test_import():
    """Test imports.

    """
    assert inspect.isfunction(hcpt.parse)


@pytest.mark.parametrize("hpc_identifier", ('XXX', 123))
def test_invalid_hpc_identifier(hpc_identifier):
    """Test parsing an invalid HPC identifier.

    """
    with pytest.raises(KeyError):
        hcpt.parse(hpc_identifier, None)


@pytest.mark.parametrize("cpt_content", (None, 123))
def test_invalid_cpt_content(cpt_content):
    """Test parsing an invalid CPT content.

    """
    with pytest.raises(KeyError):
        hcpt.parse(cpt_content, None)
