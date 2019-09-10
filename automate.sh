#!/usr/bin/env bash

echo "Started running Boto script"
python boto/initialise.py

echo "Create archive of the project to send it to the server"
(cd ~/Documents/;
tar -czvf nectar.tar.gz nectar-twitter-analytics/ > /dev/null)

cd ~/Documents/nectar-twitter-analytics/ansible/
echo "Started running Ansible playbook"
ansible-playbook playbook.yml -v