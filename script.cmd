@echo off
set port=10000
set chord_version=3
start cmd /c "python chord_v%chord_version%.py %port%"
set loopcount=1
:loop
set /a node_port = port + loopcount
if %loopcount%==32 goto exitloop
start cmd /c "python chord_v%chord_version%.py %node_port% 127.0.0.1 10000"
timeout 1
set /a loopcount=loopcount+1
goto loop
:exitloop
