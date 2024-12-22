from django.shortcuts import render
from django.http import JsonResponse
import requests
import json

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta2/models/gemini-1.5-flash:generateText"
GEMINI_API_KEY = "AIzaSyAMTzxbPfDI_EGbeJsElj9NNFKeRyC-HHA"

def chatbot_view(request):
    return render(request, "chatbot.html")  # Render the chatbot frontend

def chatbot(request):
    if request.method == "POST":
        try:
            # Parse the JSON payload from the request
            body = json.loads(request.body)
            user_message = body.get("message", "").strip()

            if not user_message:
                return JsonResponse({"response": "Message cannot be empty."}, status=400)

            # Prepare the payload for the Gemini API
            payload = {
                "instances": [
                    {
                        "text": user_message
                    }
                ],
                "parameters": {
                    "temperature": 0.7,
                    "maxOutputTokens": 100
                }
            }
            params = {"key": GEMINI_API_KEY}

            # Make the API request
            response = requests.post(GEMINI_API_URL, params=params, json=payload)
            response_data = response.json()

            if response.status_code == 200:
                # Extract the response from the Gemini API
                candidates = response_data.get("predictions", [])
                bot_response = candidates[0]["content"] if candidates else "I couldn't understand that."
            else:
                bot_response = response_data.get("error", {}).get("message", "Error communicating with the Gemini API.")

            return JsonResponse({"response": bot_response})

        except json.JSONDecodeError:
            return JsonResponse({"response": "Invalid JSON in the request body."}, status=400)
        except Exception as e:
            return JsonResponse({"response": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"response": "Invalid request method."}, status=405)