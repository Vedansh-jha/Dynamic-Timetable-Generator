import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, 
    QLineEdit, QFormLayout, QTableWidget, QTableWidgetItem, QLabel
)
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class TimetableApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynamic Timetable Generator")
        self.setGeometry(100, 100, 1200, 800)

        self.teachers = []
        self.classes = []
        self.timetable = []
        self.time_slots = [
            "9:00 AM - 10:00 AM",
            "10:00 AM - 11:00 AM",
            "11:00 AM - 12:00 PM",
            "12:00 PM - 1:00 PM",
            "2:00 PM - 3:00 PM",
            "3:00 PM - 4:00 PM"
        ]
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        self.init_dashboard()

    def init_dashboard(self):
        layout = QVBoxLayout()

        self.teacher_button = QPushButton("Add Teachers")
        self.class_button = QPushButton("Add Classes")
        self.generate_button = QPushButton("Generate Timetable")
        self.view_timetable_button = QPushButton("View Timetable")

        self.teacher_button.clicked.connect(self.add_teachers)
        self.class_button.clicked.connect(self.add_classes)
        self.generate_button.clicked.connect(self.generate_timetable)
        self.view_timetable_button.clicked.connect(self.view_timetable)

        layout.addWidget(self.teacher_button)
        layout.addWidget(self.class_button)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.view_timetable_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_teachers(self):
        """Opens a form to add teachers."""
        self.teacher_form = TeacherForm(self)
        self.setCentralWidget(self.teacher_form)

    def add_classes(self):
        """Opens a form to add classes."""
        self.class_form = ClassForm(self)
        self.setCentralWidget(self.class_form)

    def generate_timetable(self):
        """Generate the timetable based on teachers, classes, and time slots."""
        self.timetable = [] 
        scheduled_slots = {}

        period_count_by_day = {day: 0 for day in self.days}

        subject_pool = [cls["subject"] for cls in self.classes]
        random.shuffle(subject_pool)

        for cls in self.classes:
            class_name, subject, periods = cls["class_name"], cls["subject"], cls["periods"]

            for day in self.days:
                shuffled_subjects = random.sample(subject_pool, len(subject_pool))

                for period_num in range(periods):
                    if period_count_by_day[day] < len(self.time_slots):
                        period_slot = self.time_slots[period_count_by_day[day]]
                        subject_for_the_day = shuffled_subjects[period_count_by_day[day] % len(shuffled_subjects)]
                        teacher_assigned = False
                        for teacher in self.teachers:
                            if teacher["subject"] == subject_for_the_day and not teacher_assigned:
                                self.timetable.append({
                                    "class": class_name,
                                    "day": day,
                                    "period": period_count_by_day[day] + 1,
                                    "time_slot": period_slot,
                                    "subject": subject_for_the_day,
                                    "teacher": teacher["name"]
                                })
                                period_count_by_day[day] += 1
                                teacher_assigned = True
                                break

        self.statusBar().showMessage("Timetable generated successfully!")

    def view_timetable(self):
        """View the generated timetable."""
        self.timetable_view = TimetableView(self.timetable, self.days, self.time_slots)
        self.setCentralWidget(self.timetable_view)

        self.generate_pdf(self.timetable)

    def generate_pdf(self, timetable):
        """Generate PDF of the timetable."""
        c = canvas.Canvas("timetable.pdf", pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 50, "Generated Timetable")

        y_position = height - 100
        for day in self.days:
            c.setFont("Helvetica-Bold", 14)
            c.drawString(100, y_position, f"{day}:")
            y_position -= 20

            day_entries = [entry for entry in timetable if entry["day"] == day]

            c.setFont("Helvetica", 10)
            for entry in day_entries:
                line = f"Period {entry['period']}: {entry['subject']} - {entry['teacher']} ({entry['time_slot']})"
                c.drawString(100, y_position, line)
                y_position -= 20

            y_position -= 20 

        c.save()
        self.statusBar().showMessage("PDF generated successfully!")

class TeacherForm(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Add Teachers")

        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.subject_input = QLineEdit()

        layout.addRow("Teacher Name:", self.name_input)
        layout.addRow("Subject:", self.subject_input)

        self.submit_button = QPushButton("Add Teacher")
        self.submit_button.clicked.connect(self.add_teacher)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def add_teacher(self):
        name = self.name_input.text()
        subject = self.subject_input.text()
        if name and subject:
            self.parent.teachers.append({"name": name, "subject": subject})
            self.parent.statusBar().showMessage(f"Added teacher: {name} (Subject: {subject})")
            self.parent.init_dashboard()
        else:
            self.parent.statusBar().showMessage("Please fill all fields!")

class ClassForm(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Add Classes")

        layout = QFormLayout()

        self.class_name_input = QLineEdit()
        self.subject_input = QLineEdit()
        self.periods_input = QLineEdit()

        layout.addRow("Class Name:", self.class_name_input)
        layout.addRow("Subject:", self.subject_input)
        layout.addRow("Periods:", self.periods_input)

        self.submit_button = QPushButton("Add Class")
        self.submit_button.clicked.connect(self.add_class)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def add_class(self):
        class_name = self.class_name_input.text()
        subject = self.subject_input.text()
        try:
            periods = int(self.periods_input.text())
            if class_name and subject and periods > 0:
                self.parent.classes.append({
                    "class_name": class_name,
                    "subject": subject,
                    "periods": periods
                })
                self.parent.statusBar().showMessage(f"Added class: {class_name} (Subject: {subject}, Periods: {periods})")
                self.parent.init_dashboard()
            else:
                self.parent.statusBar().showMessage("Please fill all fields with valid data!")
        except ValueError:
            self.parent.statusBar().showMessage("Periods must be a number!")

class TimetableView(QWidget):
    def __init__(self, timetable, days, time_slots):
        super().__init__()
        self.setWindowTitle("Timetable View")
        self.days = days
        self.time_slots = time_slots
        layout = QVBoxLayout()

        if timetable:
            timetable_by_day = {day: [] for day in self.days}

            for entry in timetable:
                timetable_by_day[entry["day"]].append(entry)

            for day, entries in timetable_by_day.items():
                day_label = QLabel(f"{day}")
                day_label.setStyleSheet("font-weight: bold; font-size: 16px;")
                layout.addWidget(day_label)

                table = QTableWidget()
                table.setRowCount(len(entries))
                table.setColumnCount(5)
                table.setHorizontalHeaderLabels(["Class", "Period", "Time Slot", "Subject", "Teacher"])

                for row_idx, entry in enumerate(entries):
                    table.setItem(row_idx, 0, QTableWidgetItem(entry["class"]))
                    table.setItem(row_idx, 1, QTableWidgetItem(f"Period {entry['period']}"))
                    table.setItem(row_idx, 2, QTableWidgetItem(entry["time_slot"]))
                    table.setItem(row_idx, 3, QTableWidgetItem(entry["subject"]))
                    table.setItem(row_idx, 4, QTableWidgetItem(entry["teacher"]))

                layout.addWidget(table)
        else:
            layout.addWidget(QLabel("No timetable generated yet!"))

        self.setLayout(layout)

    def time_slot_index(self, time_slot):
        """Return the index of the time slot in the predefined order."""
        return self.time_slots.index(time_slot)


if __name__ == "__main__":
    app = QApplication([])
    window = TimetableApp()
    window.show()
    app.exec()