def read_marks(filename):
    students = {}
    try:
        with open(filename, 'r') as file:
            for line_no, line in enumerate(file, start=1):
                try:
                    student_id, name, subject, marks = line.strip().split(',')
                    student_id = int(student_id)
                    marks = int(marks)
                except ValueError:
                    print(f"Skipping  line {line_no}: {line.strip()}")
                    continue  

                if student_id not in students:
                    students[student_id] = {
                        "name": name,
                        "subjects": {}
                    }

                students[student_id]["subjects"][subject] = marks

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return {}

    return students


def generate_report(students):
    report_data = []

    for student_id, data in students.items():
        subjects = data["subjects"]
        total_marks = sum(subjects.values())
        avg_marks = total_marks / len(subjects)
        highest_subject = max(subjects, key=subjects.get)
        lowest_subject = min(subjects, key=subjects.get)

        report_data.append({
            "student_id": student_id,
            "name": data["name"],
            "total": total_marks,
            "average": avg_marks,
            "highest": (highest_subject, subjects[highest_subject]),
            "lowest": (lowest_subject, subjects[lowest_subject])
        })

    report_data.sort(key=lambda x: x["average"], reverse=True)
    return report_data


def write_summary(report_data, filename):
    with open(filename, 'w') as file:
        for student in report_data:
            file.write(f"Student ID: {student['student_id']}\n")
            file.write(f"Name: {student['name']}\n")
            file.write(f"Total Marks: {student['total']}\n")
            file.write(f"Average Marks: {student['average']:.2f}\n")
            file.write(f"Highest Scored Subject: {student['highest'][0]} ({student['highest'][1]})\n")
            file.write(f"Lowest Scored Subject: {student['lowest'][0]} ({student['lowest'][1]})\n")
            file.write("\n")


def main():
    input_file = "Student_Data.txt"
    output_file = "report.txt"

    students = read_marks(input_file)
    if not students:
        print("No valid data to process.")
        return

    report_data = generate_report(students)
    write_summary(report_data, output_file)

    print(f"Report generated successfully in '{output_file}'.")


