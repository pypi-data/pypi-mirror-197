# Panimalar

A package for students of Panimalar Engineering College

## Modules

## rollno

- isvalid(rollno) => boolean
- get_dept_code(rollno) => string
- get_dept(rollno) => string
- parse(rollno, required) => string (or) int
- get_year(rollno) => int

## cgpa

### Classes and Methods

- Subject
- Gpa(Subject)
- Cgpa(Gpa)

#### Subject 
This class stores the credit and grade point of a subject.
- credit
- grade point

#### Gpa

- addsubject(self, credit: int, grade_point: int)
- calc(self) -> float
- display(self) -> None
- added(self) -> None
- removesubject(self, index: int) -> None
  
#### Cpga
- calc(self)
- display(self) -> None
- added(self) -> None
- removesemester(self, index: int) -> None


## Details

- Validate Roll Number 

- Parse Details from Roll Number

Roll Number in Panimalar follows the system (YEAROFJOIN)YYYY-PEC-(DEPT)DD-(ROLLNO)XXXX

eg - 2021PECCB101

2021 - Year of Join
PEC - Panimalar Engineering College
CB - Department (Computer Science and Business Systems)
101 - Roll Number of Student


### Release Steps

- change version number in pyproject.toml (majorchanges.updates.bugfixes)
- add modules to pyproject.toml
- add dependencies if any
- add new functions in readme


