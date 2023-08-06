# -*- coding=utf-8 -*-

"""Functional testing with toy examples.

See tests/data/README.md
"""

# pylint: disable=compare-to-zero,missing-raises-doc
import subprocess
from pathlib import Path

from khloraascaf.inputs import INSTANCE_NAME_DEF, SOLVER_CBC
from khloraascaf.lib import DR_REGION_ID, IR_REGION_ID, UN_REGION_ID
from khloraascaf.outputs import (
    fmt_contigs_of_regions_filename,
    fmt_map_of_regions_filename,
)
from khloraascaf.scaffolding_methods import scaffolding
from tests.path_utils import rm


# ============================================================================ #
#                                   CONSTANTS                                  #
# ============================================================================ #
TEST_DIR: Path = Path(__file__).parent.absolute()

_TOY_DATADIR = TEST_DIR / 'data'

# ---------------------------------------------------------------------------- #
#                                    IR - UN                                   #
# ---------------------------------------------------------------------------- #
_IR_UN_DIR = _TOY_DATADIR / 'ir_un'
_IR_UN_CONTIG_ATTRS = _IR_UN_DIR / 'contig_attrs.tsv'
_IR_UN_CONTIG_LINKS = _IR_UN_DIR / 'contig_links.tsv'
_IR_UN_CONTIG_STARTER = 'C0'
_IR_UN_SOL_REGMAP = _IR_UN_DIR / 'map_of_regions_sol.tsv'
_IR_UN_SOL_REGCTG_F = _IR_UN_DIR / 'contigs_of_regions_sol_0.tsv'
_IR_UN_SOL_REGCTG_R = _IR_UN_DIR / 'contigs_of_regions_sol_1.tsv'

# ---------------------------------------------------------------------------- #
#                                    DR - UN                                   #
# ---------------------------------------------------------------------------- #
_DR_UN_DIR = _TOY_DATADIR / 'dr_un'
_DR_UN_CONTIG_ATTRS = _DR_UN_DIR / 'contig_attrs.tsv'
_DR_UN_CONTIG_LINKS = _DR_UN_DIR / 'contig_links.tsv'
_DR_UN_CONTIG_STARTER = 'C0'
_DR_UN_SOL_REGMAP = _DR_UN_DIR / 'map_of_regions_sol.tsv'
_DR_UN_SOL_REGCTG = _DR_UN_DIR / 'contigs_of_regions_sol.tsv'

# ---------------------------------------------------------------------------- #
#                                      UN                                      #
# ---------------------------------------------------------------------------- #
_UN_DIR = _TOY_DATADIR / 'un'
_UN_CONTIG_ATTRS = _UN_DIR / 'contig_attrs.tsv'
_UN_CONTIG_LINKS = _UN_DIR / 'contig_links.tsv'
_UN_CONTIG_STARTER = 'C0'
_UN_SOL_REGMAP = _UN_DIR / 'map_of_regions_sol.tsv'
_UN_SOL_REGCTG = _UN_DIR / 'contigs_of_regions_sol.tsv'

# ---------------------------------------------------------------------------- #
#                                 IR - DR - UN                                 #
# ---------------------------------------------------------------------------- #
_IR_DR_UN_DIR = _TOY_DATADIR / 'ir_dr_un'
_IR_DR_UN_CONTIG_ATTRS = _IR_DR_UN_DIR / 'contig_attrs.tsv'
_IR_DR_UN_CONTIG_LINKS = _IR_DR_UN_DIR / 'contig_links.tsv'
_IR_DR_UN_CONTIG_STARTER = 'C0'
_IR_DR_UN_SOL_REGMAP = _IR_DR_UN_DIR / 'map_of_regions_sol.tsv'
_IR_DR_UN_SOL_REGCTG_F = _IR_DR_UN_DIR / 'contigs_of_regions_sol_0.tsv'
_IR_DR_UN_SOL_REGCTG_R = _IR_DR_UN_DIR / 'contigs_of_regions_sol_1.tsv'

# ---------------------------------------------------------------------------- #
#                                 DR - IR - UN                                 #
# ---------------------------------------------------------------------------- #
_DR_IR_UN_DIR = _TOY_DATADIR / 'dr_ir_un'
_DR_IR_UN_CONTIG_ATTRS = _DR_IR_UN_DIR / 'contig_attrs.tsv'
_DR_IR_UN_CONTIG_LINKS = _DR_IR_UN_DIR / 'contig_links.tsv'
_DR_IR_UN_CONTIG_STARTER = 'C0'
_DR_IR_UN_SOL_REGMAP = _DR_IR_UN_DIR / 'map_of_regions_sol.tsv'
_DR_IR_UN_SOL_REGCTG_F = _DR_IR_UN_DIR / 'contigs_of_regions_sol_0.tsv'
_DR_IR_UN_SOL_REGCTG_R = _DR_IR_UN_DIR / 'contigs_of_regions_sol_1.tsv'


# ============================================================================ #
#                                TEST FUNCTIONS                                #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                                    IR - UN                                   #
# ---------------------------------------------------------------------------- #
def test_ir_un_func():
    """Test IR-UN toy example."""
    outdir = _IR_UN_DIR / 'tmp'
    outdir.mkdir(exist_ok=True)
    outdir_gen = scaffolding(
        _IR_UN_CONTIG_ATTRS,
        _IR_UN_CONTIG_LINKS,
        _IR_UN_CONTIG_STARTER,
        solver=SOLVER_CBC,
        outdir=outdir,
        instance_name=INSTANCE_NAME_DEF,
        debug=True,
    )
    # TOTEST verify all the debug file
    verify_scaffolding_ir_un(outdir_gen)
    rm(outdir)


def test_ir_un_cli():
    """Test IR-UN toy example for cli."""
    outdir = _IR_UN_DIR / 'tmp'
    outdir.mkdir(exist_ok=True)
    try:
        proc = subprocess.run(
            [
                'python3',
                '-m',
                'khloraascaf',
                _IR_UN_CONTIG_ATTRS,
                _IR_UN_CONTIG_LINKS,
                _IR_UN_CONTIG_STARTER,
                '--solver',
                SOLVER_CBC,
                '--debug',
                '--out-directory',
                outdir,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as err:
        raise AssertionError() from err
    outdir_gen = Path(proc.stdout.splitlines()[-1])
    verify_scaffolding_ir_un(outdir_gen)
    rm(outdir)


def verify_scaffolding_ir_un(outdir_gen: Path):
    """Verify scaffolding IR-UN.

    Parameters
    ----------
    outdir_gen : Path
        Output directory
    """
    #
    # Test output files
    #
    assert {p.name for p in outdir_gen.glob('*')} == {
        'all_scaffolding.yaml',
        'contigs_of_regions_khloraascaf_ir_un.tsv',
        'io_config.yaml',
        'map_of_regions_khloraascaf_dr.tsv',
        'map_of_regions_khloraascaf_ir_dr.tsv',
        'map_of_regions_khloraascaf_ir_un.tsv',
        'map_of_regions_khloraascaf_ir.tsv',
        'repfrag_khloraascaf_dr.tsv',
        'repfrag_khloraascaf_ir_dr.tsv',
        'repfrag_khloraascaf_ir.tsv',
        'solutions.yaml',
        'solver_cbc_khloraascaf_dr.log',
        'solver_cbc_khloraascaf_ir_dr.log',
        'solver_cbc_khloraascaf_ir_un.log',
        'solver_cbc_khloraascaf_ir.log',
        'vertices_of_regions_khloraascaf_dr.tsv',
        'vertices_of_regions_khloraascaf_ir_dr.tsv',
        'vertices_of_regions_khloraascaf_ir_un.tsv',
        'vertices_of_regions_khloraascaf_ir.tsv',
    }
    #
    # Test maps of regions
    #
    res_map_of_regions = outdir_gen / fmt_map_of_regions_filename(
        INSTANCE_NAME_DEF, (IR_REGION_ID, UN_REGION_ID),
    )
    l_sol_map = []
    with open(_IR_UN_SOL_REGMAP, 'r', encoding='utf-8') as sol_map:
        for line in sol_map:
            l_sol_map.append(line.split())
    l_res_map = []
    with open(res_map_of_regions, 'r', encoding='utf-8') as res_map:
        for line in res_map:
            l_res_map.append(line.split())
    assert l_sol_map == l_res_map
    #
    # Test contigs of region
    #
    res_contigs_of_regions = outdir_gen / fmt_contigs_of_regions_filename(
        INSTANCE_NAME_DEF, (IR_REGION_ID, UN_REGION_ID),
    )
    l_sol_ctg_f = []
    with open(_IR_UN_SOL_REGCTG_F, 'r', encoding='utf-8') as sol_ctg:
        for line in sol_ctg:
            l_sol_ctg_f.append(line.split())
    l_sol_ctg_r = []
    with open(_IR_UN_SOL_REGCTG_R, 'r', encoding='utf-8') as sol_ctg:
        for line in sol_ctg:
            l_sol_ctg_r.append(line.split())
    l_res_ctg = []
    with open(res_contigs_of_regions, 'r', encoding='utf-8') as res_ctg:
        for line in res_ctg:
            l_res_ctg.append(line.split())
    assert l_res_ctg in (l_sol_ctg_f, l_sol_ctg_r)


# ---------------------------------------------------------------------------- #
#                                    DR - UN                                   #
# ---------------------------------------------------------------------------- #
def test_dr_un_func():
    """Test DR-UN toy example."""
    outdir = _DR_UN_DIR / 'tmp'
    outdir.mkdir(exist_ok=True)
    outdir_gen = scaffolding(
        _DR_UN_CONTIG_ATTRS,
        _DR_UN_CONTIG_LINKS,
        _DR_UN_CONTIG_STARTER,
        solver=SOLVER_CBC,
        debug=True,
        outdir=outdir,
    )
    verify_scaffolding_dr_un(outdir_gen)
    rm(outdir)


def test_dr_un_cli():
    """Test DR-UN toy example for cli."""
    outdir = _DR_UN_DIR / 'tmp'
    outdir.mkdir(exist_ok=True)
    try:
        proc = subprocess.run(
            [
                'python3',
                '-m',
                'khloraascaf',
                _DR_UN_CONTIG_ATTRS,
                _DR_UN_CONTIG_LINKS,
                _DR_UN_CONTIG_STARTER,
                '--solver',
                SOLVER_CBC,
                '--debug',
                '--out-directory',
                outdir,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as err:
        raise AssertionError() from err
    outdir_gen = Path(proc.stdout.splitlines()[-1])
    verify_scaffolding_dr_un(outdir_gen)
    rm(outdir)


def verify_scaffolding_dr_un(outdir_gen: Path):
    """Verify scaffolding DR-UN.

    Parameters
    ----------
    outdir_gen : Path
        Output directory
    """
    #
    # Test output files
    #
    assert {p.name for p in outdir_gen.glob('*')} == {
        'all_scaffolding.yaml',
        'contigs_of_regions_khloraascaf_dr_un.tsv',
        'io_config.yaml',
        'map_of_regions_khloraascaf_dr_ir.tsv',
        'map_of_regions_khloraascaf_dr_un.tsv',
        'map_of_regions_khloraascaf_dr.tsv',
        'map_of_regions_khloraascaf_ir.tsv',
        'repfrag_khloraascaf_dr_ir.tsv',
        'repfrag_khloraascaf_dr.tsv',
        'repfrag_khloraascaf_ir.tsv',
        'solutions.yaml',
        'solver_cbc_khloraascaf_dr_ir.log',
        'solver_cbc_khloraascaf_dr.log',
        'solver_cbc_khloraascaf_ir.log',
        'solver_cbc_khloraascaf_dr_un.log',
        'vertices_of_regions_khloraascaf_dr_ir.tsv',
        'vertices_of_regions_khloraascaf_dr.tsv',
        'vertices_of_regions_khloraascaf_ir.tsv',
        'vertices_of_regions_khloraascaf_dr_un.tsv',
    }
    #
    # Test map of regions
    #
    res_map_of_regions = outdir_gen / fmt_map_of_regions_filename(
        INSTANCE_NAME_DEF, (DR_REGION_ID, UN_REGION_ID),
    )
    l_sol_map = []
    with open(_DR_UN_SOL_REGMAP, 'r', encoding='utf-8') as sol_map:
        for line in sol_map:
            l_sol_map.append(line.split())
    l_res_map = []
    with open(res_map_of_regions, 'r', encoding='utf-8') as res_map:
        for line in res_map:
            l_res_map.append(line.split())
    assert l_sol_map == l_res_map
    #
    # Test contigs of regions
    #
    res_contigs_of_regions = outdir_gen / fmt_contigs_of_regions_filename(
        INSTANCE_NAME_DEF, (DR_REGION_ID, UN_REGION_ID),
    )
    l_sol_ctg = []
    with open(_DR_UN_SOL_REGCTG, 'r', encoding='utf-8') as sol_ctg:
        for line in sol_ctg:
            l_sol_ctg.append(line.split())
    l_res_ctg = []
    with open(res_contigs_of_regions, 'r', encoding='utf-8') as res_ctg:
        for line in res_ctg:
            l_res_ctg.append(line.split())
    assert l_res_ctg == l_sol_ctg


# ---------------------------------------------------------------------------- #
#                                      UN                                      #
# ---------------------------------------------------------------------------- #
def test_un_func():
    """Test UN toy example."""
    outdir = _UN_DIR / 'tmp'
    outdir.mkdir(exist_ok=True)
    outdir_gen = scaffolding(
        _UN_CONTIG_ATTRS,
        _UN_CONTIG_LINKS,
        _UN_CONTIG_STARTER,
        solver=SOLVER_CBC,
        debug=True,
        outdir=outdir,
    )
    verify_scaffolding_un(outdir_gen)
    rm(outdir)


def test_un_cli():
    """Test UN toy example for cli."""
    outdir = _UN_DIR / 'tmp'
    outdir.mkdir(exist_ok=True)
    try:
        proc = subprocess.run(
            [
                'python3',
                '-m',
                'khloraascaf',
                _UN_CONTIG_ATTRS,
                _UN_CONTIG_LINKS,
                _UN_CONTIG_STARTER,
                '--solver',
                SOLVER_CBC,
                '--debug',
                '--out-directory',
                outdir,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as err:
        raise AssertionError() from err
    outdir_gen = Path(proc.stdout.splitlines()[-1])
    verify_scaffolding_un(outdir_gen)
    rm(outdir)


def verify_scaffolding_un(outdir_gen: Path):
    """Verify scaffolding UN.

    Parameters
    ----------
    outdir_gen : Path
        Output directory
    """
    #
    # Test output files
    #
    assert {p.name for p in outdir_gen.glob('*')} == {
        'all_scaffolding.yaml',
        'contigs_of_regions_khloraascaf_un.tsv',
        'io_config.yaml',
        'map_of_regions_khloraascaf_dr.tsv',
        'map_of_regions_khloraascaf_ir.tsv',
        'map_of_regions_khloraascaf_un.tsv',
        'repfrag_khloraascaf_dr.tsv',
        'repfrag_khloraascaf_ir.tsv',
        'solutions.yaml',
        'solver_cbc_khloraascaf_dr.log',
        'solver_cbc_khloraascaf_ir.log',
        'solver_cbc_khloraascaf_un.log',
        'vertices_of_regions_khloraascaf_dr.tsv',
        'vertices_of_regions_khloraascaf_ir.tsv',
        'vertices_of_regions_khloraascaf_un.tsv',
    }
    #
    # Test map of regions
    #
    res_map_of_regions = outdir_gen / fmt_map_of_regions_filename(
        INSTANCE_NAME_DEF, (UN_REGION_ID,),
    )
    l_sol_map = []
    with open(_UN_SOL_REGMAP, 'r', encoding='utf-8') as sol_map:
        for line in sol_map:
            l_sol_map.append(line.split())
    l_res_map = []
    with open(res_map_of_regions, 'r', encoding='utf-8') as res_map:
        for line in res_map:
            l_res_map.append(line.split())
    assert l_sol_map == l_res_map
    #
    # Test contigs of regions
    #
    res_contigs_of_regions = outdir_gen / fmt_contigs_of_regions_filename(
        INSTANCE_NAME_DEF, (UN_REGION_ID,),
    )
    l_sol_ctg = []
    with open(_UN_SOL_REGCTG, 'r', encoding='utf-8') as sol_ctg:
        for line in sol_ctg:
            l_sol_ctg.append(line.split())
    l_res_ctg = []
    with open(res_contigs_of_regions, 'r', encoding='utf-8') as res_ctg:
        for line in res_ctg:
            l_res_ctg.append(line.split())
    assert l_res_ctg == l_sol_ctg


# ---------------------------------------------------------------------------- #
#                                 IR - DR - UN                                 #
# ---------------------------------------------------------------------------- #
def test_ir_dr_un_func():
    """Test IR-DR-UN toy example."""
    outdir = _IR_DR_UN_DIR / 'tmp'
    outdir.mkdir(exist_ok=True)
    outdir_gen = scaffolding(
        _IR_DR_UN_CONTIG_ATTRS,
        _IR_DR_UN_CONTIG_LINKS,
        _IR_DR_UN_CONTIG_STARTER,
        solver=SOLVER_CBC,
        outdir=outdir,
        instance_name=INSTANCE_NAME_DEF,
        debug=True,
    )
    # TOTEST verify all the debug file
    verify_scaffolding_ir_dr_un(outdir_gen)
    rm(outdir)


def test_ir_dr_un_cli():
    """Test IR-DR-UN alone toy example for cli."""
    outdir = _IR_DR_UN_DIR / 'tmp'
    outdir.mkdir(exist_ok=True)
    try:
        proc = subprocess.run(
            [
                'python3',
                '-m',
                'khloraascaf',
                _IR_DR_UN_CONTIG_ATTRS,
                _IR_DR_UN_CONTIG_LINKS,
                _IR_DR_UN_CONTIG_STARTER,
                '--solver',
                SOLVER_CBC,
                '--debug',
                '--out-directory',
                outdir,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as err:
        raise AssertionError() from err
    outdir_gen = Path(proc.stdout.splitlines()[-1])
    verify_scaffolding_ir_dr_un(outdir_gen)
    rm(outdir)


def verify_scaffolding_ir_dr_un(outdir_gen: Path):
    """Verify scaffolding IR-DR-UN.

    Parameters
    ----------
    outdir_gen : Path
        Output directory
    """
    #
    # Test output files
    #
    assert {p.name for p in outdir_gen.glob('*')} == {
        'all_scaffolding.yaml',
        'contigs_of_regions_khloraascaf_ir_dr_un.tsv',
        'io_config.yaml',
        'map_of_regions_khloraascaf_dr.tsv',
        'map_of_regions_khloraascaf_ir_dr_un.tsv',
        'map_of_regions_khloraascaf_ir_dr.tsv',
        'map_of_regions_khloraascaf_ir.tsv',
        'repfrag_khloraascaf_dr.tsv',
        'repfrag_khloraascaf_ir_dr.tsv',
        'repfrag_khloraascaf_ir.tsv',
        'solutions.yaml',
        'solver_cbc_khloraascaf_dr.log',
        'solver_cbc_khloraascaf_ir_dr_un.log',
        'solver_cbc_khloraascaf_ir_dr.log',
        'solver_cbc_khloraascaf_ir.log',
        'vertices_of_regions_khloraascaf_dr.tsv',
        'vertices_of_regions_khloraascaf_ir_dr_un.tsv',
        'vertices_of_regions_khloraascaf_ir_dr.tsv',
        'vertices_of_regions_khloraascaf_ir.tsv',
    }
    #
    # Test maps of regions
    #
    res_map_of_regions = outdir_gen / fmt_map_of_regions_filename(
        INSTANCE_NAME_DEF, (IR_REGION_ID, DR_REGION_ID, UN_REGION_ID),
    )
    l_sol_map = []
    with open(_IR_DR_UN_SOL_REGMAP, 'r', encoding='utf-8') as sol_map:
        for line in sol_map:
            l_sol_map.append(line.split())
    l_res_map = []
    with open(res_map_of_regions, 'r', encoding='utf-8') as res_map:
        for line in res_map:
            l_res_map.append(line.split())
    assert l_sol_map == l_res_map
    #
    # Test contigs of region
    #
    res_contigs_of_regions = outdir_gen / fmt_contigs_of_regions_filename(
        INSTANCE_NAME_DEF, (IR_REGION_ID, DR_REGION_ID, UN_REGION_ID),
    )
    l_sol_ctg_f = []
    with open(_IR_DR_UN_SOL_REGCTG_F, 'r', encoding='utf-8') as sol_ctg:
        for line in sol_ctg:
            l_sol_ctg_f.append(line.split())
    l_sol_ctg_r = []
    with open(_IR_DR_UN_SOL_REGCTG_R, 'r', encoding='utf-8') as sol_ctg:
        for line in sol_ctg:
            l_sol_ctg_r.append(line.split())
    l_res_ctg = []
    with open(res_contigs_of_regions, 'r', encoding='utf-8') as res_ctg:
        for line in res_ctg:
            l_res_ctg.append(line.split())
    assert l_res_ctg in (l_sol_ctg_f, l_sol_ctg_r)


# ---------------------------------------------------------------------------- #
#                                 DR - IR - UN                                 #
# ---------------------------------------------------------------------------- #
def test_dr_ir_un_func():
    """Test DR-IR-UN toy example."""
    outdir = _DR_IR_UN_DIR / 'tmp'
    outdir.mkdir(exist_ok=True)
    outdir_gen = scaffolding(
        _DR_IR_UN_CONTIG_ATTRS,
        _DR_IR_UN_CONTIG_LINKS,
        _DR_IR_UN_CONTIG_STARTER,
        solver=SOLVER_CBC,
        outdir=outdir,
        instance_name=INSTANCE_NAME_DEF,
        debug=True,
    )
    # TOTEST verify all the debug file
    verify_scaffolding_dr_ir_un(outdir_gen)
    rm(outdir)


def test_dr_ir_un_cli():
    """Test DR-IR-UN alone toy example for cli."""
    outdir = _DR_IR_UN_DIR / 'tmp'
    outdir.mkdir(exist_ok=True)
    try:
        proc = subprocess.run(
            [
                'python3',
                '-m',
                'khloraascaf',
                _DR_IR_UN_CONTIG_ATTRS,
                _DR_IR_UN_CONTIG_LINKS,
                _DR_IR_UN_CONTIG_STARTER,
                '--solver',
                SOLVER_CBC,
                '--debug',
                '--out-directory',
                outdir,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as err:
        raise AssertionError() from err
    outdir_gen = Path(proc.stdout.splitlines()[-1])
    verify_scaffolding_dr_ir_un(outdir_gen)
    rm(outdir)


def verify_scaffolding_dr_ir_un(outdir_gen: Path):
    """Verify scaffolding DR-IR-UN.

    Parameters
    ----------
    outdir_gen : Path
        Output directory
    """
    #
    # Test output files
    #
    assert {p.name for p in outdir_gen.glob('*')} == {
        'all_scaffolding.yaml',
        'contigs_of_regions_khloraascaf_dr_ir_un.tsv',
        'io_config.yaml',
        'map_of_regions_khloraascaf_dr_ir_un.tsv',
        'map_of_regions_khloraascaf_dr_ir.tsv',
        'map_of_regions_khloraascaf_dr.tsv',
        'map_of_regions_khloraascaf_ir.tsv',
        'repfrag_khloraascaf_dr_ir.tsv',
        'repfrag_khloraascaf_dr.tsv',
        'repfrag_khloraascaf_ir.tsv',
        'solutions.yaml',
        'solver_cbc_khloraascaf_dr_ir_un.log',
        'solver_cbc_khloraascaf_dr_ir.log',
        'solver_cbc_khloraascaf_dr.log',
        'solver_cbc_khloraascaf_ir.log',
        'vertices_of_regions_khloraascaf_dr_ir_un.tsv',
        'vertices_of_regions_khloraascaf_dr_ir.tsv',
        'vertices_of_regions_khloraascaf_dr.tsv',
        'vertices_of_regions_khloraascaf_ir.tsv',
    }
    #
    # Test maps of regions
    #
    res_map_of_regions = outdir_gen / fmt_map_of_regions_filename(
        INSTANCE_NAME_DEF, (DR_REGION_ID, IR_REGION_ID, UN_REGION_ID),
    )
    l_sol_map = []
    with open(_DR_IR_UN_SOL_REGMAP, 'r', encoding='utf-8') as sol_map:
        for line in sol_map:
            l_sol_map.append(line.split())
    l_res_map = []
    with open(res_map_of_regions, 'r', encoding='utf-8') as res_map:
        for line in res_map:
            l_res_map.append(line.split())
    assert l_sol_map == l_res_map
    #
    # Test contigs of region
    #
    res_contigs_of_regions = outdir_gen / fmt_contigs_of_regions_filename(
        INSTANCE_NAME_DEF, (DR_REGION_ID, IR_REGION_ID, UN_REGION_ID),
    )
    l_sol_ctg_f = []
    with open(_DR_IR_UN_SOL_REGCTG_F, 'r', encoding='utf-8') as sol_ctg:
        for line in sol_ctg:
            l_sol_ctg_f.append(line.split())
    l_sol_ctg_r = []
    with open(_DR_IR_UN_SOL_REGCTG_R, 'r', encoding='utf-8') as sol_ctg:
        for line in sol_ctg:
            l_sol_ctg_r.append(line.split())
    l_res_ctg = []
    with open(res_contigs_of_regions, 'r', encoding='utf-8') as res_ctg:
        for line in res_ctg:
            l_res_ctg.append(line.split())
    assert l_res_ctg in (l_sol_ctg_f, l_sol_ctg_r)
