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
set MYIP=%MYIP: =%
set MYCSNAME=%MYCSNAME: =%
set WF=window-localrun-%MYCSNAME%-%MYIP%.origin.txt
echo ----- : begin result from script : ----- > %WF%

:: computersystem
echo computersystem info is getting...
echo ----- : begin computersystem : ----- >> %WF%
echo Name=%MYCSNAME% >> %WF%
for /f "skip=1 delims=" %%i in ('wmic computersystem get workgroup') do (
   set GETWORKGROUP=%%i
   goto workgroupbreak
)
:workgroupbreak
echo Workgroup=%GETWORKGROUP% >> %WF%
for /f "skip=1 delims=" %%i in ('wmic computersystem get domain') do (
   set GETDOMAIN=%%i
   goto domnamebreak
)
:domnamebreak
echo Domain=%GETDOMAIN% >> %WF%
echo ----- : end computersystem : ----- >> %WF%

:: operatingsystem
echo operatingsystem info is getting...
echo ----- : begin operatingsystem : ----- >> %WF%
for /f "skip=1 delims=" %%i in ('wmic os get caption') do (
   set GETCAPTION=%%i
   goto captionbreak
)
:captionbreak
echo Caption=%GETCAPTION% >> %WF%
for /f "skip=1 delims=" %%i in ('wmic os get osarchitecture') do (
   set GETOSARCHITECTURE=%%i
   goto archbreak
)
:archbreak
echo OSArchitecture=%GETOSARCHITECTURE% >> %WF%
for /f "skip=1 delims=" %%i in ('wmic os get version') do (
   set GETVERSION=%%i
   goto versionbreak
)
:versionbreak
echo version=%GETVERSION% >> %WF%
echo ----- : end operatingsystem : ----- >> %WF%


:: product
echo product info is getting...
echo ----- : begin product : ----- >> %WF%
@echo > %rfilename%
for /f "usebackq delims=" %%i in (`wmic product get caption^,version^/format:list`) do (
   @echo %%i >> %rfilename%
)
::   if you suffer from C runtime error due to findstr.exe, remove findstr,
for /f "delims=" %%i in (%rfilename%) do (
::   echo.%%i | findstr /v "^ECHO" >> %WF%
   echo %%i >> %WF%
)
del %rfilename%
echo ----- : end product : ----- >> %WF%
echo ----- : end result from script : ----- >> %WF%
