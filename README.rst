spithon
=======

A command-line tool for SPI and GPIO access on the Raspberry Pi.

GETTING STARTED
---------------

It is recommended to create a python virtual environment and activate it
before installing this library:

.. code:: bash

   $ python -m venv ~/venv/spithon
   $ source ~/venv/spithon/bin/activate

Install:

.. code:: bash

   $ pip install spithon

Post-install
~~~~~~~~~~~~

Once the library is installed, it can then be used as follows:

.. code:: bash

   $ spithon <command> [options]

Using the ``--help`` command will list all available commands
implemented by the tool. Each command can also be called with ``--help``
to see usage.

CONFIGURATION
-------------

The SPI interface and GPIO pins can be configured via the
``~/.spithon/config.ini`` configuration file. An example file for the
SPI configuration is shown below:

.. code:: ini

   [RPi.SPI]
   bus = 0
   device = 1
   mode = 0b00
   rate = 4000000
   bits_per_word = 8
   word_length = 32

   [RPi.CRC]
   width = 8
   polynomial = 0x10
   initial_value = 0

**SPI**

-  ``bus``: Defines the SPI bus to use (generally this can be kept at 0)
-  ``device``: Selects whether to use CE0 or CE1 of the Raspberry Pi
-  ``mode``: Changes the SPI mode
-  ``rate``: Changes the SCLK frequency in Hz. Raspberry Pi 3A+ limited
   to ~8MHz SCLK
-  ``bits_per_word``: Changes number of bits per word to transfer. Max
   of 8bits (one byte).
-  ``word_length``: How many bits per word (for example, 16b address
   with 16b data would be a 32 bit word

**CRC**

-  ``width``: CRC width. Generally 8, 16, or 32
-  ``polynomial``: Polynomial to use for CRC seeding
-  ``initial_value``: Initial value for CRC calculation

TYPICAL USAGE
-------------

The following highlight typical usage scenarios to get started. All
commands can be performed directly in the terminal. If you installed
with the instructions above (ie. using a python venv) make sure your
venv is activated before attempting any commands.

NOTE: Not all avaialbe commands are shown below, only the ones most
likely to be used frequently.

Getting Help
~~~~~~~~~~~~

At any time, the ``--help`` flag will show basic command usage.

.. code:: bash

   $ spithon --help

or

.. code:: bash

   $ spithon <command> --help

Write/Read
~~~~~~~~~~

A device can be written to/read from via SPI with the following
commands:

.. code:: bash

   $ spithon write <word> [--crc] [--verbose]
   $ spithon read <word> [--crc] [--verbose]

Functionally, a ``read`` transaction is identical to a ``write`` but for
CRC purposes it is assumed the destination device is returning a CRC
word rather than it being supplied by the host. In addition, a ``read``
transaction will print the return value to the ``write`` command ignores
the contents of the ``MISO`` pin altogehter.

GPIO Control
~~~~~~~~~~~~

There are multiple options for GPIO commands, but the most handy are to
set a GPIO state or read a state.

.. code:: bash

   $ spithon read <gpio channel>
   $ spithon drive_lo <gpio channel>
   $ spithon drive_hi <gpio channel>

Contributing
------------

**1. Clone the repository and cd into directory**

.. code:: bash

   git clone git@github.com:fronzbot/spithon.git
   cd spithon
   git remote add upstream https://github.com/fronzbot/spithon.git

**2. Create a virtual environment**

.. code:: bash

   python -m venv ~/venv/spithon-dev
   source ~/venv/spithon-dev/bin/activate

**3. Install test requirements**

.. code:: bash

   pip install -r requirements_test.txt

**4. Install development version of the script**

.. code:: bash

   cd 
   pip install -e .

**5. Create a local branch for development**

.. code:: bash

   git checkout -b <your-branch-name>

**6. Make changes**

Now you can make changes to the code, test, etc. See the Testing section
below for details on how to test your code before committing.

**7. Catching up to main branch**

If your features have fallen behind the main branch, you can run the
following commands to rebase. Sometimes this will require manually
editing files to resolve conflicts, but just follow the prompts and git
should guide you through it.

.. code:: bash

   git checkout <your-branch>
   git fetch upstream dev
   git rebase upstream/dev

If rebase detects conflicts, repeat the following process until all
changes have been resolved:

``git status`` shows you the file with a conflict. You will need to edit
that file and resolve the lines between ``<<<< | >>>>``.

Add the modified file: ``git add <file>`` or ``git add .``.

Continue rebase: ``git rebase --continue``.

Repeat until all conflicts resolved.

**8. Commit your changes**

To commit changes to your branch, just add the files and the push to
your branch:

.. code:: bash

   git add .
   git commit -m "Commit message."
   git push origin <your-branch-name>

**9. Open a Pull Request**

Navigate to the `github repo
page <https://github.com/fronzbot/spithon>`__ and open a new pull
request with your changes.

Testing
-------

Some basic testing capability is included. Right now it’s just linting
to make sure the codebase is clean for multiple people to develop with.

The full test suite can be run with the following:

.. code:: bash

   tox

If the output of ``black`` says it would reformat a file, you can do so
automatically via:

.. code:: bash

   black <file_name>

**Tests must pass before PR’s can be merged!**
