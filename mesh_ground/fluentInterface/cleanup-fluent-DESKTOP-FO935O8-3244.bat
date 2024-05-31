echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\v222\fluent/ntbin/win64/winkill.exe"

"C:\PROGRA~1\ANSYSI~1\v222\fluent\ntbin\win64\tell.exe" DESKTOP-FO935O8 58893 CLEANUP_EXITING
if /i "%LOCALHOST%"=="DESKTOP-FO935O8" (%KILL_CMD% 13204) 
if /i "%LOCALHOST%"=="DESKTOP-FO935O8" (%KILL_CMD% 3244) 
if /i "%LOCALHOST%"=="DESKTOP-FO935O8" (%KILL_CMD% 10232)
del "\\tsclient\_media_thedal_Vault\python\foam_to_fluent2D\mesh_ground\fluentInterface\cleanup-fluent-DESKTOP-FO935O8-3244.bat"
