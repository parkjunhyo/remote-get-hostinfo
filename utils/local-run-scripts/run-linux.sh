#! /bin/bash

# Get Local IP address
DEFAULTIF=$(route | grep -i "default" | awk '{print $8}')
SEARCHEDIP=$(ip addr show $DEFAULTIF | grep -i 'inet ' | awk '{print $2}' | awk -F "[/]" '{print $1}')

# Get Host Name
SEARCHEDHOSTNAME=$(hostnamectl | grep -i "static hostname" | awk '{print $3}')

# File Path for Result
WF="linux-localrun-"$SEARCHEDHOSTNAME"-"$SEARCHEDIP".origin.txt"

# Run Script
echo "----- : result from script : -----" > $WF
echo "hostnamectl info getting.."
echo "----- : begin hostnamectl : -----" >> $WF
hostnamectl >> $WF
echo "----- : end hostnamectl : -----" >> $WF

echo "/etc/os-release info getting.."
echo "----- : begin /etc/os-release : -----" >> $WF
cat /etc/os-release >> $WF
echo "----- : end /etc/os-release : -----" >> $WF


# GET Linux Distribution
ID_LIKE=$(cat /etc/os-release | grep -i id_like | awk -F"[=]" '{print $2}')

# Change all captial to lower case
LOWERCASE_IDLIKE=${ID_LIKE,,}

## Match Command and Run
echo "product info getting.."
echo "----- : begin product : -----" >> $WF
if [[ $ID_LIKE =~ .*"debian".* ]] || [[ $ID_LIKE =~ .*"ubuntu".* ]]
then
  dpkg -l | awk '{print $2"!!!!!"$3}' >> $WF
elif [[ $ID_LIKE =~ .*"rhel".* ]] || [[ $ID_LIKE =~ .*"fedora".* ]] || [[ $ID_LIKE =~ .*"centos".* ]]
then
  rpm -qa >> $WF
fi
echo "----- : end product : -----" >> $WF

# END
echo "----- : end of script : -----" >> $WF
