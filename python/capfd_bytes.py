import os
import tempfile

import pytest


@pytest.fixture
def ctx():
    with tempfile.TemporaryFile() as tmp_o, tempfile.TemporaryFile() as tmp_e:
        stdout, stderr = 1, 2
        stdout_duped, stderr_duped = os.dup(stdout), os.dup(stderr)
        tmp_o_fd, tmp_e_fd = tmp_o.fileno(), tmp_e.fileno()

        class CapFdBytes(object):
            stopped = False

            def readouterr_bytes(self):
                def _getvalue(s):
                    s.seek(0)
                    ret = s.read()
                    s.seek(0)
                    s.truncate()
                    return ret

                return _getvalue(tmp_o), _getvalue(tmp_e)

        os.dup2(tmp_o_fd, stdout), os.dup2(tmp_e_fd, stderr)

        yield CapFdBytes()

        os.dup2(stdout_duped, stdout), os.dup2(stderr_duped, stderr)
        os.close(stdout_duped), os.close(stderr_duped)
