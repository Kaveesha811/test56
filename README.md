# Student Result Management System

A simple Python GUI application for managing student records, calculating grades, and saving/loading data.

## Features

- **Add Students**: Input student ID, name, and marks for 5 subjects
- **Calculate Grades**: Automatic grade calculation based on average marks
  - A: 90-100%
  - B: 80-89%
  - C: 70-79%
  - D: 60-69%
  - F: Below 60%
- **View Records**: Display all students in a table
- **Search**: Find and display individual student details
- **Update**: Modify existing student information
- **Delete**: Remove student records
- **Save/Load**: Persist data to JSON file

## How to Run

```bash
python student_system.py
```

## Project Structure

### Student Class
```python
Student(student_id, name, marks)
```
- `student_id`: Unique integer ID
- `name`: Student's full name
- `marks`: Dictionary of 5 subjects and their marks
- Methods:
  - `calculate_total()`: Sum of all marks
  - `calculate_grade()`: Grade based on average percentage
  - `to_dict()`: Convert to dictionary for JSON storage

### StudentApp Class
- Manages GUI using Tkinter
- Handles all operations (add, update, delete, search)
- Manages data loading/saving to JSON

## Data Format

Students are saved in `students.json` as:
```json
[
  {
    "id": 1,
    "name": "John Smith",
    "marks": {
      "Math": 85,
      "Science": 90,
      "English": 78,
      "ICT": 92,
      "History": 88
    },
    "total": 433,
    "grade": "B"
  }
]
```

## GUI Tabs

### Tab 1: Add/Update Student
- Enter Student ID and name
- Input marks for all 5 subjects (0-100)
- Add new or update existing students
- Save/Load records

### Tab 2: View Records
- Search students by ID
- View all students
- Delete students
- Click table rows to populate edit form

## Key Learning Points

1. **Object-Oriented Programming**: Student and StudentApp classes
2. **Python Data Types**: Dictionaries, lists, strings
3. **Functions**: Modular functions for each operation
4. **File I/O**: JSON file handling
5. **GUI Development**: Tkinter with tabs and tables
6. **Data Validation**: Input validation for marks (0-100)

## Usage Example

1. Click on "Add/Update Student" tab
2. Enter Student ID (e.g., 101)
3. Enter Name (e.g., "Alice")
4. Enter marks for each subject
5. Click "Add Student"
6. Click "Save Records" to save to file
7. Switch to "View Records" tab to see students in table

## Technical Details

- **Language**: Python 3.x
- **GUI Framework**: Tkinter
- **Data Storage**: JSON
- **File**: students.json

## Grade Calculation Algorithm

```
Average = (Math + Science + English + ICT + History) / 5
If Average >= 90: Grade = A
If Average >= 80: Grade = B
If Average >= 70: Grade = C
If Average >= 60: Grade = D
Else: Grade = F
```

## Notes

- Student IDs must be unique
- Marks must be between 0 and 100
- All subjects are required
- Data persists in students.json file
