class Language:
    C = 'c'
    CPP = 'cpp'
    JAVA = 'java'
    PYTHON = 'python'
    GO = 'go'

    LANGUAGE_CHOICES = (
        (C, "C (GCC 9.3.0)"),
        (CPP, "C++ (G++ 9.3.0)"),
        (JAVA, "Java (OpenJDK 14.0.1)"),
        (PYTHON, "Python (Python 3.8.2)"),
        (GO, 'Go (Golang 1.13.8)')
    )


class Verdict:
    PENDING = 'P'
    RUNNING = 'R'
    ACCEPTED = 'AC'
    PRESENTATION_ERROR = 'PE'
    TIME_LIMIT_EXCEEDED = 'TLE'
    MEMORY_LIMIT_EXCEEDED = 'MLE'
    WRONG_ANSWER = 'WA'
    RUNTIME_ERROR = 'RE'
    OUTPUT_LIMIT_EXCEEDED = 'OLE'
    COMPILE_ERROR = 'CE'
    SYSTEM_ERROR = 'SE'
    VERDICT_CHOICES = (
        (PENDING, 'Pending'),
        (RUNNING, 'Running'),
        (ACCEPTED, 'Accepted'),
        (PRESENTATION_ERROR, 'Presentation Error'),
        (TIME_LIMIT_EXCEEDED, 'Time Limit Exceeded'),
        (MEMORY_LIMIT_EXCEEDED, 'Memory Limit Exceeded'),
        (WRONG_ANSWER, 'Wrong Answer'),
        (RUNTIME_ERROR, 'Runtime Error'),
        (OUTPUT_LIMIT_EXCEEDED, 'Output Limit Exceeded'),
        (COMPILE_ERROR, 'Compile Error'),
        (SYSTEM_ERROR, 'System Error'),
    )