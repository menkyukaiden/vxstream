import json
from logging import getLogger
from time import sleep

from celery import task, current_task
from celery.result import AsyncResult
from configobj import ConfigObj
from django import template
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from app.forms import InterfaceConfigurationForm
from app.models import Satellites, InterfaceProperties
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
def sats(request):
    """

    :param request:
    :return: HttpResponse
    """
    context = {
        'sats': Satellites.objects.all(),
    }
    template = loader.get_template('app/satellites.html')
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
def sats_ajax(request):
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
                transpon_from_files = gen.sats_list()

                # Delete all entries in the db
                cursor = connection.cursor()
                cursor.execute("TRUNCATE TABLE `app_satellites`")

                # Populate the table with all file names and file content
                for tr in transpon_from_files:
                    Satellites(name=tr, config=gen.read_sat_config(tr)).save()
                    print(tr)
            elif data == "delete":
                transponder_name = request.POST['element']
                # Delete
                #print(transponder_name)
                Satellites.objects.filter(name=transponder_name).delete()
            return HttpResponse(data)
    return render(request)


@login_required(login_url="login/")
def post_config_ajax(request):
    """
    post_config_ajax
    :param request:
    :return: HttpResponse
    """
    if request.method == 'POST':
        if request.is_ajax():
            interfacenum = request.POST['interfacenum']
            satselect = request.POST['satellitesselect']
            satcustom = request.POST['satellitesinput']
            si = request.POST['satellitesinput']
            dss = request.POST['deliverysystemselect']
            fi = request.POST['frequencyinput']
            symi = request.POST['symrateinput']
            pol = request.POST['polarizationselect']
            mod = request.POST['modulationselect']
            fec = request.POST['fecselect']
            rol = request.POST['rolloffselect']
            pilot = request.POST['pilotselect']
            lnbtype = request.POST['lnbtypeselect']
            lnblofstd = request.POST['lnblofstandardinput']
            lnblof = request.POST['lnblofinput']
            lnbloflow = request.POST['lnbloflowinput']
            lnblofhigh = request.POST['lnblofhighinput']

            if satselect == "default":
                # Custom sat
                print(satcustom)
            else:
                # Preset sat
                print(satselect)
            print("from:" + interfacenum)
        return HttpResponse(request)
    else:
        context = {}
        tpl = loader.get_template('app/page_404.html')
        return HttpResponse(tpl.render(context, request))


# page: interfaces
@login_required(login_url="login/")
def interfaces(request):
    """

    :param request:
    :return: HttpResponse
    """
    form = InterfaceConfigurationForm()
    #print(form.fields)
    dvb_int = InterfaceProperties.objects.all()
    satellites = Satellites.objects.all()
    context = {
        'satellites': satellites,
        'form': form,
        'dvb_int': dvb_int,
    }
    tpl = loader.get_template('app/interfaces.html')
    return HttpResponse(tpl.render(context, request))
