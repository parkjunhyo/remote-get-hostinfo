#! /bin/bash

############ Command Validation-Checking ##################
echo "Command Validation-Checking  .........."
if [[ $(which hostnamectl) ]]
then
   HOSTCTLCMDSTATUS=1
else
   HOSTCTLCMDSTATUS=0
fi
echo ""
########## GET LOCAL IP ADDRESS ########
echo ""
DEFAULTIF=$(ip route | grep -i default | awk '{print $5}')
SEARCHEDIP=$(ip addr show $DEFAULTIF | grep -i 'inet ' | awk '{print $2}' | awk -F "[/]" '{print $1}')

############### GET HOST NAME ##########
if [[ $HOSTCTLCMDSTATUS == 1 ]]
then
   if [[ $(hostnamectl) ]]
   then
      SEARCHEDHOSTNAME=$(hostnamectl | grep -i "static hostname" | awk '{print $3}')
   else
      SEARCHEDHOSTNAME=$(hostname)
   fi
else
   SEARCHEDHOSTNAME=$(hostname)
fi

######### CREATE FILE PATH TO WRITE THE RESULT ###############
WF="linux-localrun-"$SEARCHEDHOSTNAME"-"$SEARCHEDIP".origin.txt"

######## RUN SCRIPT ########################
echo "----- : begin result from script : -----" > $WF

echo "hostnamectl (hostname) info getting.."
echo "----- : begin hostnamectl : -----" >> $WF
if [[ $HOSTCTLCMDSTATUS == 1 ]]
then
   if [[ $(hostnamectl) ]]
   then
      hostnamectl >> $WF
   else
      echo Static hostname: $(hostname) >> $WF
      ARCHSTR=$(uname -i)
      LOWER_ARCHSTR=${ARCHSTR,,}
      if [[ $LOWER_ARCHSTR =~ .*"unknown".* ]]
      then
         ARCHSTR=$(uname -m)
      fi
      echo Architecture: $ARCHSTR >> $WF
   fi
else
   echo Static hostname: $(hostname) >> $WF
   ARCHSTR=$(uname -i)
   LOWER_ARCHSTR=${ARCHSTR,,}
   if [[ $LOWER_ARCHSTR =~ .*"unknown".* ]]
   then
      ARCHSTR=$(uname -m)
   fi
   echo Architecture: $ARCHSTR >> $WF
fi
echo "----- : end hostnamectl : -----" >> $WF


echo "/etc/os-release info getting.."
echo "----- : begin /etc/os-release : -----" >> $WF
if [[ -f /etc/os-release ]]
then
   cat /etc/os-release >> $WF
   #
   TEMPSTATUS=$(cat /etc/os-release | grep -i id_like)
   if [[ $TEMPSTATUS ]]
   then
      IDLIKE_TEMP=$(cat /etc/os-release | grep -i '^id_like=' | awk -F"[=]" '{print $2}')
   else
      IDLIKE_TEMP=$(cat /etc/os-release | grep -i '^id=' | awk -F"[=]" '{print $2}')
   fi
   IDLIKE_TEMP_LOWER=${IDLIKE_TEMP,,}
else
   if [[ -f /etc/system-release ]]
   then
      ONAME=$(cat /etc/system-release | awk '{if(NR==1) print $0}')
      echo NAME=\"$ONAME\" >> $WF
   elif [[ -f /etc/redhat-release ]]
   then
      ONAME=$(cat /etc/redhat-release | awk '{if(NR==1) print $0}')
      echo NAME=\"$ONAME\" >> $WF
   elif [[ -f /etc/centos-release ]]
   then
      ONAME=$(cat /etc/centos-release | awk '{if(NR==1) print $0}')
      echo NAME=\"$ONAME\" >> $WF
   elif [[ -f /etc/lsb-release ]]
   then
      ONAME=$(cat /etc/lsb-release | grep -i DISTRIB_DESCRIPTION | awk -F"[=]" '{if(NR==1) print $2}')
      echo NAME=$ONAME >> $WF
   else
      ONAME=$(cat /etc/issue | awk '{if(NR==1) print $0}')
      echo NAME=\"$ONAME\" >> $WF
   fi
   #
   IDLIKE_TEMP=$(sudo find /etc/ -iname "*-release" | awk -F "[/]" '{if(NF==3) print $NF;}' | awk -F "[-]" '{printf $1" "}')
   IDLIKE_TEMP_LOWER=${IDLIKE_TEMP,,}
   echo ID_LIKE=$IDLIKE_TEMP_LOWER >> $WF
   #
   ID_TEMP=$(echo $ONAME | awk '{print $1$2}')
   ID_TEMP_LOWER=${ID_TEMP,,}
   echo ID=$ID_TEMP_LOWER >> $WF
   #
   VERSION_TEMP=$(echo $ONAME | awk -F"release" '{print $NF}')
   echo VERSION=\"$VERSION_TEMP\" >> $WF
   echo VERSION_ID=\"$VERSION_TEMP\" >> $WF
fi
echo "----- : end /etc/os-release : -----" >> $WF

echo "kernal info getting.."
echo "----- : begin kernal : -----" >> $WF
KERNAL_TEMP=$(cat /proc/version | awk -F"[(]" '{print $1}')
echo oskernal=$KERNAL_TEMP >> $WF
echo "----- : end kernal : -----" >> $WF


echo "product info getting.."
echo "----- : begin product : -----" >> $WF
LOWERCASE_IDLIKE=${IDLIKE_TEMP_LOWER,,}
IFS=' '
read -ra VAL <<< $LOWERCASE_IDLIKE
for i in "${VAL[@]}"; do
    if [[ $i =~ .*"debian".* ]] || [[ $i =~ .*"ubuntu".* ]]
    then
       dpkg -l | awk '{print $2"!!!!!"$3}' >> $WF
       break;
    elif [[ $i =~ .*"rhel".* ]] || [[ $i =~ .*"redhat".* ]] || [[ $i =~ .*"fedora".* ]] || [[ $i =~ .*"centos".* ]] || [[ $i =~ .*"suse".* ]] || [[ $i =~ .*"sles".* ]]
    then
       rpm -qa >> $WF
       break;
    else
       continue;
    fi
done
echo "----- : end product : -----" >> $WF

echo "----- : end result from script : -----" >> $WF

