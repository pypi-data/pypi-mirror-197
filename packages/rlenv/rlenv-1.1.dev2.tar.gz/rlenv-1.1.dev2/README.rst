=======================
Accenta Gym Environment
=======================

Copyright (c) 2019-2022 Accenta (www.accenta.ai)

* Web site: https://gitlab.com/ens-data-challenge/accenta-gym-environment
* Online documentation: https://ens-data-challenge.gitlab.io/accenta-gym-environment
* Examples: https://ens-data-challenge.gitlab.io/accenta-gym-environment/gallery/

* Source code: https://gitlab.com/ens-data-challenge/accenta-gym-environment
* Issue tracker: https://gitlab.com/ens-data-challenge/accenta-gym-environment/issues


Description
===========

Accenta Gym Environment

Note:

    This project is still in beta stage, so the API is not finalized yet.


Dependencies
============

C.f. requirements.txt

.. _install:

Installation
============

Posix (Linux, MacOSX, WSL, ...)
-------------------------------

From the EnergyPlus Python source code::

    conda deactivate         # Only if you use Anaconda...
    python3 -m venv env
    source env/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    python3 setup.py develop


Windows
-------

From the EnergyPlus Python source code::

    conda deactivate         # Only if you use Anaconda...
    python3 -m venv env
    env\Scripts\activate.bat
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    python3 setup.py develop


Build and run the Accenta Gym Environment Docker image
======================================================

Build the docker image
----------------------

From the EnergyPlus Python source code::

    docker build -t registry.gitlab.com/ens-data-challenge/accenta-gym-environment .

Run unit tests from the docker container
----------------------------------------

From the EnergyPlus Python source code::

    docker run registry.gitlab.com/ens-data-challenge/accenta-gym-environment pytest

Run an example from the docker container
----------------------------------------

From the EnergyPlus Python source code::

    docker run registry.gitlab.com/ens-data-challenge/accenta-gym-environment python3 /rlenv/examples/plot_wall_env.py

Push the docker image on the container registry
-----------------------------------------------

From the EnergyPlus Python source code::

    docker push registry.gitlab.com/ens-data-challenge/accenta-gym-environment


Documentation
=============

* Online documentation: https://ens-data-challenge.gitlab.io/accenta-gym-environment
* API documentation: https://ens-data-challenge.gitlab.io/accenta-gym-environment/api.html


Example usage
=============

C.f. https://ens-data-challenge.gitlab.io/accenta-gym-environment/gallery/


Bug reports
===========

To search for bugs or report them, please use the Accenta's Gym Environments Bug Tracker at:

    https://gitlab.com/accenta_group/ai-gym/issues
