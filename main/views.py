from django.shortcuts import render


def show_main(request):
    context = {
        "name": "Muhammad Eshan Bobby Bhaskara",
        "npm": "2506546333",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems student at Fasilkom UI with a growing "
            "interest in technology and its impact on society. Working "
            "collaboratively, thinking critically, and approaching problems "
            "with attention to detail."
        ),
    }
    return render(request, "index.html", context)
