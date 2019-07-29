from django.conf import settings
from django.shortcuts import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from api.helix import Twitch
from api.alexa import alexa_resp
import json
import logging

logger = logging.getLogger('app')
config = settings.CONFIG


@require_http_methods(["GET"])
def api_home(request):
    log_req(request)
    return HttpResponse('API Online')


@csrf_exempt
@require_http_methods(["POST"])
def alexa_post(request):
    log_req(request)
    try:
        body = request.body.decode('utf-8')
        event = json.loads(body)
        logger.debug(event)
        intent = event['request']['intent']['name']
        if intent == 'NextLevel':
            return get_next_level(event)
        elif intent == 'RandomLevel':
            return get_random_level(event)
        elif intent == 'SkipLevel':
            return skip_current_level(event)
        elif intent == 'UndoLevel':
            return undo_next_level(event)
        elif intent == 'OpenQueue':
            return open_maker_queue(event)
        elif intent == 'CloseQueue':
            return close_maker_queue(event)
        elif intent == 'ClearChat':
            return clear_chat(event)
        # elif intent == 'SendChat':
        #     return send_chat(event)
        # elif intent == 'ChatStatus':
        #     return chat_status(event)
        # elif intent == 'GetTitle':
        #     return get_title(event)
        # elif intent == 'UpdateTitle':
        #     return update_title(event)
        # elif intent == 'GetFollows':
        #     return get_follows(event)
        # elif intent == 'GetGame':
        #     return get_game(event)
        else:
            raise ValueError('Unknown Intent')
    except Exception as error:
        logger.exception(error)
        return alexa_resp('Error. {}'.format(error), 'Error')


def get_next_level(event):
    logger.debug('NextLevel')
    twitch = Twitch(event['session']['user']['accessToken'])
    twitch.send_irc_msg('!next')
    return alexa_resp('Done.', 'Get Next Level')


def get_random_level(event):
    logger.debug('RandomLevel')
    twitch = Twitch(event['session']['user']['accessToken'])
    twitch.send_irc_msg('!random')
    return alexa_resp('Done.', 'Get Random Level')


def skip_current_level(event):
    logger.debug('SkipLevel')
    twitch = Twitch(event['session']['user']['accessToken'])
    twitch.send_irc_msg('!skip')
    return alexa_resp('I skipped the current level.', 'Skip Current Level')


def undo_next_level(event):
    logger.debug('UndoLevel')
    twitch = Twitch(event['session']['user']['accessToken'])
    twitch.send_irc_msg('!undo')
    return alexa_resp('I reverted the last level.', 'Undo Next Level')


def open_maker_queue(event):
    logger.debug('OpenQueue')
    twitch = Twitch(event['session']['user']['accessToken'])
    twitch.send_irc_msg('!open')
    return alexa_resp('The queue is now open.', 'Open Maker Queue')


def close_maker_queue(event):
    logger.debug('CloseQueue')
    twitch = Twitch(event['session']['user']['accessToken'])
    twitch.send_irc_msg('!close')
    return alexa_resp('The queue is now closed.', 'Close Maker Queue')


def clear_chat(event):
    logger.debug('ClearChat')
    twitch = Twitch(event['session']['user']['accessToken'])
    twitch.send_irc_msg('/clear')
    return alexa_resp('Chat has been cleared.', 'Clear Chat')


def send_chat(event):
    logger.debug('SendChat')
    message = event['request']['intent']['slots']['message']['value']
    logger.debug('message:raw: {}'.format(message))
    message = message.lstrip('chat').strip()
    message = message.lstrip('to').strip()
    message = message.lstrip('say').strip()
    message = message.lstrip('i said').strip()
    logger.debug('message:stripped: {}'.format(message))
    twitch = Twitch(event['session']['user']['accessToken'])
    twitch.send_irc_msg(message)
    return alexa_resp('Message sent.', 'Send Chat Message')


def chat_status(event):
    logger.debug('ChatStatus')
    status = event['request']['intent']['slots']['status']['value']
    mode = event['request']['intent']['slots']['mode']['value']
    logger.debug('status: {}'.format(status))
    logger.debug('mode: {}'.format(mode))

    if 'emote' in mode:
        chat_mode = 'emoteonly'
    elif 'nine' in mode:
        chat_mode = 'r9kbeta'
    elif 'slow' in mode:
        chat_mode = 'slow'
    elif 'follower' in mode:
        chat_mode = 'followers'
    elif 'sub' in mode:
        chat_mode = 'subscribers'
    else:
        speech = 'Unknown chat mode. {}'.format(mode)
        return alexa_resp(speech, 'Unknown Chat Mode')

    twitch = Twitch(event['session']['user']['accessToken'])
    if status == 'on' or status == 'enable':
        twitch.set_chat_mode(chat_mode, True)
        speech = '{} mode turned on.'.format(mode)
        return alexa_resp(speech, 'Chat Mode')
    elif staticmethod == 'off' or status == 'disable':
        twitch.set_chat_mode(chat_mode, False)
        speech = '{} mode turned off.'.format(mode)
        return alexa_resp(speech, 'Chat Mode')
    else:
        speech = 'I was unsure if you wanted to turn the mode on or off.'
        return alexa_resp(speech, 'Unknown Action')


def get_title(event):
    logger.debug('GetTitle')
    twitch = Twitch(event['session']['user']['accessToken'])
    channel = twitch.get_channel()
    logger.debug(channel)
    title = channel['status']
    logger.debug('title: {}'.format(title))
    speech = 'Your current title is. {}'.format(title)
    return alexa_resp(speech, 'Current Title')


def update_title(event):
    logger.debug('UpdateTitle')
    title = event['request']['intent']['slots']['title']['value']
    title = title.title()
    logger.debug('title: {}'.format(title))
    twitch = Twitch(event['session']['user']['accessToken'])
    update = twitch.update_channel(title)
    logger.debug(update)
    speech = 'Your title has been updated too. {}'.format(title)
    return alexa_resp(speech, 'Update Title')


def get_follows(event):
    logger.debug('GetFollows')
    twitch = Twitch(event['session']['user']['accessToken'])
    channel = twitch.get_channel()
    logger.debug('channel:followers: {}'.format(channel['followers']))
    speech = 'You currently have {} followers.'.format(channel['followers'])
    return alexa_resp(speech, 'Followers')


def get_game(event):
    logger.debug('GetGame')
    twitch = Twitch(event['session']['user']['accessToken'])
    channel = twitch.get_channel()
    logger.debug('channel:game: {}'.format(channel['game']))
    speech = 'You are currently playing. {}'.format(channel['game'])
    return alexa_resp(speech, 'Game')


def log_req(request):
    """
    DEBUGGING ONLY
    """
    data = None
    if request.method == 'GET':
        data = 'GET: '
        for key, value in request.GET.items():
            data += '"%s": "%s", ' % (key, value)
    if request.method == 'POST':
        data = 'POST: '
        for key, value in request.POST.items():
            data += '"%s": "%s", ' % (key, value)
    if data:
        data = data.strip(', ')
        logger.debug(data)
        json_string = '{%s}' % data
        return json_string
    else:
        return None
