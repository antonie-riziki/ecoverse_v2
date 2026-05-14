from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.home, name="home"),
    path('registration', views.registration, name="registration"),
    path('signin', views.signin, name="signin"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('settings', views.settings, name="settings"),
    path('analytics', views.analytics, name="analytics"),
    path('impact', views.impact, name="impact"),
    path('rewards', views.rewards, name="reward"),
    path('nearby', views.nearby, name="nearby"),
    path('community', views.community, name="community"),
    path('ai-assistant', views.ai_assistant, name="ai_assistant"),
    path('chatbot-response/', views.chatbot_response, name='chatbot_response'),

    path("api/bags/launch-token/", views.launch_ecoverse_token, name="launch_ecoverse_token"),
    path("api/bags/health/", views.bags_health, name="bags_health"),
    path("api/recycling/verify/", views.verify_recycling_submission, name="verify_recycling_submission"),
    path("api/recycling/<int:submission_id>/send-reward/", views.send_recycling_reward, name="send_recycling_reward"),





    
]