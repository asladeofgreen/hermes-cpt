"""
.. module:: utils.py
   :copyright: Copyright "Sep 21, 2019", Institute Pierre Simon Laplace
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: CPT testing utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.fr>


"""
import os


def get_cpt_file(hpc_identifier, file_suffix):
    """Returns contents of test CPT file.

    """
    path = get_cpt_fpath(hpc_identifier, file_suffix)
    with open(path, 'r') as fstream:
        return fstream.read()


def get_cpt_fpath(hpc_identifier, file_suffix):
    """Returns path to a test CPT file.

    """
    path = os.path.dirname(__file__)
    path = os.path.join(path, 'cpt_files')
    path = os.path.join(path, '{}-{}.txt'.format(hpc_identifier, file_suffix))

    return path


def get_cpt_json_fpath(hpc_identifier, file_suffix):
    """Returns path to a test CPT JSON file.

    """
    path = os.path.dirname(__file__)
    path = os.path.join(path, 'cpt_files_json')
    path = os.path.join(path, '{}-{}.json'.format(hpc_identifier, file_suffix))

    return path
