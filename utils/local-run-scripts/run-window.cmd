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