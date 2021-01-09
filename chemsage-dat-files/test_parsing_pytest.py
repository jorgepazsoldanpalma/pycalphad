# coding: utf-8
import pytest

import pyparsing
pyparsing.ParserElement.enablePackrat(0)
from pycalphad.io.cs_dat import create_cs_dat_grammar, grammar_header

# The number of solution phases here EXCLUDES gas phase if it's not present
# (i.e. the num_soln_phases here may be one less than line 2)
database_filenames = [
    # Reorganized to make passing ones test first
    ("Pb-Sn.dat", 4, 0),  # FACT
    ("C-O.dat", 1, 4),  # Thermochimica
    ("W-Au-Ar-Ne-O_04.dat", 2, 5),  # Thermochimica

    # Highest priority to pass:
    ("CuZnFeCl-Viitala (1).dat", 4, 11),  # https://doi.org/10.1016/j.calphad.2019.101667

    # Data files from FACT documentation
    # See https://gtt-technologies.de/software/chemapp/documentation/online-manual/
    (pytest.param("C-N-O.dat", 1, 2, marks=pytest.mark.xfail)),
    ("C-O-Si.dat", 1, 7),
    ("Fe-C.dat", 4, 2),
    ("Fe2SiO4-Mg2SiO4.dat", 3, 2),
    ("O-H-EA.dat", 2, 1),
    ("Pitzer.dat", 2, 6),
    ("subl-ex.dat", 4, 0),

    # Data files from thermochimica `data/` directory
    # See https://github.com/ornl-cees/thermochimica
    ("FeCuCbase.dat", 6, 4),
    ("FeTiVO.dat", 5, 21),
    ("Kaye_NobleMetals.dat", 9, 8),
    ("ZIRC-noSUBI.dat", 22, 28),
    ("test14.dat", 42, 8),

    # Data files from publications
]


@pytest.mark.parametrize("fn, num_soln_phases, num_stoich_phases", database_filenames)
def test_chemsage_reading(fn, num_soln_phases, num_stoich_phases):
    try:
        with open(fn) as fp:
            lines = fp.read()
            cs_dat_grammar = create_cs_dat_grammar()
            out = cs_dat_grammar.parseString(lines)
    except Exception as e:
        print('fail ' + fn + ' - ', end='')
        print(e)
        raise e
    assert len(out.solution_phases) == num_soln_phases
    assert len(out.stoichiometric_phases) == num_stoich_phases



header_data = [
    # filename, num_soln_phases, num_stoich_phases, num_pure_elements, num_gibbs_coeffs, num_excess_coeffs

    # Highest priority to pass:
    ("CuZnFeCl-Viitala (1).dat", 5, 11, 8, 6, 6),  # https://doi.org/10.1016/j.calphad.2019.101667

    # Data files from FACT documentation
    # See https://gtt-technologies.de/software/chemapp/documentation/online-manual/
    ("Pb-Sn.dat", 5, 0, 2, 6, 2),
    ("C-N-O.dat", 1, 2, 3, 6, 4),
    ("C-O-Si.dat", 1, 7, 3, 6, 1),
    ("Fe-C.dat", 4, 2, 2, 6, 4),
    ("Fe2SiO4-Mg2SiO4.dat", 4, 2, 2, 6, 1),
    ("O-H-EA.dat", 2, 1, 3, 6, 6),
    ("Pitzer.dat", 2, 6, 6, 1, 1),
    ("subl-ex.dat", 5, 0, 3, 4, 4),

    # Data files from thermochimica `data/` directory
    # See https://github.com/ornl-cees/thermochimica
    ("C-O.dat", 1, 4, 2, 6, 6),
    ("W-Au-Ar-Ne-O_04.dat", 3, 5, 5, 6, 6),
    ("FeCuCbase.dat", 7, 4, 3, 6, 6),
    ("FeTiVO.dat", 5, 21, 4, 6, 6),
    ("Kaye_NobleMetals.dat", 9, 8, 4, 6, 6),
    ("ZIRC-noSUBI.dat", 22, 28, 9, 6, 6),
    ("test14.dat", 42, 8, 4, 6, 6),

    # Data files from publications
]
@pytest.mark.parametrize("fn, num_soln_phases, num_stoich_phases, num_pure_elements, num_gibbs_coeffs, num_excess_coeffs", header_data)
def test_header_parsing(fn, num_soln_phases, num_stoich_phases, num_pure_elements, num_gibbs_coeffs, num_excess_coeffs):
    with open(fn) as fp:
        lines = fp.read()
    out = grammar_header().parseString(lines)
    print(out)
    assert len(out.list_soln_species_count) == num_soln_phases
    assert out.num_stoich_phases == num_stoich_phases
    assert len(out.pure_elements) == num_pure_elements
    assert len(out.pure_elements_mass) == num_pure_elements
    assert len(out.gibbs_coefficient_idxs) == num_gibbs_coeffs
    assert len(out.excess_coefficient_idxs) == num_excess_coeffs


