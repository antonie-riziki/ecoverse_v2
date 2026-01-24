from django.shortcuts import render
import google.generativeai as genai
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import os
import sys
import json
import africastalking


load_dotenv()

sys.path.insert(1, './bizwave_app')

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

africastalking.initialize(
    username="EMID",
    api_key=os.getenv("AT_API_KEY")
)


def get_gemini_response(prompt):

    model = genai.GenerativeModel("gemini-2.5-flash", 

        system_instruction = f"""
        
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

        """

        )


    response = model.generate_content(
        prompt,
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=1.5, 
      )
    
    )


    
    return response.text



# Create your views here.
def home(request):
    return render(request, 'index.html')


def registration(request):
    return render(request, 'registration.html')


def signin(request):
    return render(request, 'signin.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def settings(request):
    return render(request, 'settings.html')


def rewards(request):
    return render(request, 'rewards.html')


def impact(request):
    return render(request, 'impact.html')


def analytics(request):
    return render(request, 'analytics.html')


def nearby(request):
    return render(request, 'nearby.html')


def community(request):
    return render(request, 'community.html')



@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        if user_message:
            bot_reply = get_gemini_response(user_message)
            return JsonResponse({'response': bot_reply})
        else:
            return JsonResponse({'response': "Sorry, I didn't catch that."}, status=400)

