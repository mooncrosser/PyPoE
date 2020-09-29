"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/file_system.py                                    |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================



Agreement
===============================================================================

See PyPoE/LICENSE

Documentation
===============================================================================

Classes
-------------------------------------------------------------------------------

.. autoclass: FileSystem
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
from enum import IntEnum
from typing import Union, List

# 3rd-party
import brotli

# self
from PyPoE.poe.file.ggpk import GGPKFile
from PyPoE.poe.file.bundle import Index
from PyPoE.poe.file.shared import ParserError

# =============================================================================
# Globals
# =============================================================================

__all__ = ['FileSystem']

# =============================================================================
# Classes
# =============================================================================


class FS_TYPES(IntEnum):
    BUNDLE = 0
    GGPK = 1
    DISK = 2


class FileSystem:
    def __init__(self, root_path):
        self.root_path: str = root_path
        self.ggpk: Union[GGPKFile, None] = None

        ggpk_path = os.path.join(root_path, 'content.ggpk')
        if os.path.exists(os.path.join(root_path, 'content.ggpk')):
            self.ggpk = GGPKFile()
            self.ggpk.read(ggpk_path)
            self.ggpk.directory_build()

        self.index: Union[Index, None] = Index()
        try:
            if self.ggpk:
                self.index.read(self.ggpk[self.index.PATH].record.extract())
            else:
                self.index.read(os.path.join(root_path, self.index.PATH))
        except FileNotFoundError:
            self.index = None

    def get_file(self, path: str) -> bytes:
        if self.index:
            try:
                fr = self.index.get_file_record(path)
            except FileNotFoundError:
                pass
            else:
                if self.ggpk:
                    fr.bundle.read(
                        self.ggpk[fr.bundle.ggpk_path].record.extract()
                    )
                else:
                    fr.bundle.read(os.path.join(
                        self.root_path, fr.bundle.ggpk_path))
                return fr.get_file()

        # If the file is in the index, this section can't be reached
        if self.ggpk:
            try:
                return self.ggpk[path].record.extract()
            except FileNotFoundError:
                pass

        # If no GGPK is loaded or the file isn't within the GGPK, lastly the
        # root directory is tried
        try:
            with open(os.path.join(self.root_path, path), 'rb') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                'Specified file can not be found in the Index, content.ggpk '
                'or disk')

    def extract_dds(self, data: bytes) -> bytes:
        """
        Attempts to extract a .dds from the given data bytes.

        .dds files in the content.ggpk may be compressed with brotli or may be
        a reference to another .dds file.

        This function will take of those kind of files accordingly and try to return
        a file instead.
        If any problems arise an error will be raised instead.

        Parameters
        ----------
        data
            The raw data to extract the dds from.

        Returns
        -------
        bytes
            the uncompressed, dereferenced .dds file data

        Raises
        -------
        ValueError
            If the file data contains a reference, but path_or_ggpk is not specified
        TypeError
            If the file data contains a reference, but path_or_ggpk is of invalid
            type (i.e. not str or :class:`GGPKFile`
        ParserError
            If the uncompressed size does not match the size in the header
        brotli.error
            If whatever bytes were read were not brotli compressed
        """
        # Already a DDS file, so return it
        if data[:4] == b'DDS ':
            return data
        # Is this a reference?
        elif data[:1] == b'*':
            path = data[1:].decode()
            data = self.get_file(path)
            return self.extract_dds(data)
        else:
            size = int.from_bytes(data[:4], 'little')
            dec = brotli.decompress(data[4:])
            if len(dec) != size:
                raise ParserError(
                    'Decompressed size does not match size in the header'
                )
            return dec
