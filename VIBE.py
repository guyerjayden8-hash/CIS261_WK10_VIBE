#Jamie Guyer
#CSI261
#WK10 VIBE Coding 

from dataclasses import dataclass

FILE_NAME = "student_grades.txt"


def calculate_average(test_1: float, test_2: float, test_3: float) -> float:
    return (test_1 + test_2 + test_3) / 3


def calculate_grade(average: float) -> str:
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


@dataclass
class Student:
    """Represent one student's scores and calculated results."""

    name: str
    student_id: str
    test1: float
    test2: float
    test3: float
    average: float
    grade: str

    @classmethod
    def from_scores(
        cls, name: str, student_id: str, test1: float, test2: float, test3: float
    ) -> "Student":
        average = calculate_average(test1, test2, test3)
        return cls(name, student_id, test1, test2, test3, average, calculate_grade(average))

    def to_dictionary(self) -> dict:
        return {
            "name": self.name,
            "id": self.student_id,
            "test1": self.test1,
            "test2": self.test2,
            "test3": self.test3,
            "average": self.average,
            "grade": self.grade,
        }


def get_score(test_name: str) -> float:
	"""Get a test score from 0 through 100."""
	while True:
		try:
			score = float(input(f"{test_name} score (0-100): "))
		except ValueError:
			print("Please enter a number.")
			continue

		if 0 <= score <= 100:
			return score
		print("Score must be between 0 and 100.")


def add_student() -> dict:
    name = input("Student name: ").strip()
    student_id = input("Student ID: ").strip()
    test_1 = get_score("Test 1")
    test_2 = get_score("Test 2")
    test_3 = get_score("Test 3")
    student = Student.from_scores(name, student_id, test_1, test_2, test_3)
    return student.to_dictionary()


def display_records(records: list[dict]) -> None:
    if not records:
        print("No student records to display.")
        return

    print("\nStudent Grade Report")
    print("-" * 72)
    print(f"{'Name':<20}{'Student ID':<15}{'Test 1':>8}{'Test 2':>8}{'Test 3':>8}{'Average':>10}{'Grade':>7}")
    print("-" * 72)
    for record in records:
        print(
            f"{record['name']:<20}{record['id']:<15}"
            f"{record['test1']:>8.2f}{record['test2']:>8.2f}{record['test3']:>8.2f}"
            f"{record['average']:>10.2f}{record['grade']:>7}"
        )
    print("-" * 72)


def display_statistics(records: list[dict]) -> None:
    if not records:
        print("No student records available for statistics.")
        return

    averages = [record["average"] for record in records]
    print("\nClass Statistics")
    print(f"Highest average: {max(averages):.2f}")
    print(f"Lowest average: {min(averages):.2f}")
    print(f"Class average: {sum(averages) / len(averages):.2f}")


def search_students(records: list[dict]) -> None:
    search_name = input("Enter a student name to search: ").strip().lower()
    matches = [record for record in records if search_name in record["name"].lower()]
    if matches:
        display_records(matches)
    else:
        print("No students found with that name.")


def save_records(records: list[dict]) -> bool:
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            for record in records:
                file.write(
                    f"{record['name']}|{record['id']}|{record['test1']:.2f}|"
                    f"{record['test2']:.2f}|{record['test3']:.2f}|"
                    f"{record['average']:.2f}|{record['grade']}\n"
                )
    except OSError as error:
        print(f"Could not save records: {error}")
        return False
    return True


def load_records() -> list[dict]:
    records: list[dict] = []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                fields = line.rstrip("\n").split("|")
                if len(fields) != 7:
                    print(f"Skipping invalid record on line {line_number}.")
                    continue
                try:
                    test_1, test_2, test_3 = map(float, fields[2:5])
                    student = Student.from_scores(
                        fields[0], fields[1], test_1, test_2, test_3
                    )
                    records.append(student.to_dictionary())
                except ValueError:
                    print(f"Skipping invalid record on line {line_number}.")
    except FileNotFoundError:
        return records
    except OSError as error:
        print(f"Could not load records: {error}")
    return records


def main() -> None:
    records = load_records()
    if records:
        print(f"Loaded {len(records)} student record(s) from {FILE_NAME}.")

    while True:
        print("\nStudent Grade Calculator")
        print("1. Add student record")
        print("2. Display grade report")
        print("3. Display class statistics")
        print("4. Search for a student")
        print("5. Save and Exit")
        choice = input("Select an option (1-5) or press ESC to exit: ").strip()

        if choice == "1":
            records.append(add_student())
            save_records(records)
            print("Student record added.")
        elif choice == "2":
            display_records(records)
        elif choice == "3":
            display_statistics(records)
        elif choice == "4":
            search_students(records)
        elif choice in ("5", "\x1b"):
            save_records(records)
            print("Goodbye.")
            break
        else:
            print("Please select an option from 1-5 or press ESC to exit.")


if __name__ == "__main__":
	main()
