# FILE: /my-python-package/my-python-package/my_python_package/__init__.py
"""
my_python_package

This package provides functionality to parse .mat files generated from CONN first-level ROI-to-ROI analyses
and output them in a format suitable for COMBAT harmonization.

Modules:
- extract_first_levels: Contains functions for extracting and processing ROI data.
"""

from .extract_first_levels import extract  # Importing functions for easier access at the package level.