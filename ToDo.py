from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.app import App
from datetime import datetime

class Task:
    def __init__(self, title, description, category, priority, due_date, status="New"):
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.due_date = due_date
        self.status = status

class ToDoListApp(App):
    MAX_TASKS = 4
    
    def build(self):
        self.tasks = []
        self.task_widgets = {} 

        # UI components with default values
        self.title_input = TextInput(hint_text="Title")
        self.description_input = TextInput(hint_text="Description")
        self.category_spinner = Spinner(text="Personal", values=["Personal", "Work", "Study"])
        self.priority_spinner = Spinner(text="Low", values=["Low", "Medium", "High"])
        self.due_date_input = TextInput(hint_text="Due Date (YYYY-MM-DD)")
        self.status_label = Button(text="Status: New", on_release=self.show_global_status_dropdown)
        self.task_list_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.task_list_layout.bind(minimum_height=self.task_list_layout.setter('height'))
        self.scroll_view = ScrollView()

        # Dropdown for status selection
        self.status_dropdown = DropDown()
        for status in ["New", "In Progress", "Completed"]:
            btn = Button(text=status, size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: self.update_status(btn.text))
            self.status_dropdown.add_widget(btn)

        # Buttons
        add_button = Button(text="Add Task", on_press=self.add_task)
        clear_button = Button(text="Clear", on_press=self.clear_fields)

        # Layout setup
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        input_layout = GridLayout(cols=2, spacing=10, row_force_default=True, row_default_height=40)
        # Table headings
        table_headings = GridLayout(cols=6, spacing=10, size_hint_y=None, height=30)
        table_headings.add_widget(Label(text="Title"))
        table_headings.add_widget(Label(text="Description"))
        table_headings.add_widget(Label(text="Due Date"))
        table_headings.add_widget(Label(text="Category"))
        table_headings.add_widget(Label(text="Priority"))
        table_headings.add_widget(Label(text="Status"))

        # Combine headings and task_list_layout in a box layout
        table_layout = BoxLayout(orientation='vertical')
        table_layout.add_widget(table_headings)
        table_layout.add_widget(self.task_list_layout)

        # Combine everything in a scroll view
        self.scroll_view.add_widget(table_layout)

        # Add UI components to layout
        input_layout.add_widget(self.title_input)
        input_layout.add_widget(self.description_input)
        input_layout.add_widget(self.category_spinner)
        input_layout.add_widget(self.priority_spinner)
        input_layout.add_widget(self.due_date_input)
        input_layout.add_widget(add_button)
        input_layout.add_widget(clear_button)

        layout.add_widget(input_layout)
        layout.add_widget(self.status_label)  # Fix this line
        layout.add_widget(self.scroll_view)

        return layout

    def add_task(self, instance):
        if len(self.tasks) >= self.MAX_TASKS:
            print("Maximum number of tasks reached.")
            return

        title = self.title_input.text.strip()
        description = self.description_input.text.strip()
        category = self.category_spinner.text.strip()
        priority = self.priority_spinner.text.strip()
        due_date = self.due_date_input.text.strip()

        if not all([title, description, category, priority, due_date]):
            print("Please fill in all required fields.")
            return

        new_task = Task(title, description, category, priority, due_date)
        self.tasks.append(new_task)
        print(f"Task added: {new_task.__dict__}")
        self.update_task_list()
        self.clear_fields()


    def show_global_status_dropdown(self, instance):
        self.status_dropdown.open(instance)

    def update_task_list(self):
        # Clear only the task rows, not the table headings
        self.task_list_layout.clear_widgets(children=self.task_list_layout.children[:1])

        # Table rows
        for task in self.tasks:
            task_layout = GridLayout(cols=6, spacing=10, size_hint_y=None, height=30)
            title_label = Label(text=f"{task.title}", markup=True)
            description_label = Label(text=f"{task.description}", markup=True)
            due_date_label = Label(text=f"{task.due_date}", markup=True)
            category_label = Label(text=f"{task.category}", markup=True)
            priority_label = Label(text=f"{task.priority}", markup=True)

            # Create a button for the status
            status_button = Button(text=f"{task.status}", size_hint_y=None, height=30)
            status_button.bind(on_release=lambda instance, task=task: self.show_status_dropdown(instance, task))

            # Apply strikethrough effect for completed tasks
            if task.status == "Completed":
                for label in [title_label, description_label, due_date_label, category_label, priority_label, status_button]:
                    label.text = "[s]" + label.text + "[/s]"

            # Add the labels and status button to the task layout
            task_layout.add_widget(title_label)
            task_layout.add_widget(description_label)
            task_layout.add_widget(due_date_label)
            task_layout.add_widget(category_label)
            task_layout.add_widget(priority_label)
            task_layout.add_widget(status_button)

            # Add the task layout to the task_list_layout
            self.task_list_layout.add_widget(task_layout)

            # Update the existing task widget if it exists
            if task in self.task_widgets:
                self.update_task_widget(task)

        # Calculate the content height dynamically
        content_height = sum(widget.height for widget in self.task_list_layout.children)
        self.scroll_view.height = content_height

        # Ensure the ScrollView scrolls if necessary
        self.scroll_view.scroll_y = 1.0



    def create_task_widget(self, task):
        task_layout = GridLayout(cols=6, spacing=10, size_hint_y=None, height=30)
        title_label = Label(text=f"{task.title}")
        description_label = Label(text=f"{task.description}")
        due_date_label = Label(text=f"{task.due_date}")
        category_label = Label(text=f"{task.category}")
        priority_label = Label(text=f"{task.priority}")

        status_button = Button(text=f"{task.status}", size_hint_y=None, height=30)
        status_button.bind(on_release=lambda instance, t=task: self.show_status_dropdown(instance, t))

        task_layout.add_widget(title_label)
        task_layout.add_widget(description_label)
        task_layout.add_widget(due_date_label)
        task_layout.add_widget(category_label)
        task_layout.add_widget(priority_label)
        task_layout.add_widget(status_button)

        self.task_widgets[task] = task_layout
        self.task_list_layout.add_widget(task_layout)

    def update_task_widget(self, task):
        task_layout = self.task_widgets[task]
        # Update the content of the task widget (e.g., status button text)
        for widget in task_layout.children:
            if isinstance(widget, Button):
                widget.text = f"{task.status}"
                if task.status == "Completed":
                    widget.text = "[s]" + widget.text + "[/s]"

    def show_status_dropdown(self, instance, task):
        # Use task-specific dropdown
        task_dropdown = DropDown()

        for status in ["New", "In Progress", "Completed"]:
            btn = Button(text=status, size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: self.update_task_status(task, btn.text))
            task_dropdown.add_widget(btn)

        task_dropdown.open(instance)

    def update_task_status(self, task, new_status):
        print(f"Updating task status: {task.title} - New Status: {new_status}")
        task.status = new_status
        self.update_task_list()


    def clear_fields(self, instance=None):
        self.title_input.text = ""
        self.description_input.text = ""
        self.category_spinner.text = "Category"
        self.priority_spinner.text = "Priority"
        self.due_date_input.text = ""
        self.status_label.text = "Status: New"

if __name__ == '__main__':
    ToDoListApp().run()
