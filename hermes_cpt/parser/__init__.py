"""
.. module:: hermes_cpt.parser.__init__.py
   :copyright: Copyright "Sep 21, 2019", Institute Pierre Simon Laplace
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: CPT parsing sub-package.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.fr>


"""
import os

from hermes_cpt.constants import HPC_TGCC
from hermes_cpt.parser import tgcc as parser_tgcc



# Map of HPC identifiers to cpt parsers.
_PARSERS = {
    HPC_TGCC: parser_tgcc
}


def parse(centre, cpt):
    """Returns conso blocks extracted from a CPT file.

    :param str centre: HPC node, e.g. tgcc.
    :param str cpt: Either a CPT file path or CPT file contents.

    """
    centre = str(centre).lower()
    try:
        parser = _PARSERS[centre]
    except KeyError:
        raise KeyError("Unsupported HPC: {}".format(centre))
    cpt = _get_cpt_content(cpt)

    return parser.get_consumption(cpt)


def _get_cpt_content(cpt):
    """Returns raw CPT file information ready to be parsed.

    """
    # Open file (if necessary).
    if os.path.isfile(cpt):
        with open(cpt, 'r') as fstream:
            cpt = fstream.read()

    # Strip empty lines & convert all text to lower case.
    return [l.strip() for l in cpt.split('\n') if l.strip()]


__all__ = ["parse"]
