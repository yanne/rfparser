*** settings ***
Library  OperatingSystem
Library  Collections

* Variables *
${greeting}   Hello world!

*** test cases ***
Test 1
  [Tags]   absolutely-critical   mandatory
  Log  ${greeting}  DEBUG
Test 2
  ${files}=  List Directory  .
  Log  ${files}
  Log  WARNING
  ...  warn

Test 3  ${a dict}  Create Dictionary   foo  bar
  Log  ${a dict}
  My Uk


*** keywords ***
My UK   Log  Moi

