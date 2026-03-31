import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class Student:
    """Stores student information"""
    def __init__(self, student_id, name, marks):
        self.student_id = student_id
        self.name = name
        self.marks = marks
        
    def get_total(self):
        return sum(self.marks.values())
    
    def get_grade(self):
        avg = self.get_total() / len(self.marks)
        if avg >= 90:
            return "A"
        elif avg >= 80:
            return "B"
        elif avg >= 70:
            return "C"
        elif avg >= 60:
            return "D"
        else:
            return "F"
    
    def to_dict(self):
        return {
            "id": self.student_id,
            "name": self.name,
            "marks": self.marks,
            "total": self.get_total(),
            "grade": self.get_grade()
        }


# Main Application
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Student System")
        self.root.geometry("700x500")
        
        self.students = []
        self.load_data()
        
        # Create UI
        self.create_ui()
    
    def create_ui(self):
        # Input Section
        frame = ttk.Frame(self.root, padding="10")
        frame.pack()
        
        ttk.Label(frame, text="Student ID:").grid(row=0, column=0)
        self.id_entry = ttk.Entry(frame)
        self.id_entry.grid(row=0, column=1)
        
        ttk.Label(frame, text="Name:").grid(row=1, column=0)
        self.name_entry = ttk.Entry(frame)
        self.name_entry.grid(row=1, column=1)
        
        # Marks Section
        ttk.Label(frame, text="Marks (0-100):").grid(row=2, column=0, columnspan=2, pady=10)
        
        self.mark_fields = {}
        subjects = ["Math", "Science", "English", "ICT", "History"]
        for i, subject in enumerate(subjects):
            ttk.Label(frame, text=subject + ":").grid(row=3+i, column=0)
            entry = ttk.Entry(frame, width=10)
            entry.grid(row=3+i, column=1)
            self.mark_fields[subject] = entry
        
        # Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Add", command=self.add_student).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="View All", command=self.view_all).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_student).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Save", command=self.save_data).pack(side="left", padx=5)
        
        # Table
        columns = ("ID", "Name", "Total", "Grade")
        self.table = ttk.Treeview(self.root, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=80)
        
        self.table.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.refresh_table()
    
    def add_student(self):
        try:
            sid = int(self.id_entry.get())
            name = self.name_entry.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Enter name")
                return
            
            # Check if ID exists
            if any(s.student_id == sid for s in self.students):
                messagebox.showerror("Error", "ID already exists")
                return
            
            # Get marks
            marks = {}
            for subject, field in self.mark_fields.items():
                try:
                    mark = float(field.get())
                    if mark < 0 or mark > 100:
                        raise ValueError
                    marks[subject] = mark
                except ValueError:
                    messagebox.showerror("Error", f"Invalid mark for {subject}")
                    return
            
            # Create student
            student = Student(sid, name, marks)
            self.students.append(student)
            self.refresh_table()
            self.clear_fields()
            messagebox.showinfo("Success", f"Student added!\nGrade: {student.get_grade()}")
        
        except ValueError:
            messagebox.showerror("Error", "Invalid ID")
    
    def view_all(self):
        if not self.students:
            messagebox.showinfo("Info", "No students")
            return
        
        text = "All Students:\n\n"
        for s in self.students:
            text += f"ID: {s.student_id} | {s.name} | Total: {s.get_total()}/500 | Grade: {s.get_grade()}\n"
        
        messagebox.showinfo("Students", text)
    
    def delete_student(self):
        try:
            sid = int(self.id_entry.get())
            for i, s in enumerate(self.students):
                if s.student_id == sid:
                    self.students.pop(i)
                    self.refresh_table()
                    self.clear_fields()
                    messagebox.showinfo("Success", "Student deleted")
                    return
            messagebox.showerror("Error", "Student not found")
        except ValueError:
            messagebox.showerror("Error", "Invalid ID")
    
    def refresh_table(self):
        # Clear table
        for item in self.table.get_children():
            self.table.delete(item)
        
        # Add rows
        for s in self.students:
            self.table.insert("", "end", values=(s.student_id, s.name, 
                                                f"{s.get_total()}/500", s.get_grade()))
    
    def clear_fields(self):
        self.id_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        for field in self.mark_fields.values():
            field.delete(0, "end")
    
    def save_data(self):
        try:
            data = [s.to_dict() for s in self.students]
            with open("students.json", "w") as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Success", "Data saved!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def load_data(self):
        if not os.path.exists("students.json"):
            return
        
        try:
            with open("students.json", "r") as f:
                data = json.load(f)
            
            for record in data:
                student = Student(record["id"], record["name"], record["marks"])
                self.students.append(student)
        except:
            pass


# Run
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()


    """Class representing a student with marks and grade calculation."""
    
    SUBJECTS = ["Math", "Science", "English", "ICT", "History"]
    GRADE_THRESHOLDS = {
        'A': 90,
        'B': 80,
        'C': 70,
        'D': 60,
        'F': 0
    }
    
    def __init__(self, student_id: int, name: str, marks: Dict[str, float]):
        """
        Initialize a student.
        
        Args:
            student_id: Unique student identifier
            name: Student's full name
            marks: Dictionary of marks for each subject
        """
        self.student_id = student_id
        self.name = name
        self.marks = marks
        self.total_marks = self.calculate_total()
        self.percentage = self.calculate_percentage()
        self.grade = self.calculate_grade()
    
    def calculate_total(self) -> float:
        """Calculate total marks from all subjects."""
        return sum(self.marks.values())
    
    def calculate_percentage(self) -> float:
        """Calculate percentage scored."""
        if len(self.marks) == 0:
            return 0
        return (self.total_marks / (len(self.marks) * 100)) * 100
    
    def calculate_grade(self) -> str:
        """
        Calculate grade based on percentage.
        A: 90-100%, B: 80-89%, C: 70-79%, D: 60-69%, F: Below 60%
        """
        for grade, threshold in self.GRADE_THRESHOLDS.items():
            if self.percentage >= threshold:
                return grade
        return 'F'
    
    def to_dict(self) -> Dict:
        """Convert student data to dictionary for JSON storage."""
        return {
            "id": self.student_id,
            "name": self.name,
            "marks": self.marks,
            "total": self.total_marks,
            "percentage": round(self.percentage, 2),
            "grade": self.grade
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Student':
        """Create Student object from dictionary."""
        student = Student(data["id"], data["name"], data["marks"])
        return student


# ============== STUDENT MANAGEMENT SYSTEM ==============
class StudentManagementSystem:
    """Main system for managing students and their results."""
    
    def __init__(self):
        """Initialize the student management system."""
        self.students: List[Student] = []
        self.file_name = "students.json"
        self.load_data()
    
    def add_student(self, student_id: int, name: str, marks: Dict[str, float]) -> bool:
        """
        Add a new student to the system.
        
        Args:
            student_id: Unique student ID
            name: Student name
            marks: Dictionary of marks
            
        Returns:
            True if successful, False otherwise
        """
        # Check if student ID already exists
        if self.get_student(student_id):
            return False
        
        student = Student(student_id, name, marks)
        self.students.append(student)
        return True
    
    def get_student(self, student_id: int) -> Optional[Student]:
        """Get student by ID."""
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None
    
    def get_all_students(self) -> List[Student]:
        """Get all students."""
        return sorted(self.students, key=lambda s: s.student_id)
    
    def delete_student(self, student_id: int) -> bool:
        """Delete a student by ID."""
        for i, student in enumerate(self.students):
            if student.student_id == student_id:
                self.students.pop(i)
                return True
        return False
    
    def update_student(self, student_id: int, name: str, marks: Dict[str, float]) -> bool:
        """Update student information."""
        student = self.get_student(student_id)
        if student:
            student.name = name
            student.marks = marks
            student.total_marks = student.calculate_total()
            student.percentage = student.calculate_percentage()
            student.grade = student.calculate_grade()
            return True
        return False
    
    def save_data(self) -> bool:
        """Save all student records to JSON file."""
        try:
            data = [student.to_dict() for student in self.students]
            with open(self.file_name, "w") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def load_data(self) -> bool:
        """Load student records from JSON file."""
        if not os.path.exists(self.file_name):
            return False
        
        try:
            with open(self.file_name, "r") as f:
                data = json.load(f)
                self.students.clear()
                for record in data:
                    student = Student.from_dict(record)
                    self.students.append(student)
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def get_top_performers(self, limit: int = 5) -> List[Student]:
        """Get top performing students."""
        return sorted(self.students, key=lambda s: s.percentage, reverse=True)[:limit]
    
    def get_grade_statistics(self) -> Dict:
        """Get statistics of grades."""
        grades = {}
        for student in self.students:
            grade = student.grade
            grades[grade] = grades.get(grade, 0) + 1
        return grades


# ============== GUI APPLICATION ==============
class StudentResultGUI:
    """Tkinter GUI for Student Result Management System."""
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Student Result Management System - EduTech Solutions")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        self.system = StudentManagementSystem()
        self.selected_student_id = None
        
        # Configure style
        self.configure_styles()
        
        # Create menu
        self.create_menu()
        
        # Create main interface
        self.create_main_interface()
        
        # Load data on startup
        self.refresh_table()
    
    def configure_styles(self):
        """Configure GUI styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TLabel', font=('Arial', 10))
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        style.configure('TButton', font=('Arial', 10))
    
    def create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Records", command=self.save_records)
        file_menu.add_command(label="Load Records", command=self.load_records)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="View Results", command=self.view_results)
        view_menu.add_command(label="Top Performers", command=self.show_top_performers)
        view_menu.add_command(label="Grade Statistics", command=self.show_statistics)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_main_interface(self):
        """Create main GUI interface."""
        # Create notebook (tabs)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Add/Update Student
        self.add_student_frame = ttk.Frame(notebook)
        notebook.add(self.add_student_frame, text="Add/Update Student")
        self.create_add_student_section()
        
        # Tab 2: View Records
        self.view_frame = ttk.Frame(notebook)
        notebook.add(self.view_frame, text="View Records")
        self.create_view_section()
        
        # Tab 3: Search & Delete
        self.search_frame = ttk.Frame(notebook)
        notebook.add(self.search_frame, text="Search & Manage")
        self.create_search_section()
    
    def create_add_student_section(self):
        """Create section for adding/updating students."""
        # Input frame
        input_frame = ttk.LabelFrame(self.add_student_frame, text="Student Information", padding=10)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Student ID
        ttk.Label(input_frame, text="Student ID:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_id = ttk.Entry(input_frame, width=20)
        self.entry_id.grid(row=0, column=1, sticky="w", pady=5)
        
        # Name
        ttk.Label(input_frame, text="Name:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_name = ttk.Entry(input_frame, width=20)
        self.entry_name.grid(row=1, column=1, sticky="w", pady=5)
        
        # Marks frame
        marks_frame = ttk.LabelFrame(input_frame, text="Marks (0-100)", padding=10)
        marks_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        
        self.mark_entries = {}
        for i, subject in enumerate(Student.SUBJECTS):
            ttk.Label(marks_frame, text=f"{subject}:").grid(row=i, column=0, sticky="w", pady=5)
            entry = ttk.Entry(marks_frame, width=15)
            entry.grid(row=i, column=1, sticky="w", pady=5)
            self.mark_entries[subject] = entry
        
        # Buttons frame
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=15)
        
        ttk.Button(button_frame, text="Add Student", command=self.add_student).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update Student", command=self.update_student).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear Fields", command=self.clear_fields).pack(side="left", padx=5)
    
    def create_view_section(self):
        """Create section for viewing student records."""
        # Table frame
        table_frame = ttk.Frame(self.view_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create treeview with scrollbars
        scrollbar_y = ttk.Scrollbar(table_frame)
        scrollbar_y.pack(side="right", fill="y")
        
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")
        
        columns = ("ID", "Name", "Total Marks", "Percentage", "Grade")
        self.tree = ttk.Treeview(
            table_frame, 
            columns=columns, 
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            height=20
        )
        
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        # Define headings
        widths = [80, 150, 120, 120, 80]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
        
        self.tree.pack(fill="both", expand=True)
        
        # Bind row selection
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)
    
    def create_search_section(self):
        """Create section for searching and managing students."""
        # Search frame
        search_frame = ttk.LabelFrame(self.search_frame, text="Search Student", padding=10)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(search_frame, text="Search by ID:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(search_frame, width=20)
        self.search_entry.pack(side="left", padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_student).pack(side="left", padx=5)
        
        # Result frame
        result_frame = ttk.LabelFrame(self.search_frame, text="Student Details", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.result_text = tk.Text(result_frame, height=20, width=60, state="disabled")
        self.result_text.pack(fill="both", expand=True)
        
        # Action buttons
        button_frame = ttk.Frame(self.search_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="Delete Selected Student", command=self.delete_student).pack(side="left", padx=5)
        ttk.Button(button_frame, text="View Full Details", command=self.view_full_details).pack(side="left", padx=5)
    
    def add_student(self):
        """Add a new student."""
        try:
            student_id = int(self.entry_id.get())
            name = self.entry_name.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Please enter student name")
                return
            
            # Check if student already exists
            if self.system.get_student(student_id):
                messagebox.showerror("Error", "Student ID already exists")
                return
            
            # Get marks
            marks = {}
            for subject in Student.SUBJECTS:
                try:
                    mark = float(self.mark_entries[subject].get())
                    if mark < 0 or mark > 100:
                        raise ValueError
                    marks[subject] = mark
                except ValueError:
                    messagebox.showerror("Error", f"Invalid marks for {subject}. Please enter 0-100")
                    return
            
            # Add student
            if self.system.add_student(student_id, name, marks):
                self.refresh_table()
                self.clear_fields()
                student = self.system.get_student(student_id)
                messagebox.showinfo("Success", f"Student Added!\nGrade: {student.grade}\nPercentage: {student.percentage:.2f}%")
            else:
                messagebox.showerror("Error", "Failed to add student")
        
        except ValueError:
            messagebox.showerror("Error", "Invalid Student ID. Please enter a number")
    
    def update_student(self):
        """Update an existing student."""
        try:
            student_id = int(self.entry_id.get())
            name = self.entry_name.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Please enter student name")
                return
            
            marks = {}
            for subject in Student.SUBJECTS:
                try:
                    mark = float(self.mark_entries[subject].get())
                    if mark < 0 or mark > 100:
                        raise ValueError
                    marks[subject] = mark
                except ValueError:
                    messagebox.showerror("Error", f"Invalid marks for {subject}. Please enter 0-100")
                    return
            
            if self.system.update_student(student_id, name, marks):
                self.refresh_table()
                self.clear_fields()
                student = self.system.get_student(student_id)
                messagebox.showinfo("Success", f"Student Updated!\nGrade: {student.grade}\nPercentage: {student.percentage:.2f}%")
            else:
                messagebox.showerror("Error", "Student not found")
        
        except ValueError:
            messagebox.showerror("Error", "Invalid Student ID")
    
    def delete_student(self):
        """Delete a student."""
        try:
            search_id = int(self.search_entry.get())
            if self.system.delete_student(search_id):
                self.refresh_table()
                self.search_entry.delete(0, tk.END)
                self.result_text.config(state="normal")
                self.result_text.delete("1.0", tk.END)
                self.result_text.config(state="disabled")
                messagebox.showinfo("Success", "Student deleted successfully")
            else:
                messagebox.showerror("Error", "Student not found")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Student ID")
    
    def search_student(self):
        """Search for a student by ID."""
        try:
            student_id = int(self.search_entry.get())
            student = self.system.get_student(student_id)
            
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            
            if student:
                details = f"Student ID: {student.student_id}\n"
                details += f"Name: {student.name}\n"
                details += f"{'='*40}\n\n"
                details += "Marks by Subject:\n"
                for subject, mark in student.marks.items():
                    details += f"  {subject}: {mark}/100\n"
                details += f"\n{'='*40}\n"
                details += f"Total Marks: {student.total_marks}/500\n"
                details += f"Percentage: {student.percentage:.2f}%\n"
                details += f"Grade: {student.grade}\n"
                
                self.result_text.insert("1.0", details)
            else:
                self.result_text.insert("1.0", "Student not found")
            
            self.result_text.config(state="disabled")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Student ID")
    
    def view_full_details(self):
        """View full details of selected student."""
        self.search_student()
    
    def on_tree_select(self, event):
        """Handle tree selection."""
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            values = self.tree.item(item)['values']
            self.selected_student_id = values[0]
            
            # Populate fields
            student = self.system.get_student(self.selected_student_id)
            if student:
                self.entry_id.delete(0, tk.END)
                self.entry_id.insert(0, str(student.student_id))
                self.entry_name.delete(0, tk.END)
                self.entry_name.insert(0, student.name)
                
                for subject in Student.SUBJECTS:
                    self.mark_entries[subject].delete(0, tk.END)
                    self.mark_entries[subject].insert(0, str(student.marks[subject]))
    
    def refresh_table(self):
        """Refresh the student table."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for student in self.system.get_all_students():
            self.tree.insert("", "end", values=(
                student.student_id,
                student.name,
                f"{student.total_marks}/500",
                f"{student.percentage:.2f}%",
                student.grade
            ))
    
    def clear_fields(self):
        """Clear input fields."""
        self.entry_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        for entry in self.mark_entries.values():
            entry.delete(0, tk.END)
    
    def save_records(self):
        """Save records to file."""
        if self.system.save_data():
            messagebox.showinfo("Success", "Records saved successfully!")
        else:
            messagebox.showerror("Error", "Failed to save records")
    
    def load_records(self):
        """Load records from file."""
        if self.system.load_data():
            self.refresh_table()
            messagebox.showinfo("Success", "Records loaded successfully!")
        else:
            messagebox.showwarning("Info", "No saved records found")
    
    def view_results(self):
        """Show all student results."""
        results = "Student Results Summary\n"
        results += "=" * 60 + "\n\n"
        
        for student in self.system.get_all_students():
            results += f"ID: {student.student_id} | Name: {student.name}\n"
            results += f"Total: {student.total_marks}/500 | Percentage: {student.percentage:.2f}% | Grade: {student.grade}\n"
            results += "-" * 60 + "\n"
        
        self.show_info_window("Student Results", results)
    
    def show_top_performers(self):
        """Show top performing students."""
        if not self.system.students:
            messagebox.showinfo("Info", "No students in the system")
            return
        
        top = self.system.get_top_performers(10)
        results = "Top Performers\n"
        results += "=" * 60 + "\n\n"
        
        for i, student in enumerate(top, 1):
            results += f"{i}. {student.name} (ID: {student.student_id})\n"
            results += f"   Percentage: {student.percentage:.2f}% | Grade: {student.grade}\n\n"
        
        self.show_info_window("Top Performers", results)
    
    def show_statistics(self):
        """Show grade statistics."""
        if not self.system.students:
            messagebox.showinfo("Info", "No students in the system")
            return
        
        stats = self.system.get_grade_statistics()
        results = "Grade Statistics\n"
        results += "=" * 60 + "\n\n"
        results += f"Total Students: {len(self.system.students)}\n\n"
        
        for grade in ['A', 'B', 'C', 'D', 'F']:
            count = stats.get(grade, 0)
            percentage = (count / len(self.system.students)) * 100 if self.system.students else 0
            results += f"Grade {grade}: {count} students ({percentage:.1f}%)\n"
        
        self.show_info_window("Grade Statistics", results)
    
    def show_about(self):
        """Show about dialog."""
        about_text = """
Student Result Management System
EduTech Solutions

Version 1.0
© 2026 EduTech Solutions

A comprehensive system for managing student records,
calculating grades, and generating academic reports.

Features:
• Add and manage student records
• Calculate grades based on subject marks
• View detailed student results
• Save and load records
• Performance analytics
        """
        messagebox.showinfo("About", about_text)
    
    def show_info_window(self, title, content):
        """Show information in a new window."""
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("700x400")
        
        text = tk.Text(window, wrap="word", padx=10, pady=10)
        text.pack(fill="both", expand=True)
        text.insert("1.0", content)
        text.config(state="disabled")
        
        ttk.Button(window, text="Close", command=window.destroy).pack(pady=10)


# ============== MAIN APPLICATION ==============
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentResultGUI(root)
    root.mainloop()