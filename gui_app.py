import customtkinter as ctk
from tkinter import ttk, messagebox
from main import StudentManagementSystem

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.sms = StudentManagementSystem()

        # Configure window
        self.title("Student Management System")
        self.geometry("1100x580")

        # Configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Student System", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Inputs
        self.entry_id = ctk.CTkEntry(self.sidebar_frame, placeholder_text="ID")
        self.entry_id.grid(row=1, column=0, padx=20, pady=10)
        
        self.entry_name = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Name")
        self.entry_name.grid(row=2, column=0, padx=20, pady=10)

        self.entry_age = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Age")
        self.entry_age.grid(row=3, column=0, padx=20, pady=10)

        self.entry_course = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Course")
        self.entry_course.grid(row=4, column=0, padx=20, pady=10)

        self.entry_marks = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Marks")
        self.entry_marks.grid(row=5, column=0, padx=20, pady=10)

        # Buttons
        self.add_button = ctk.CTkButton(self.sidebar_frame, text="Add Student", command=self.add_student_event)
        self.add_button.grid(row=7, column=0, padx=20, pady=10)
        
        self.update_button = ctk.CTkButton(self.sidebar_frame, text="Update Student", command=self.update_student_event)
        self.update_button.grid(row=8, column=0, padx=20, pady=10)

        self.delete_button = ctk.CTkButton(self.sidebar_frame, text="Delete Student", command=self.delete_student_event, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.delete_button.grid(row=9, column=0, padx=20, pady=10)
        
        self.save_button = ctk.CTkButton(self.sidebar_frame, text="Save & Exit", command=self.save_and_exit_event, fg_color="green")
        self.save_button.grid(row=10, column=0, padx=20, pady=(10, 20))


        # Main Area
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Search by Name")
        self.search_entry.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="ew")
        
        self.search_button = ctk.CTkButton(self, text="Search", width=100, command=self.search_event)
        self.search_button.grid(row=0, column=2, padx=(10, 20), pady=(20, 0), sticky="ew")

        # Treeview (Table)
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview", 
                             background="#2a2d2e", 
                             foreground="white", 
                             fieldbackground="#2a2d2e", 
                             rowheight=25)
        self.style.map('Treeview', background=[('selected', '#3B8ED0')])
        
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.grid(row=1, column=1, columnspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.tree_scroll = ctk.CTkScrollbar(self.tree_frame)
        self.tree_scroll.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Name", "Age", "Course", "Marks"), show="headings", yscrollcommand=self.tree_scroll.set)
        self.tree_scroll.configure(command=self.tree.yview)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Course", text="Course")
        self.tree.heading("Marks", text="Marks")
        
        self.tree.column("ID", width=100)
        self.tree.column("Name", width=200)
        self.tree.column("Age", width=80)
        self.tree.column("Course", width=150)
        self.tree.column("Marks", width=100)
        
        self.tree.pack(expand=True, fill="both")
        
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        self.refresh_table()

    def clear_inputs(self):
        self.entry_id.delete(0, 'end')
        self.entry_name.delete(0, 'end')
        self.entry_age.delete(0, 'end')
        self.entry_course.delete(0, 'end')
        self.entry_marks.delete(0, 'end')

    def refresh_table(self, students=None):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        if students is None:
            students = self.sms.get_all_students()
            
        for s in students:
            self.tree.insert("", "end", values=s)

    def add_student_event(self):
        sid = self.entry_id.get()
        name = self.entry_name.get()
        age = self.entry_age.get()
        course = self.entry_course.get()
        marks = self.entry_marks.get()
        
        if not sid or not name or not age or not course or not marks:
            messagebox.showerror("Error", "All fields are required.")
            return

        success, msg = self.sms.add_student(sid, name, age, course, marks)
        if success:
            messagebox.showinfo("Success", msg)
            self.clear_inputs()
            self.refresh_table()
        else:
            messagebox.showerror("Error", msg)

    def update_student_event(self):
        # Update is tricky with this layout, let's just delete the old ID and Add new for simplicity 
        # OR more robustly, update specific fields. 
        # Strategy: The user selects a row, it fills the inputs. 
        # They change the inputs (except ID shouldn't stick if it's the key, but let's assume ID is immutable or key).
        
        sid = self.entry_id.get()
        if not self.sms.student_exists(sid):
            messagebox.showerror("Error", "Student ID not found or cannot change ID.")
            return

        # We treat this as updating Name/Age/Course/Marks for the given ID
        # Since our backend updates one field at a time, we'll just update all 4 sequentially or refactor backend.
        # Let's call update for each field for now.
        
        self.sms.update_student(sid, 'Name', self.entry_name.get())
        self.sms.update_student(sid, 'Age', self.entry_age.get())
        self.sms.update_student(sid, 'Course', self.entry_course.get())
        self.sms.update_student(sid, 'Marks', self.entry_marks.get())
        
        messagebox.showinfo("Success", "Student updated successfully!")
        self.refresh_table()
        self.clear_inputs()

    def delete_student_event(self):
        sid = self.entry_id.get()
        if not sid:
            messagebox.showerror("Error", "Please enter or select a Student ID.")
            return
        
        if messagebox.askyesno("Confirm", f"Delete student {sid}?"):
            success, msg = self.sms.delete_student(sid)
            if success:
                messagebox.showinfo("Success", msg)
                self.clear_inputs()
                self.refresh_table()
            else:
                messagebox.showerror("Error", msg)

    def search_event(self):
        query = self.search_entry.get()
        if not query:
            self.refresh_table()
            return
            
        results = self.sms.search_student(query)
        self.refresh_table(results)

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            record = item['values']
            # record is [id, name, age, course, marks]
            
            self.clear_inputs()
            self.entry_id.insert(0, record[0])
            self.entry_name.insert(0, record[1])
            self.entry_age.insert(0, record[2])
            self.entry_course.insert(0, record[3])
            self.entry_marks.insert(0, record[4])

    def save_and_exit_event(self):
        self.sms.save_data()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
