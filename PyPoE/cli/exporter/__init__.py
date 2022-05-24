"""
GGPK User Interface Classes

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/__init__.py                                   |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Creates a qt User Interface to browse GGPK files.

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
import typing
import warnings

# 3rd-Party
from colorama import init

# self
from PyPoE import APP_DIR
from PyPoE.cli.config import ConfigHelper
from PyPoE.cli.core import OutputHook

# =============================================================================
# Globals
# =============================================================================

__all__: typing.List[str] = ['CONFIG_PATH', 'config']

CONFIG_PATH = os.path.join(APP_DIR, 'exporter.conf')

config = ConfigHelper(infile=CONFIG_PATH)

# =============================================================================
# Init
# =============================================================================

init()
OutputHook(warnings.showwarning)
