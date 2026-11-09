"""Paths used by every analysis script. Set them with environment variables; defaults assume this layout:
    <repo>/analysis/scripts   this folder
    <repo>/analysis/templates HTML / markdown templates
    <repo>/work               working data folder (inputs downloaded per data/README.md, outputs written here)
SH_WORK    working data folder (was /home/user/repro in the original runs)
SH_SHARED  shared project folder copy (was /mnt/project-files/ShapingHistory/repro); defaults to SH_WORK
SH_FIGS    figure output folder (default <repo>/paper/figures)
SH_PAPER   paper folder (default <repo>/paper)
SH_LIT     local literature texts used for quote checking (not distributed; default <repo>/work/lit)
"""
import os
SCRIPTS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(SCRIPTS, '..', '..'))
TEMPLATES = os.path.join(REPO, 'analysis', 'templates')
WORK = os.environ.get('SH_WORK', os.path.join(REPO, 'work'))
SHARED = os.environ.get('SH_SHARED', WORK)
FIGS = os.environ.get('SH_FIGS', os.path.join(REPO, 'paper', 'figures'))
PAPER = os.environ.get('SH_PAPER', os.path.join(REPO, 'paper'))
LIT = os.environ.get('SH_LIT', os.path.join(WORK, 'lit'))
