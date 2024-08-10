Usage
=====

TMNT consists of a few different parts. Most of this documentation is dedicated to setting up the app part of TMNT (the UI and Controller Microservice).

Installation of ``tmnpy``
-------------------------

To use ``tmnpy``, our python package for threat modeling, you'll need to install it using pip:

.. code-block:: console

   $ git clone git@github.com:tufts-tsp/tmnpy.git
   $ pip install ./tmnpy

Note: We are working to make this available on `pypi <https://pypi.org/>` in the coming weeks.

Running the TMNT App
--------------------

You can run the UI and Controller either independently or together. Please refer to the instructions for the modules you want to use below.

NOTE: If you are running this locally, we highly recommend using `venv <https://docs.python.org/3/library/venv.html>`_ to ensure you are using the correct packages and their versions. You can install these with the ``requirements.txt`` files in ``app`` and ``controller``.

UI
^^

Right now, the UI is the part of the tool that has the most functionality and is freestanding. You can run it either by cloning this repository and running the UI or you can use our Docker image (see :ref:`docker-setup`).

If you clone the repo, you can run the app with the following::

    cd app
    python manage.py migrate
    python manage.py runserver

Once the app is running, you should be able to navigate to ``http://localhost:8000/tmnt/`` to use the app.

Controller
^^^^^^^^^^

To run the the controller, you either can use our Docker image (see :ref:`docker-setup`) or you can clone this repo and manually run it. If you clone the repo, you will need to install `tmnpy <https://github.com/tufts-tsp/tmnpy>`_. We provide a wheel of the package in this repo, and it will be available on pypi by the end of August. In addition to ``tmnpy``, there are a set of requirements in ``controller/requirements.txt``. Once you have the requirements installed, you simply need to run ``controller.py``.

.. _docker-setup:
Docker Setup
------------

If you want you can also build your own Docker images using the Dockerfiles in ``app`` and ``controller``. You can run either on their own or together. If you run them together, we recommend building/running the controller first. You'll want to install `Docker Desktop <https://docs.docker.com/desktop/>`_.

To setup ``controller`` you simply run::

    docker build . -f controller/Dockerfile -t controller
    docker run -p 127.0.0.1:50051:50051/tcp controller

The ``app`` uses very similar commands::

    docker build . -f app/Dockerfile -t tmnt-ui
    docker run -p 127.0.0.1:8000:8000/tcp tmnt-ui

You can change the ports for either part. If you change the port for the ``controller`` you should set it with an environmental variable ``CONTROLLER_PORT`` in both Dockerfiles. Additionally, if you are running the controller on a different IP from the ``app``, you should set ``CONTROLLER_HOST`` in ``app/Dockerfile``.
