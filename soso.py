import tkinter as tk
from tkinter import messagebox

class VotingSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Voting System")
        self.root.configure(bg='#d9eaff')  # Set background color to light blue
        self.polls = {}  # Store polls in a dictionary
        self.votes = {}  # Store votes in a dictionary
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Login", font=("Arial", 24), bg='#d9eaff').pack(pady=20)
        tk.Label(self.root, text="Username:", bg='#d9eaff').pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()
        tk.Label(self.root, text="Password:", bg='#d9eaff').pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()
        
        tk.Button(self.root, text="Login", command=self.handle_login).pack(pady=10)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "admin":
            self.create_admin_dashboard()
        elif username.isdigit() and password.isdigit():
            if 5230111 <= int(username) <= 5230143 and 5230111 <= int(password) <= 5230143:
                self.create_user_dashboard()
            else:
                messagebox.showerror("Login Error", "Invalid username or password")
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    def create_admin_dashboard(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 24), bg='#d9eaff').pack(pady=20)
        tk.Button(self.root, text="Create Poll", command=self.create_poll_screen).pack(pady=10)
        tk.Button(self.root, text="View Results", command=self.view_results_screen).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)

    def create_poll_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Create Poll", font=("Arial", 24), bg='#d9eaff').pack(pady=20)
        tk.Label(self.root, text="Poll Question:", bg='#d9eaff').pack()
        self.poll_question_entry = tk.Entry(self.root)
        self.poll_question_entry.pack()
        tk.Label(self.root, text="Option 1:", bg='#d9eaff').pack()
        self.option1_entry = tk.Entry(self.root)
        self.option1_entry.pack()
        tk.Label(self.root, text="Option 2:", bg='#d9eaff').pack()
        self.option2_entry = tk.Entry(self.root)
        self.option2_entry.pack()
        
        tk.Button(self.root, text="Submit Poll", command=self.submit_poll).pack(pady=10)
        tk.Button(self.root, text="Back to Dashboard", command=self.create_admin_dashboard).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)

    def submit_poll(self):
        question = self.poll_question_entry.get()
        option1 = self.option1_entry.get()
        option2 = self.option2_entry.get()
        # Store poll details in the dictionary
        self.polls[question] = [option1, option2]
        # Initialize vote counts
        self.votes[question] = {option1: 0, option2: 0}
        messagebox.showinfo("Poll Created", "Poll has been created successfully!")
        self.create_admin_dashboard()

    def create_user_dashboard(self):
        self.clear_screen()
        
        tk.Label(self.root, text="User Dashboard", font=("Arial", 24), bg='#d9eaff').pack(pady=20)
        tk.Button(self.root, text="Vote", command=self.vote_screen).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)

    def vote_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Vote", font=("Arial", 24), bg='#d9eaff').pack(pady=20)
        tk.Label(self.root, text="Select Poll:", bg='#d9eaff').pack()
        
        self.poll_vars = tk.StringVar()
        self.poll_vars.set("Select a Poll")
        
        self.poll_menu = tk.OptionMenu(self.root, self.poll_vars, *self.polls.keys())
        self.poll_menu.pack(pady=10)
        
        tk.Button(self.root, text="Submit", command=self.show_poll_options).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)

    def show_poll_options(self):
        selected_poll = self.poll_vars.get()
        if selected_poll in self.polls:
            options = self.polls[selected_poll]
            self.clear_screen()
            
            tk.Label(self.root, text=f"Vote for: {selected_poll}", font=("Arial", 24), bg='#d9eaff').pack(pady=20)
            
            self.vote_vars = tk.StringVar()
            self.vote_vars.set(options[0])
            
            for option in options:
                tk.Radiobutton(self.root, text=option, variable=self.vote_vars, value=option, bg='#d9eaff').pack(pady=5)
                
            tk.Button(self.root, text="Submit Vote", command=self.submit_vote).pack(pady=10)
            tk.Button(self.root, text="Back to Dashboard", command=self.create_user_dashboard).pack(pady=10)
            tk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)
        else:
            messagebox.showerror("Error", "No poll selected")

    def submit_vote(self):
        selected_poll = self.poll_vars.get()
        selected_option = self.vote_vars.get()
        if selected_poll in self.votes:
            # Update the vote count
            self.votes[selected_poll][selected_option] += 1
            messagebox.showinfo("Vote Submitted", "Your vote has been submitted successfully!")
        else:
            messagebox.showerror("Error", "Error in submitting vote")
        self.create_user_dashboard()

    def view_results_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="View Results", font=("Arial", 24), bg='#d9eaff').pack(pady=20)
        tk.Label(self.root, text="Poll Results:", bg='#d9eaff').pack()
        
        for poll, options in self.polls.items():
            tk.Label(self.root, text=f"{poll}:", bg='#d9eaff').pack()
            for option in options:
                vote_count = self.votes[poll].get(option, 0)
                tk.Label(self.root, text=f" - {option}: {vote_count} votes", bg='#d9eaff').pack()  # Display actual vote count
        
        tk.Button(self.root, text="Back to Dashboard", command=self.create_admin_dashboard).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)

    def logout(self):
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VotingSystemApp(root)
    root.mainloop()
