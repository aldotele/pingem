from django.shortcuts import render
from ping.ping_pack.ping_data import Ping
from .forms import UrlForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def home(request):
    context = dict()
    context['form'] = UrlForm()
    return render(request, "index.html", context)


def ping(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UrlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            regexp = form.cleaned_data['regexp']
            try:  # attempting to connect to Url
                current_ping = Ping(url)
                status_code, response_time, resp_content = current_ping.get_ping_data()
                is_matching, matching_details = Ping.is_regexp_matching(regexp, resp_content)
                Ping.save_ping_data(url, status_code, response_time, regexp, is_matching, matching_details)
            except ConnectionError:  # return "N/A" in case attempt not being successful
                status_code, response_time, is_matching = "N/A", "N/A", "N/A"
            # creating context variables that will be accessed inside result template
            context = {"url": url, "status_code": status_code, "response_time": response_time, "match": is_matching}
            return render(request, 'result.html', context)
        else:  # case of not valid form data
            return HttpResponseRedirect(reverse('home'))
    else:  # in case the request is not a POST
        return HttpResponseRedirect(reverse('home'))