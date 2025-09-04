import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python To-Do List")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Data file
        self.data_file = "tasks.json"
        
        # Load tasks
        self.tasks = self.load_tasks()
        
        # Create GUI
        self.create_gui()
        
        # Populate tasks
        self.update_task_list()
    
    def create_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Python To-Do List", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Task entry
        ttk.Label(main_frame, text="New Task:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.task_entry = ttk.Entry(main_frame, width=40)
        self.task_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(5, 0))
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        # Priority
        ttk.Label(main_frame, text="Priority:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(main_frame, textvariable=self.priority_var, 
                                     values=["Low", "Medium", "High"], state="readonly", width=10)
        priority_combo.grid(row=2, column=1, sticky=tk.W, pady=(0, 5), padx=(5, 0))
        
        # Add button
        add_btn = ttk.Button(main_frame, text="Add Task", command=self.add_task)
        add_btn.grid(row=2, column=2, sticky=tk.W, pady=(0, 5), padx=(5, 0))
        
        # Task list frame
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Task list
        self.task_listbox = tk.Listbox(list_frame, height=15, yscrollcommand=scrollbar.set,
                                      selectmode=tk.SINGLE, font=("Arial", 10))
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Bind selection event
        self.task_listbox.bind('<<ListboxSelect>>', self.on_task_select)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
        # Action buttons
        self.complete_btn = ttk.Button(button_frame, text="Mark Complete", 
                                      command=self.complete_task, state=tk.DISABLED)
        self.complete_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.edit_btn = ttk.Button(button_frame, text="Edit", 
                                  command=self.edit_task, state=tk.DISABLED)
        self.edit_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.delete_btn = ttk.Button(button_frame, text="Delete", 
                                    command=self.delete_task, state=tk.DISABLED)
        self.delete_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Status bar
        self.status_var = tk.StringVar(value=f"Total tasks: {len(self.tasks)}")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_tasks(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.tasks, f)
    
    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.tasks):
            status = "✓" if task['completed'] else "○"
            priority = task['priority'][0]
            self.task_listbox.insert(tk.END, f"{i+1}. [{priority}] {task['task']} {status}")
            
            # Color coding for completed tasks and priorities
            if task['completed']:
                self.task_listbox.itemconfig(i, {'fg': 'gray'})
            elif task['priority'] == 'High':
                self.task_listbox.itemconfig(i, {'fg': 'red'})
            elif task['priority'] == 'Medium':
                self.task_listbox.itemconfig(i, {'fg': 'orange'})
        
        self.status_var.set(f"Total tasks: {len(self.tasks)} | Completed: {sum(1 for t in self.tasks if t['completed'])}")
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task.")
            return
        
        self.tasks.append({
            'task': task_text,
            'priority': self.priority_var.get(),
            'completed': False
        })
        
        self.save_tasks()
        self.update_task_list()
        self.task_entry.delete(0, tk.END)
        self.task_entry.focus()
    
    def on_task_select(self, event):
        selection = self.task_listbox.curselection()
        if selection:
            self.complete_btn.config(state=tk.NORMAL)
            self.edit_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
        else:
            self.complete_btn.config(state=tk.DISABLED)
            self.edit_btn.config(state=tk.DISABLED)
            self.delete_btn.config(state=tk.DISABLED)
    
    def complete_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            self.tasks[index]['completed'] = not self.tasks[index]['completed']
            self.save_tasks()
            self.update_task_list()
    
    def edit_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            task = self.tasks[index]
            
            # Create edit window
            edit_win = tk.Toplevel(self.root)
            edit_win.title("Edit Task")
            edit_win.geometry("400x200")
            edit_win.resizable(False, False)
            edit_win.transient(self.root)
            edit_win.grab_set()
            
            # Center the window
            edit_win.update_idletasks()
            x = self.root.winfo_x() + (self.root.winfo_width() - edit_win.winfo_width()) // 2
            y = self.root.winfo_y() + (self.root.winfo_height() - edit_win.winfo_height()) // 2
            edit_win.geometry(f"+{x}+{y}")
            
            # Edit frame
            edit_frame = ttk.Frame(edit_win, padding="10")
            edit_frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(edit_frame, text="Task:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
            
            task_var = tk.StringVar(value=task['task'])
            task_entry = ttk.Entry(edit_frame, textvariable=task_var, width=40)
            task_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10), padx=(5, 0))
            
            ttk.Label(edit_frame, text="Priority:").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
            
            priority_var = tk.StringVar(value=task['priority'])
            priority_combo = ttk.Combobox(edit_frame, textvariable=priority_var, 
                                         values=["Low", "Medium", "High"], state="readonly", width=10)
            priority_combo.grid(row=1, column=1, sticky=tk.W, pady=(0, 10), padx=(5, 0))
            
            # Button frame
            btn_frame = ttk.Frame(edit_frame)
            btn_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
            
            def save_edit():
                new_text = task_var.get().strip()
                if not new_text:
                    messagebox.showwarning("Warning", "Task cannot be empty.")
                    return
                
                self.tasks[index]['task'] = new_text
                self.tasks[index]['priority'] = priority_var.get()
                self.save_tasks()
                self.update_task_list()
                edit_win.destroy()
            
            ttk.Button(btn_frame, text="Save", command=save_edit).pack(side=tk.LEFT, padx=(0, 5))
            ttk.Button(btn_frame, text="Cancel", command=edit_win.destroy).pack(side=tk.LEFT)
            
            # Set focus to entry
            task_entry.focus()
            task_entry.select_range(0, tk.END)
    
    def delete_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
                del self.tasks[index]
                self.save_tasks()
                self.update_task_list()
                # Clear selection
                self.task_listbox.selection_clear(0, tk.END)

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
