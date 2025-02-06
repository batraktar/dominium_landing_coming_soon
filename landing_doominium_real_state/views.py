import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

TELEGRAM_TOKEN = "7639849573:AAFfoDuLlhgDj0wuOw6qzEfFHl6pLTnE8ik"
CHAT_IDS = [396360105]  # Список ID


@csrf_exempt
def consultation_view(request):
    if request.method == "POST":
        name = request.POST.get("name", "Не вказано")
        phone = request.POST.get("phone", "Не вказано")
        subject = request.POST.get("subject", "Не вказано")
        message = request.POST.get("message", "Не вказано")

        text = f"""
📩 *Нова заявка на консультацію*  
👤 *Ім'я:* {name}  
📞 *Телефон:* {phone}  
📌 *Тема:* {subject}  
📝 *Повідомлення:* {message}  
        """

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        errors = []

        for chat_id in CHAT_IDS:
            payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                errors.append({"chat_id": chat_id, "error": response.text})

        if errors:
            return JsonResponse({"status": "error", "details": errors}, status=500)

        return JsonResponse({"status": "ok"}, status=200)

    return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)


def index(request):
    return render(request, 'base.html')


def custom_404(request, exception):
    return render(request, "404.html", status=404)
