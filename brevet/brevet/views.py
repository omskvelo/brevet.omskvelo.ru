from django.shortcuts import render

# --- Static pages ---
def faq(request):
    return render(request, "faq.html")