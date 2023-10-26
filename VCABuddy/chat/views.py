from rest_framework.response import Response
from rest_framework.decorators import api_view
from chat.models import ChatMessage
from authentication.models import CustomUser
from chat.chat_bot import Chatbot, text_to_audio

chatbot = Chatbot("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")

@api_view(['POST', 'GET'])
def voice_input(request):
    user1 = CustomUser.objects.get(email='admin@g.com')

    if request.method == "POST":
        message = request.data.get("message")
        input_type = request.data.get("input_type")
        language = request.data.get("language")

        # Pass the text message to the chatbot and get a text response
        text_response = chatbot.get_response(message, language, input_type)

        chat_message = ChatMessage.objects.create(user=user1, message=message, response=text_response)
        chat_message.save()
        return Response({"text_response": text_response})

    elif request.method == "GET":
        messages = ChatMessage.objects.filter(user=user1).values()  # Convert QuerySet to a list of dictionaries
        return Response(list(messages))

    else:
        return Response({"error": "Invalid request method."})
    
@api_view(['POST'])
def text_to_voice(request):
    if request.method == "POST":
        message = request.data.get("message")
        text_to_audio(message)
        return Response({"hhh": "working"})

        