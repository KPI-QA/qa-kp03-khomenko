*** Settings ***
Documentation  CLI Functionality
Library  Process 
Library  String


*** Variables ***
${result}
${outputstr}
${rootident}    
*** Test Cases ***
Can tree filesystem
    ${rootident} =    Generate Random String    5     ${SPACE}
    ${result} =    Run Process    python    ${CURDIR}/cliclient.py    read    shell=yes
    Log  ${result.stderr}
    Log  ${result.stdout}
    Should Not Be Empty  ${result.stdout}
    Should Start With    ${result.stdout}    ${rootident}root>\n

Can create directory When Name Provided
    ${result} =    Run Process    python    ${CURDIR}/cliclient.py    create-dir    --name  testCreateDir    shell=yes
    Should Not Be Empty    ${result.stdout}
    Should Start With    ${result.stdout}    Directory is created!

Cannot create directory When Name Not Provided
    ${result} =    Run Process    python    ${CURDIR}/cliclient.py    create-dir    shell=yes
    Should Be Empty   ${result.stdout}
    Should Contain    ${result.stderr}    Error: Missing option '-n' / '--name'.


Can move directory 
    Run Process    python    ${CURDIR}/cliclient.py    create-dir    --name  testmove1    shell=yes
    Run Process    python    ${CURDIR}/cliclient.py    create-dir    --name  testmove2    shell=yes
    ${result} =    Run Process    python    ${CURDIR}/cliclient.py    move-dir    -f  testmove1    -t  testmove2    shell=yes
    Should Not Be Empty    ${result.stdout}
    Should Start With    ${result.stdout}    Directory moved successfully 


Can remove directory
    Run Process    python    ${CURDIR}/cliclient.py    create-dir    --name  testremove1    shell=yes
    ${result} =    Run Process    python    ${CURDIR}/cliclient.py    remove-dir    --name  testremove1    shell=yes
    Should Not Be Empty    ${result.stdout}
    Should Start With    ${result.stdout}    File removed successfully!


Can create log file
    ${result} =    Run Process    python    ${CURDIR}/cliclient.py    create-file    --name  createlog1    --type  logtextfile    --capacity  10    shell=yes
    Should Not Be Empty    ${result.stdout}
    Should Start With    ${result.stdout}    File of type (logtextfile) created successfully!


Can create buffer file
    ${result} =    Run Process    python    ${CURDIR}/cliclient.py    create-file    --name  createbuff1    --type  bufferfile    --capacity  10    shell=yes
    Should Not Be Empty    ${result.stdout}
    Should Start With    ${result.stdout}    File of type (bufferfile) created successfully!


Can create binary file 
    ${result} =    Run Process    python    ${CURDIR}/cliclient.py    create-file    --name  createbin1    --type  binaryfile    --capacity  10    shell=yes
    Should Not Be Empty    ${result.stdout}
    Should Start With    ${result.stdout}    File of type (binaryfile) created successfully!


Can write to file writeable
    Run Process    python    ${CURDIR}/cliclient.py    create-file    --name  writeable    --type  logtextfile    --capacity  10    shell=yes
    ${result} =    Run Process    python    ${CURDIR}/cliclient.py    writeto    --name  writeable    --newline  Hello Wrold!    shell=yes
    Should Not Be Empty    ${result.stdout}
    Should Start With    ${result.stdout}    Record has been written!
    
Cannot write to writeless
    Run Process    python    ${CURDIR}/cliclient.py    create-file    --name  writelessbin1    --type  binaryfile    --capacity  10    shell=yes
    ${result} =    Run Process    python    ${CURDIR}/cliclient.py    writeto    --name  writelessbin1    --newline  Hello Wrold!    shell=yes
    Should Start With    ${result.stdout}    Invalid action!

Can read file
    Run Process    python    ${CURDIR}/cliclient.py    create-file    --name  fileToRead    --type  binaryfile    --capacity  10    shell=yes
    ${result} =    Run Process    python    ${CURDIR}/cliclient.py    read    --name  fileToRead    shell=yes
    Should Not Be Empty    ${result.stdout}
    Should Contain    ${result.stdout}    but you can't touch
    
Can remove file 
    Run Process    python    ${CURDIR}/cliclient.py    create-file    --name  fileToRemove    --type  binaryfile    --capacity  10    shell=yes
    ${result} =    Run Process    python    ${CURDIR}/cliclient.py    remove-file    --name  fileToRemove    shell=yes
    Should Start With    ${result.stdout}    File removed successfully!

*** Keywords ***

