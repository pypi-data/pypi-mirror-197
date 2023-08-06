# SPDX-FileCopyrightText: 2022 The Ikarus Developers mueller@ibb.uni-stuttgart.de
# SPDX-License-Identifier: LGPL-3.0-or-later
# this file is modified from dumux https://git.iws.uni-stuttgart.de/dumux-repositories/dumux/-/blob/master/setup.py

try:
    from dune.packagemetadata import metaData
except ImportError:
    from packagemetadata import metaData
from skbuild import setup

# When building a new package, update the version numbers below and run:
#
# cd
#  /dune/dune-common/build-cmake/run-in-dune-env pip install twine scikit-build
# git config --global --add safe.directory /tmp/Ikarus
# /dune/dune-common/build-cmake/run-in-dune-env python setup.py sdist
# > /dune/dune-common/build-cmake/run-in-dune-env python -m twine upload dist/* --verbose
# install locally:  pip install -v --pre --log logfile --find-links file://$PWD/dist ikarus==version
# apt update
# apt install nano
# cat << EOF > ~/.pypirc
# The current working directory is: $PWD
# You are logged in as $(whoami)
# EOF
# nano ~/.pypirc
# python -m venv /dune/dune-common/build-cmake/dune-env/
# source /dune/dune-common/build-cmake/dune-env/bin/activate
# pip install pyikarus  --no-build-isolation

pyikarusVersion = "0.3.0.dev202310000048" #+ datetime.today().time().strftime("%H%M%S")
duneVersion = "2.9.0"

metadata = metaData(duneVersion)[1]
metadata["version"] = pyikarusVersion

setup(**metadata)
