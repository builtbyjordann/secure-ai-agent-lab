#determine what document to use based on the question

def choose_document(question):
    question = question.lower()

    if "vacation" in question:
        return "vacation.txt"

    if "benefits" in question:
        return "benefits.txt"

    if "payroll" in question or "salary" in question:
        return "payroll.txt"

    return None

