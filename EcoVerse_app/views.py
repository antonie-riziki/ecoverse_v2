import africastalking
from django.shortcuts import render, redirect

# import google.generativeai as genai # deprecated version
from google import genai
from google.genai import types
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import os
import sys
import json
import requests


# from opik import configure
# from opik.integrations.genai import track_genai


# configure()


load_dotenv()

sys.path.insert(1, "./EcoVerse_app")


# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

africastalking.initialize(username="EMID", api_key=os.getenv("AT_API_KEY"))

response = requests.get('https://public-api-v2.bags.fm/api/v1/endpoint', 
  headers={'x-api-key': os.getenv("BAGS_API_KEY")})

sms = africastalking.SMS
airtime = africastalking.Airtime

"""

Opik Configuration for Gemini AI Model

"""

# os.environ["GEMINI_API_KEY"] = "your-api-key-here"

# opik_client = google.genai.Client()


# client = track_genai(client)


# def opik_gemini_agent(prompt: str):
#     response = client.models.generate_content(
#         model="gemini-2.0-flash-001", contents=prompt
#     )

#     return response.text


def get_opik_client(base_client):
    """
    Safely wraps the Gemini client with Opik if available.
    Never crashes the app.
    """
    try:
        from opik import configure
        from opik.integrations.genai import track_genai

        configure()
        return track_genai(base_client)

    except Exception as e:
        # Log locally, but never crash prod
        print("Opik disabled:", str(e))
        return base_client


def opik_gemini_agent(prompt: str):
    safe_client = get_opik_client(client)

    response = safe_client.models.generate_content(
        model="gemini-2.0-flash-001", contents=prompt
    )

    return response.text


def get_gemini_response(prompt):

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="""
                
                You are EcoVerse AI Assistant, an intelligent sustainability and green innovation expert designed to educate, guide, 
                and support users in topics related to energy transformation, waste management, and environmental conservation.

                Core Focus Areas:
                    - Your primary domains of expertise include:
                    - Waste-to-energy technologies (biogas, pyrolysis, gasification, anaerobic digestion)
                    - Renewable energy (solar, wind, hydro, geothermal, biomass)
                    - Solar energy systems (installation, maintenance, costs, ROI, off-grid vs on-grid)
                    - EV charging infrastructure (deployment, usage, benefits, network optimization)
                    - Energy storage (battery technologies, grid integration, optimization)
                    - Circular economy and waste recycling
                    - Smart energy grids and IoT in energy management
                    - Carbon credits, offset systems, and sustainability finance
                    - Environmental conservation (deforestation, water, biodiversity, waste reduction)
                    - ESG principles and climate change mitigation strategies
                    - Green policies and innovations in Africa (especially Kenya and East Africa)

            
                
                Capabilities:
                You should:
                    1. Explain complex sustainability topics clearly and accurately.

                    2. Provide actionable insights and data-driven recommendations.

                    3. Suggest policies, technologies, or startups working in the sector.

                    4. Offer localized examples and initiatives in Kenya and Africa.

                    5. Educate users on how they can contribute to environmental sustainability.

                    6. Guide innovators on integrating AI, IoT, and Data Science into green solutions.

                    7. Respond to both technical (engineers, developers) and non-technical (students, activists) audiences with suitable tone and depth.

                
                Tone & Style:

                - Use a professional, inspiring, and knowledgeable tone, Keep answers short for conversational response behaviors.
                - Avoid unnecessary jargon — explain technical terms simply when used.
                - Encourage eco-awareness, innovation, and collaboration.
                - Be data-informed, evidence-based, and globally aware while remaining locally relevant.

                
                Important:
                If the user’s question is outside the scope of energy, sustainability, or environmental technology, politely decline and redirect to related eco-innovation topics.

                Example Topics Users May Ask About:

                - “How can Kenya scale waste-to-energy projects?”

                - “What are the best EV charging companies in Africa?”

                - “How do carbon credits work for small communities?”

                - “What AI models are used for energy optimization?”

                - “How can households reduce energy waste?”

                """,
            max_output_tokens=1000,
            top_k=2,
            top_p=0.5,
            temperature=0.9,
            # response_mime_type= 'application/json',
            # stop_sequences= ['\n'],
            seed=42,
        ),
    )

    return response.text


def registration_message(phone_number):
    amount = "10"
    currency_code = "KES"

    airtime_rec = "+254" + str(phone_number)

    recipients = [f"+254{str(phone_number)}"]

    # Set your message
    message = (
        f"Welcome to EcoVerse, a platform for green innovation and sustainability!"
    )

    # Set your shortCode or senderId
    sender = 20384

    try:
        response = sms.send(message, recipients, sender)
        responses = airtime.send(
            phone_number=airtime_rec, amount=amount, currency_code=currency_code
        )

        print(response)
        print(responses)

    except Exception as e:
        print(f"Houston, we have a problem: {e}")


# Create your views here.
def home(request):
    return render(request, "index.html")


def registration(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        # Check if email already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        # Split full name
        name_parts = full_name.split(" ")
        first_name = name_parts[0]
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        user.save()

        registration_message(phone)
        messages.success(request, "Account created successfully")
        return redirect("signin")

    return render(request, "registration.html")


def signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            # login_message(user.phone_number)
            return redirect("/dashboard")
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "signin.html")


def dashboard(request):
    return render(request, "dashboard.html")


def settings(request):
    return render(request, "settings.html")


def rewards(request):
    return render(request, "rewards.html")


def impact(request):
    return render(request, "impact.html")


def analytics(request):
    return render(request, "analytics.html")


def nearby(request):
    return render(request, "nearby.html")


def community(request):
    return render(request, "community.html")


def ai_assistant(request):
    return render(request, "ai_assist.html")


@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        if user_message:
            bot_reply = get_gemini_response(user_message)
            opik_response = opik_gemini_agent(user_message)
            # print("Opik Gemini Response:", opik_response)
            return JsonResponse({"response": opik_response})
        else:
            return JsonResponse({"response": "Sorry, I didn't catch that."}, status=400)



@csrf_exempt
def launch_ecoverse_token(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    existing = EcoToken.objects.filter(is_launched=True).first()
    if existing:
        return JsonResponse({
            "message": "EcoVerse token already launched",
            "token_mint": existing.token_mint,
            "bags_url": existing.bags_url,
        })

    payload = {
        "name": "EcoVerse",
        "symbol": "ECO",
        "description": "Organic waste recycling reward token for EcoVerse.",
        "imageUrl": "https://your-domain.com/static/ecoverse-logo.png",
        "initialBuyLamports": 10000000,
    }

    response = requests.post(
        "http://localhost:8787/launch-token",
        json=payload,
        timeout=60,
    )

    data = response.json()

    if not data.get("success"):
        return JsonResponse(data, status=500)

    result = data["result"]

    token = EcoToken.objects.create(
        name=payload["name"],
        symbol=payload["symbol"],
        token_mint=result.get("tokenMint"),
        metadata_url=result.get("metadataUrl"),
        bags_url=f"https://bags.fm/{result.get('tokenMint')}",
        launch_signature=result.get("signature"),
        is_launched=True,
    )

    return JsonResponse({
        "message": "EcoVerse token launched successfully",
        "token_mint": token.token_mint,
        "bags_url": token.bags_url,
        "signature": token.launch_signature,
    })