#!/usr/bin/env python3
"""Print the install command for one repo (from its README, else generic).

Usage: install_cmd.py <owner/repo>
Reuses spill_repo_carousel.readme_install so the reel terminal shows
the same command as the carousel slide.
"""
import sys

from spill_repo_carousel import readme_install

full = sys.argv[1]
print(readme_install(full) or f"npx skills add {full} -g")
