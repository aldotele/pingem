from django.shortcuts import render
from ping.ping_pack.ping_data import Ping
from .forms import UrlForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView
from .models import Url
from django.urls import reverse


def home(request):
    context = dict()
    context['form'] = UrlForm()
    return render(request, "index.html", context)


def ping(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UrlForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            context = {}
            url = form.cleaned_data['url']
            regexp = form.cleaned_data['regexp']
            context['url'] = form.cleaned_data['url']
            context['regexp'] = regexp
            try:
                current_ping = Ping(url)
                status_code, response_time, resp_content = current_ping.get_ping_data()
                is_matching, matching_details = Ping.is_regexp_matching(regexp, resp_content)
                Ping.save_ping_data(url, status_code, response_time, regexp, is_matching, matching_details)
            except ConnectionError:
                status_code, response_time, is_matching = "N/A", "N/A", "N/A"

            context = {"url": url, "status_code": status_code, "response_time": response_time, "match": is_matching}
            return render(request, 'ping-data.html', context)
    else:
        return HttpResponseRedirect(reverse('home'))


# def ping_old(request):
#     # context = {}
#     # url = request.POST.get('url', '')
#     # ping = Ping(url)
#     # status_code = ping.get_status_code()
#     # response_time = ping.get_response_time()
#     # context['url'] = url
#     # context['status_code'] = status_code
#     # context['response_time'] = response_time
#     # return render(request, 'result.html', context)


# class UrlCreateView(CreateView):
#     model = Url
#     fields = ['link']
#     template_name = 'index.html'
#     #success_url = reverse_lazy('show')