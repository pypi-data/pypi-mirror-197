# -*- coding=utf-8 -*-

"""Tests for SequenceGraph class."""

from pathlib import Path

from Bio import SeqIO
from khloraascaf.assembly_graph import AssemblyGraph

from khloraascaf_utils.asm_graph_to_fasta import SequenceGraph


# ============================================================================ #
#                                   CONSTANTS                                  #
# ============================================================================ #
TEST_DIR: Path = Path(__file__).parent.absolute()

_DATA_DIR = TEST_DIR / 'data'

# ---------------------------------------------------------------------------- #
#                                    IR - UN                                   #
# ---------------------------------------------------------------------------- #
_IR_UN_DIR = _DATA_DIR / 'ir_un'
_IR_UN_CONTIG_LINKS = _IR_UN_DIR / 'contig_links.tsv'
_IR_UN_CONTIGS_FASTA = _IR_UN_DIR / 'contigs.fasta'
_IR_UN_LINKS_FASTA = _IR_UN_DIR / 'links.fasta'
_IR_UN_SOL_REGMAP = _IR_UN_DIR / 'map_of_regions_sol.tsv'
_IR_UN_SOL_REGCTG_F = _IR_UN_DIR / 'contigs_of_regions_sol_0.tsv'
_IR_UN_FASTA_SOL = _IR_UN_DIR / 'asm_graph_paths.fasta'

# ---------------------------------------------------------------------------- #
#                                    DR - UN                                   #
# ---------------------------------------------------------------------------- #
_DR_UN_DIR = _DATA_DIR / 'dr_un'
_DR_UN_CONTIG_LINKS = _DR_UN_DIR / 'contig_links.tsv'
_DR_UN_CONTIGS_FASTA = _DR_UN_DIR / 'contigs.fasta'
_DR_UN_LINKS_FASTA = _DR_UN_DIR / 'links.fasta'
_DR_UN_SOL_REGMAP = _DR_UN_DIR / 'map_of_regions_sol.tsv'
_DR_UN_SOL_REGCTG = _DR_UN_DIR / 'contigs_of_regions_sol_0.tsv'
_DR_UN_FASTA_SOL = _DR_UN_DIR / 'asm_graph_paths.fasta'


# ============================================================================ #
#                                   FUNCTIONS                                  #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                                    IR - UN                                   #
# ---------------------------------------------------------------------------- #
def test_ir_un_fasta():
    """Test for IR-UN FASTA."""
    asm_graph = AssemblyGraph(_IR_UN_SOL_REGMAP, _IR_UN_SOL_REGCTG_F)
    seq_graph = SequenceGraph(
        asm_graph, _IR_UN_CONTIGS_FASTA,
        _IR_UN_CONTIG_LINKS, _IR_UN_LINKS_FASTA,
    )
    seq_sol = {
        str(record.seq)
        for record in SeqIO.parse(_IR_UN_FASTA_SOL, 'fasta')
    }
    for region_path in asm_graph.all_region_paths():
        print(seq_graph.region_path_to_seq(region_path))
        assert str(seq_graph.region_path_to_seq(region_path)) in seq_sol


# ---------------------------------------------------------------------------- #
#                                    DR - UN                                   #
# ---------------------------------------------------------------------------- #
def test_dr_un_fasta():
    """Test for DR-UN FASTA."""
    asm_graph = AssemblyGraph(_DR_UN_SOL_REGMAP, _DR_UN_SOL_REGCTG)
    seq_graph = SequenceGraph(
        asm_graph, _DR_UN_CONTIGS_FASTA,
        _DR_UN_CONTIG_LINKS, _DR_UN_LINKS_FASTA,
    )
    seq_sol = {
        str(record.seq)
        for record in SeqIO.parse(_DR_UN_FASTA_SOL, 'fasta')
    }
    for region_path in asm_graph.all_region_paths():
        print(seq_graph.region_path_to_seq(region_path))
        assert str(seq_graph.region_path_to_seq(region_path)) in seq_sol
