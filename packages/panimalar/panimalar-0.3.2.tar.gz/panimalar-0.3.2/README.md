# Panimalar

A package for students of Panimalar Engineering College

## Modules

### rollno

- isvalid(rollno)
- get_dept_code(rollno)
- get_dept(rollno)
- parse(rollno, required)


## Details

- Validate Roll Number 

- Parse Details from Roll Number

Roll Number in Panimalar follows the system (YEAROFJOIN)YYYY-PEC-(DEPT)DD-(ROLLNO)XXXX

eg) 2021PECCB101

2021 - Year of Join
PEC - Panimalar Engineering College
CB - Department (Computer Science and Business Systems)
101 - Roll Number of Student


### Release Steps

- change version number in pyproject.toml (majorchanges.updates.bugfixes)
- add modules to pyproject.toml
- add dependencies if any
- add new functions in readme


