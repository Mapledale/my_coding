Windows:
Install Python 2.7
make sure python is recognized as a command in cmd
    to test it enter "python" in the cmd
    if it doesnt work add the "C:\Python27" directory to the system variable Path
make sure pip is recognized as a command in cmd
    to test it enter "pip -V" in the cmd
    if it doesnt work add the "C:\Python27\Scripts" directory to the system variable Path

make sure putty and pscp are recognized as commands in cmd
    if it doesnt work add the "C:\Program Files\PuTTY" directory to the system variable Path


launch Genie by executing genie.py
The first launch might take a while as it auto installs the necessary packages



CentOs:
Install Python 2.7 and pip if not already installed:
    sudo yum -y install python
    sudo yum -y install python-pip

launch Genie by executing genielinux.sh

The first launch might take a while as it auto installs the necessary packages



Using Genie:
    First a connection needs to be added to the list. this can be done by adding an ip adress in the ip adress field and hittihg the add button.
    The username, password and port are assumed to be admin, CHGME.1a and 22 if not specified.
    The added connections will be stored persistently and can be edited in the userdata.yaml file.

    The next step is to select one connection and click connect GUI.
    After that the SSH, DTE and Telnet buttons can be used to open terminal sessions to the ECM.
    The buttons below perform the action on all selected modules.

    The copying section uses the selected source from the dropdown and the checked modules from above as the destination.
    The full paths to the files need to be specified.