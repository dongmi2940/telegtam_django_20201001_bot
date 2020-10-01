import json
import telegram

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Post
from .tasks import get_zum_realtime_keywords
from django.shortcuts import get_list_or_404, get_object_or_404, render, resolve_url


bot = telegram.Bot(token = settings.TELEGRAM_TOKEN)

def index(request):
    return HttpResponse("hello django")

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {"post": post,})


#외부에서 POST요청을 직접적으로 못받게 되어있다. 
@csrf_exempt
def webhook(request):
    json_string = request.body
    telegram_update = json.loads(json_string) #dict 

    received_text = telegram_update['message']['text']

    if received_text == '실검':
        keyword_list = get_zum_realtime_keywords() #list => str
        # 1안:  django templete 엔진을 활용해서 문자열 생성 
        # 2안: 
        text = '\n'.join(keyword_list)
    elif received_text == '내역':
        text = ''
        for post in Post.objects.all():
            post_url = request.build_absolute_uri(resolve_url(post))
            text += f"""{post.title}
{post_url}          
            """
    else : 
        text = "ECHO) " + received_text 

    chat_id = telegram_update['message']['chat']['id'] #가장 최근에 온 메시지의 chat id를 가져옵니다
    bot.sendMessage(chat_id=chat_id, text=text)

    return HttpResponse("ok")
