
1. Sample Code for Window Local Run

- save "runcmd.cmd" with below

========================================================================
@ECHO OFF
:: random value for temporary file name
set random_name=%RANDOM%
set rfilename=%random_name%.txt

:: Get Local IP
route print -4 | findstr /I /L 0.0.0.0 > %rfilename%
for /f "tokens=1,3" %%m in (%rfilename%) do (
  if %%m==0.0.0.0 (
     set MYIP=%%n
	 goto ipbreak
  )
)
:ipbreak
del %rfilename% 

:: GET Computer Name
for /f "skip=1 tokens=1" %%i in ('wmic computersystem get name') do (  
   set MYCSNAME=%%i
   goto csnamebreak 
)
:csnamebreak

:: Set file to write
set WF=window-%MYCSNAME%-%MYIP%.origin.txt

:: Run
echo ----- : result from script : ----- > %WF%
:: computersystem
echo computersystem info is getting...
echo ----- : begin computersystem : ----- >> %WF%
for /f "delims=" %%i in ('wmic computersystem') do (
   echo %%i >> %WF%
)
echo ----- : end computersystem : ----- >> %WF%
:: operatingsystem
echo operatingsystem info is getting...
echo ----- : begin operatingsystem : ----- >> %WF%
for /f "delims=" %%i in ('wmic os') do (
   echo %%i >> %WF%
)
echo ----- : end operatingsystem : ----- >> %WF%
:: product
echo product info is getting...
echo ----- : begin product : ----- >> %WF%
for /f "delims=" %%i in ('wmic product') do (
   echo %%i >> %WF%
)
echo ----- : end product : ----- >> %WF%
echo ----- : end of script : ----- >> %WF%
========================================================================

2. sample code for Linux

- save "run-linux.sh" with below

=======================================================================
#! /bin/bash

# Get Local IP address
DEFAULTIF=$(route | grep -i "default" | awk '{print $8}')
SEARCHEDIP=$(ip addr show $DEFAULTIF | grep -i 'inet ' | awk '{print $2}' | awk -F "[/]" '{print $1}')

# Get Host Name
SEARCHEDHOSTNAME=$(hostnamectl | grep -i "static hostname" | awk '{print $3}')

# File Path for Result
WF="linux-"$SEARCHEDHOSTNAME"-"$SEARCHEDIP".origin.txt"

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
=======================================================================
