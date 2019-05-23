if [ ! -d "venv/" ]; then
  mkdir venv/;
  sudo pip install virtualenv;
  virtualenv venv/;
  sudo yum -y install sshpass;
fi
source venv/bin/activate;
python genie.py;

