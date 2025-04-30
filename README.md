# 🗓️ Dynamic Timetable Generator

The **Dynamic Timetable Generator** is a Python-based desktop application designed to help educational institutions easily create and manage weekly class schedules. Built with **PyQt5** for the user interface and **ReportLab** for PDF export, this tool provides a user-friendly and efficient way to automate timetable creation without relying on spreadsheets or manual work.

The application allows users to add teachers, assign subjects to them, and input classes along with the number of periods each subject needs in a week. Once this information is entered, the system uses a randomized scheduling algorithm to generate a timetable that assigns teachers to classes and time slots in a balanced way across the week (Monday to Friday).

The generated timetable is displayed in an organized, day-wise view within the app using PyQt's table widgets. Each day's schedule shows class name, subject, teacher, time slot, and period number. This clear and structured view makes it easy for users to verify the distribution of periods and teacher assignments.

In addition to on-screen display, the app also automatically generates a **PDF version** of the timetable. The exported PDF groups entries by weekday and includes formatted details for printing or sharing. This feature is especially helpful for administrators or coordinators who need to distribute timetables physically or via email.

This version of the timetable generator is ideal for small to medium-sized institutions looking for a quick, offline, and easy-to-use scheduling tool. While the current logic is based on random assignment, the system ensures there are no overlapping periods within a day. It can be further enhanced by integrating constraint-based scheduling techniques, database storage, or user authentication.

## Key Features
- Add teachers and subjects
- Add classes with required periods
- Automatically generate non-conflicting weekly timetable
- View and verify the schedule within the app
- Export timetable to a structured PDF file
- Simple, clean, and intuitive UI using PyQt5

This project is a great foundation for learning GUI development, basic scheduling algorithms, and PDF automation in Python.
