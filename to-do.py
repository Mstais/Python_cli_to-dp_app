import json 


class Task:
    def __init__(self, description, priority, due_date):
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.is_complete = False

    def __str__(self):
        status = "[X]" if self.is_complete else "[ ]"
        
        # Include all details for a clean view
        return f"{status} {self.description} (Priority: {self.priority}, Due: {self.due_date})"
    
    def mark_complete(self):
        self.is_complete = True
        return f"Task '{self.description}' marked as complete."
    
    def to_dict(self):
        return {
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date,
            "is_complete": self.is_complete 
        }


def display_menu():
    print("Welcome to your To-Do List!\n")
    print("Menu:")
    print("1. Add a new task")
    print("2. View all tasks")
    print("3. Mark a task as complete")
    print("4. Exit")


todo_list = [] 

def save_tasks():
    try:
        
        list_of_dicts = [task.to_dict() for task in todo_list]
        
        with open("todo.json", "w") as f:
            json.dump(list_of_dicts, f, indent=4)
            
    except IOError:
        print("Error: Could not save tasks to file.")
    
def load_tasks():
    global todo_list 

    try:
        with open("todo.json", "r") as f:
        
            list_of_dicts = json.load(f)

            
            rebuilt_tasks = []
            for d in list_of_dicts:
                
                task_obj = Task(d["description"], d["priority"], d["due_date"])
                task_obj.is_complete = d["is_complete"]
                rebuilt_tasks.append(task_obj)

            todo_list = rebuilt_tasks

    
    except (FileNotFoundError, json.JSONDecodeError):
        
        todo_list = []

def add_task():
    description = input("Enter the task description: ")
    priority = input("Enter the priority (e.g., High, Medium, Low): ")
    due_date = input("Enter the due date: ")
    
   
    new_task_object = Task(description, priority, due_date)
    todo_list.append(new_task_object)

    print(f"\nTask '{description}' successfully added!")
    print("-" * 30)

def view_tasks():
    print("\n--- Your Current To-Do List ---")
    
    if len(todo_list) == 0:
        print("Your list is empty! Add a new task (Option 1).")

    else:
        for i, task_object in enumerate(todo_list):
           
            print(f"{i + 1}. {task_object}")

    print("-" * 30)

def complete_task():
    if not todo_list:
        print("\nYour list is empty! Nothing to complete.")
        print("-" * 30)
        return
    
    view_tasks() 
    
    task_num = input("Select the task number you have completed: ")

    try:
        task_index = int(task_num) - 1
        
        task_to_complete = todo_list[task_index] 
        confirmation_message = task_to_complete.mark_complete() 
        
        print(f"\n{confirmation_message}")
        save_tasks()

    except ValueError:
        print("\nInvalid input. Please enter the number of the task.")

    except IndexError:
        print(f"\nError: Please enter a number between 1 and {len(todo_list)}.")

    print("-" * 30)


def main():

    load_tasks()

    while True:
        display_menu()
        choice = input("Enter your choice (1, 2, 3, or 4): ")

        if choice == '1':
            add_task()
            save_tasks() 

        elif choice == '2':
            view_tasks()

        elif choice == '3':
            complete_task()
            # save_tasks() is called inside complete_task() now, but no harm in having it here
            pass 

        elif choice == '4':
            print("Thanks for using the To-Do List! Goodbye.")
            
            save_tasks() 
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()