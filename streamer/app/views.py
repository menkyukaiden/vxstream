import json
from logging import getLogger
from time import sleep

from celery import task, current_task
from celery.result import AsyncResult
# from django.http import HttpResponse
from configobj import ConfigObj
from django import template
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from app.forms import InterfaceConfigurationForm
from app.models import Transponders
from .utils.generic import GenericUtils

logger = getLogger(__name__)

register = template.Library()


# page: index
def index(request):
    """

    :param request:
    :return: HttpResponse
    """
    context = {}
    template = loader.get_template('app/home.html')
    return HttpResponse(template.render(context, request))

# all html templates (for dev)
def all_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))


# page: channels
@login_required(login_url="login/")
def channels(request):
    freq_list = []
    obj = ConfigObj("app/utils/astra.conf")
    dict = {}
    i = 0
    for key, value in obj.items():
        try:
            # affectation of audiopid only to raise exception
            audiopid = (value['AUDIO_PID'])

            # Add the name of the channel
            value.update({'NAME': key})

            # Get the list of frequencies
            freq_list.append(value['FREQUENCY'])

            dict[i] = i
            dict[i] = value
            i += 1
        except:
            pass
    # Sort and remove duplicates
        freq_list = sorted(list(set(freq_list)))

    #print (dict)

    context = {
        'title': 'Channels list',
        'channels': dict,
        'frequencies': freq_list
    }
    template = loader.get_template('app/channels.html')
    return HttpResponse(template.render(context, request))


# page: transponders
@login_required(login_url="login/")
def transponders(request):
    """

    :param request:
    :return: HttpResponse
    """
    context = {
        'transponders': Transponders.objects.all(),
    }
    template = loader.get_template('app/transponders.html')
    return HttpResponse(template.render(context, request))


def error_404(request):
    """
    error_404
    :param request:
    :return: HttpResponse
    """
    context = {}
    template = loader.get_template('app/page_404.html')
    return HttpResponse(template.render(context, request))


# page: profile
@login_required(login_url="login/")
def profile(request):
    """

    :param request:
    :return:
    """
    context = {}
    template = loader.get_template('app/profile.html')
    return HttpResponse(template.render(context, request))



@task()
def do_work():
    """ Get some rest, asynchronously, and update the state all the time """
    for i in range(100):
        sleep(0.1)
        current_task.update_state(state='PROGRESS',
            meta={'current': i, 'total': 100})


def poll_state(request):
    """ A view to report the progress to the user """
    if 'job' in request.GET:
        job_id = request.GET['job']
    else:
        return HttpResponse('No job id given.')

    job = AsyncResult(job_id)
    data = job.result or job.state
    return HttpResponse(json.dumps(data), content_type='application/json')


def init_work(request):
    """ A view to start a background job and redirect to the status page """
    job = do_work.delay()
    return HttpResponseRedirect(reverse('poll_state') + '?job=' + job.id)

@login_required(login_url="login/")
def transponders_ajax(request):
    """

    :param request:
    :return: HttpResponse
    """
    if request.method == 'POST':
        if request.is_ajax():
            data = request.POST['mydata']
            if data == "update":
                # get the list from /usr/share/dvb/dvb-s
                gen = GenericUtils()
                transpon_from_files = gen.transponder_list()

                # Delete all entries in the db
                cursor = connection.cursor()
                cursor.execute("TRUNCATE TABLE `app_transponders`")

                # Populate the table with all file names and file content
                for tr in transpon_from_files:
                    Transponders(name=tr, config=gen.read_sat_config(tr)).save()
            elif data == "delete":
                transponder_name = request.POST['element']
                # Delete
                #print(transponder_name)
                Transponders.objects.filter(name=transponder_name).delete()
            return HttpResponse(data)
    return render(request)

@login_required(login_url="login/")
def post_config_ajax(request):
    """

    :param request:
    :return: HttpResponse
    """
    if request.method == 'POST':
        if request.is_ajax():
            data = request.POST['config']
            print(data)

        return HttpResponse(data)
    else:
        context = {}
        tmp = loader.get_template('app/page_404.html')
        return HttpResponse(tmp.render(context, request))

# page: interfaces
@login_required(login_url="login/")
def interfaces(request):
    """

    :param request:
    :return: HttpResponse
    """
    form = InterfaceConfigurationForm()
    context = {
        'transponders': Transponders.objects.all(),
        'form': form
    }
    template = loader.get_template('app/interfaces.html')
    return HttpResponse(template.render(context, request))