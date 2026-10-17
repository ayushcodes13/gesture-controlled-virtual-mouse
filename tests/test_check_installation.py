import io
import unittest
from contextlib import redirect_stdout
from collections import namedtuple
from unittest.mock import patch

import check_installation


VersionInfo = namedtuple(
    "VersionInfo", "major minor micro releaselevel serial"
)


class CheckPythonVersionTests(unittest.TestCase):
    def run_check(self, version):
        output = io.StringIO()
        with patch.object(check_installation.sys, "version_info", version):
            with redirect_stdout(output):
                compatible = check_installation.check_python_version()
        return compatible, output.getvalue()

    def test_rejects_python_38(self):
        compatible, output = self.run_check(VersionInfo(3, 8, 18, "final", 0))

        self.assertFalse(compatible)
        self.assertIn("need 3.9+", output)

    def test_accepts_python_39(self):
        compatible, output = self.run_check(VersionInfo(3, 9, 6, "final", 0))

        self.assertTrue(compatible)
        self.assertIn("Python 3.9.6 is compatible", output)


if __name__ == "__main__":
    unittest.main()
