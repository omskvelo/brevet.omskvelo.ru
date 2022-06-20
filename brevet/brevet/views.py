from django.shortcuts import render

# --- Static pages ---
def faq(request):
    return render(request, "faq.html")

def calc(request):
    return render(request, "calc.html")