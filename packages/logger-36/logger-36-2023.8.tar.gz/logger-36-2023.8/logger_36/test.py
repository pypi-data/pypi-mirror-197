# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2023)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from pathlib import Path as path_t
from tempfile import TemporaryDirectory
from io import StringIO as fake_file_t
from logger_36 import (
    LOGGER,
    AddFileHandler,
    MaximumMemoryUsage,
    SetShowMemoryUsage,
    SaveLOGasHTML,
)


with TemporaryDirectory() as tmp_folder:
    tmp_folder = path_t(tmp_folder)
    tmp_file = tmp_folder / "log.txt"

    AddFileHandler(tmp_file)
    SetShowMemoryUsage(True)

    for level in ("debug", "info", "warning", "error", "critical"):
        LogMessage = getattr(LOGGER, level)
        LogMessage(f"{level.capitalize()} message")
        LogMessage(f"Multi-line\n{level.capitalize()}\nmessage")

    LOGGER.info("V" + 30 * "e" + "ry l" + 30 * "o" + "ng line")
    LOGGER.info("V" + 30 * "e" + "ry l" + 30 * "o" + "ng line...\n...with a newline")

    usage, unit = MaximumMemoryUsage(decimals=1)
    LOGGER.info(f"Max. memory usage: {usage}{unit}")

    content = open(tmp_file, "r").read()
    print(f"\n{content}")

fake_file = fake_file_t()
SaveLOGasHTML(fake_file)
print(fake_file.getvalue())
