#!/usr/bin/env python3
"""Compatibility entry point for the safe primary virtual mouse implementation.

The former independent implementation enabled desktop control on startup. Keep
this filename for existing users, but delegate to ``main.py`` so both entry
points share the same opt-in controls and failsafe behavior.
"""

from main import VirtualMouse


if __name__ == "__main__":
    VirtualMouse().run()
