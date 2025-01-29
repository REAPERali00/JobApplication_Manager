
import tkinter as tk
from tkinter import ttk, scrolledtext
from models.job import Job, ApplicationStatus
from datetime import datetime
import makeCv
import database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App:
    def __init__(self) -> None:
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Job Application Manager")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f5")

        # Define fields
        self.job = None
        self.cols = [
            'Company', 'Contact name', 'Position', 'Email',
            'Company website', 'Company address', 'Application date',
            'Cover letter sent?', 'Interview date', 'How did you find them?', 'Resume', 'Application Status', 'Notes',
        ]

        # Organize the UI
        self.setup_ui()

    def setup_ui(self):
        """Organize the UI into sections for better layout."""
        # Frame for form inputs
        form_frame = ttk.LabelFrame(self.root, text="Job Application Form", padding=10)
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Set background color for form_frame to match root
        form_frame.configure(style="Custom.TLabelframe")

        # Subframe for text inputs (left side)
        text_input_frame = ttk.Frame(form_frame)
        text_input_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        # Subframe for scrolled text boxes (right side)
        scrolled_text_frame = ttk.Frame(form_frame)
        scrolled_text_frame.grid(row=0, column=1, sticky="ne", padx=10, pady=10)

        # Frame for buttons
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, pady=10)

        # Create entry fields in the text input frame
        self.entries = self.create_entry_fields(text_input_frame)

        # Create scrolled text boxes in the scrolled text frame
        self.text_boxes = self.create_text_box(scrolled_text_frame)

        # Add buttons to the button frame
        ttk.Button(button_frame, text="Submit", command=lambda: self.submit(self.entries, self.text_boxes)).pack(
            side=tk.LEFT, padx=10
        )
        ttk.Button(button_frame, text="Show Charts", command=self.show_chart).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="View Database", command=self.view_db).pack(side=tk.LEFT, padx=10)

        # Configure resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Apply styling for consistency
        self.setup_styles()

    def setup_styles(self):
        """Apply custom styles to the application."""
        style = ttk.Style()
        style.configure("Custom.TLabelframe", background="#f0f0f5")
        style.configure("Custom.TLabelframe.Label", font=("Arial", 12, "bold"))
        style.configure("Custom.TLabel", background="#f0f0f5", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10), padding=5)

    def create_entry_fields(self, parent):
        """Create entry fields dynamically based on column names."""
        entries = {}
        for index, column_name in enumerate(self.cols):
            # Skip scrolled text fields
            if column_name in ["Application text", "Cover letter text"]:
                continue

            # Create a label and input field
            label = ttk.Label(parent, text=column_name, style="Custom.TLabel")
            label.grid(row=index, column=0, sticky='e', padx=5, pady=5)

            # Handle dropdown for Resume
            if column_name == 'Resume':
                # options = ['Software', 'part_time', 'Embedded_systems', 'Webdev']
                options =  makeCv.get_resume() or [""]
                selected_option = tk.StringVar()
                dropdown = ttk.Combobox(parent, textvariable=selected_option, values=options, state="readonly")
                dropdown.grid(row=index, column=1, sticky='ew', padx=5, pady=5)
                dropdown.set(options[0])  # Set the default value
                entries[column_name] = selected_option
                continue

            # Handle dropdown for Application Status
            if column_name == 'Application Status':
                status_options = [status.value for status in ApplicationStatus]
                selected_status = tk.StringVar()
                dropdown = ttk.Combobox(parent, textvariable=selected_status, values=status_options, state="readonly")
                dropdown.grid(row=index, column=1, sticky='ew', padx=5, pady=5)
                dropdown.set(status_options[0])  # Set the default value
                entries[column_name] = selected_status
                continue

            # Create an entry field
            entry = ttk.Entry(parent)
            entry.grid(row=index, column=1, sticky='ew', padx=5, pady=5)

            # Store the entry widget in a dictionary
            entries[column_name] = entry
        return entries

    def create_text_box(self, parent):
        """Create scrolled text boxes for application and cover letter."""
        text_boxes = {}
        labels = ["Application text", "Cover letter text"]

        for idx, label_text in enumerate(labels):
            # Create a label and scrolled text box
            label = ttk.Label(parent, text=label_text, style="Custom.TLabel")
            label.grid(row=idx, column=0, sticky='w', padx=5, pady=5)

            text_box = scrolledtext.ScrolledText(parent, width=50, height=8, wrap=tk.WORD, font=("Arial", 10))
            text_box.grid(row=idx, column=1, padx=5, pady=5)

            # Store the text box in a dictionary
            text_boxes[label_text] = text_box

        return text_boxes
    def submit(self, entries, text_boxes):
        """Handle form submission."""
        self.create_job(entries, text_boxes)
        if not self.job:
            print("Could not process job")
            exit(1)

        makeCv.write_cache(self.job)
        makeCv.submission_folder(self.job)
        print("Created folder and prompt")

        database.save_job(self.job)
        print("Saved job")

    def create_job(self, entries, text_boxes):
        """Extract and process form data."""
        try:
            data = {}
            for key, entry in entries.items():
                if key in ["Resume", "Application Status"]:
                    data[key] = entry.get()  # Handle dropdown values
                else:
                    value = entry.get().strip()
                    data[key] = value if value else None

            for key, text_box in text_boxes.items():
                value = text_box.get("1.0", "end-1c").strip()
                data[key] = value if value else None

            if data.get("Application date"):
                data["Application date"] = datetime.strptime(data["Application date"], "%Y-%m-%d").date()

            if data.get("Interview date"):
                data["Interview date"] = datetime.strptime(data["Interview date"], "%Y-%m-%d").date()

            if data.get("Cover letter sent?"):
                data["Cover letter sent?"] = data["Cover letter sent?"].lower() in ["yes", "true", "1"]

            self.job = Job(
                company=data.get("Company"),
                contact_name=data.get("Contact name"),
                position=data.get("Position"),
                email=data.get("Email"),
                company_website=data.get("Company website"),
                company_address=data.get("Company address"),
                application_date=data.get("Application date"),
                cover_letter_sent=data.get("Cover letter sent?"),
                interview_date=data.get("Interview date"),
                how_did_you_find_them=data.get("How did you find them?"),
                resume=data.get("Resume"),
                notes=data.get("Notes"),
                application=data.get("Application text"),
                cover_letter=data.get("Cover letter text"),
                application_status=data.get("Application Status"),
            )
            print("Job model created:")
            print(self.job.dict())
        except Exception as e:
            print("Error processing form submission:", str(e))

     # Function to create the application rate pie chart and return the figure
    def app_pie_rate(self):
        # Fetch application data from the database
        data = database.fetch_application_data()

        # Create a figure and axis for the chart
        fig, ax = plt.subplots()
        statuses = [status for status, _ in data]
        counts = [count for _, count in data]

        # Plot the data
        ax.pie(counts, labels=statuses, autopct='%1.1f%%', startangle=90)
        ax.set_title('Application Rate')

        return fig

    # Function to create the application rate over time chart and return the figure
    def app_rate_over_time(self):
        try:
            # Fetch application data from the database
            data = database.fetch_application_stat()

            # Extract valid dates and counts together, filtering out None dates
            filtered_data = [(datetime.strptime(date, "%Y-%m-%d"), count) for date, count in data if date is not None]

            # Split filtered data into two lists: dates and counts
            dates, counts = zip(*filtered_data) if filtered_data else ([], [])

            # Check if we have valid data
            if not dates:
                print("No valid data to plot.")
                return None

            # Calculate cumulative counts
            cumulative_counts = []
            total = 0
            for count in counts:
                total += count
                cumulative_counts.append(total)

            # Create a figure and axis for the chart
            fig, ax = plt.subplots()
            ax.plot(dates, cumulative_counts, marker='o', linestyle='-', color='b')

            # Format the x-axis to show dates properly
            fig.autofmt_xdate()

            # Add labels and title
            ax.set_xlabel('Date')
            ax.set_ylabel('Cumulative Number of Applications')
            ax.set_title('Application Rate Over Time')

            return fig
        except Exception as e:
            print("Error generating application rate chart:", str(e))
            return None

    def show_chart(self):
        """Display charts in a single window."""
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Application Rate Chart")

        pie_chart = self.app_pie_rate()
        line_chart = self.app_rate_over_time()

        if pie_chart:
            canvas_pie = FigureCanvasTkAgg(pie_chart, master=chart_window)
            canvas_pie.draw()
            canvas_pie.get_tk_widget().pack(side=tk.LEFT, padx=10, pady=10)

        if line_chart:
            canvas_line = FigureCanvasTkAgg(line_chart, master=chart_window)
            canvas_line.draw()
            canvas_line.get_tk_widget().pack(side=tk.RIGHT, padx=10, pady=10)

    def view_db(self):
            """Display database data in a Treeview and allow editing application status."""
            # Create a new window for viewing and editing database data
            view_window = tk.Toplevel(self.root)
            view_window.title("Database Viewer")

            # Define the database columns (must match the DB schema)
            columns = [
                'id', 'company', 'contact_name', 'position', 'email', 'company_website',
                'company_address', 'application_date', 'cover_letter_sent', 'interview_date',
                'how_did_you_find_them', 'resume', 'notes', 'application', 'cover_letter', 'application_status'
            ]

            # Create a Treeview widget
            tree = ttk.Treeview(view_window, columns=columns, show='headings')
            tree.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

            # Configure Treeview columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            # Add data from the database
            data = database.fetch_all_jobs()  # Fetch all job records from the database
            for row in data:
                tree.insert('', 'end', values=row)

            # Add scrollbar for Treeview
            scrollbar = ttk.Scrollbar(view_window, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.grid(row=0, column=2, sticky="ns")

            # Add a dropdown and button for updating the application status
            selected_item = tk.StringVar()
            dropdown = ttk.Combobox(view_window, textvariable=selected_item)
            dropdown['values'] = [status.value for status in ApplicationStatus]
            dropdown.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

            update_button = tk.Button(view_window, text="Update Status", command=lambda: self.update_status(tree, selected_item.get()))
            update_button.grid(row=1, column=1, padx=10, pady=10)

            # Configure window resizing behavior
            view_window.grid_rowconfigure(0, weight=1)
            view_window.grid_columnconfigure(0, weight=1)

    def update_status(self, tree, new_status):
            """Update the application status for the selected row in the database."""
            try:
                # Get the selected row
                selected_item = tree.selection()
                if not selected_item:
                    print("No row selected.")
                    return

                # Get the job ID from the selected row (assumes 'id' is the first column)
                selected_values = tree.item(selected_item, 'values')
                job_id = selected_values[0]  # Adjust this index based on your schema

                # Update the application status in the database
                database.update_application_status(job_id, new_status)

                # Update the Treeview display
                updated_values = list(selected_values)
                updated_values[-1] = new_status  # Update the last column (application_status)
                tree.item(selected_item, values=updated_values)

                print(f"Updated application status for job ID {job_id} to {new_status}.")
            except Exception as e:
                print("Error updating application status:", str(e))

    def start(self):
        """Start the application."""
        self.root.mainloop()
        makeCv.get_resume()


# Initialize and start the application
if __name__ == "__main__":
    database.initialize_db()
    app = App()
    app.start()

