from typing import Optional

from django.db.models import Count
from django.db.models.functions import TruncDay
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import UrlForm
from .models import Url, Click
from rest_framework import viewsets, mixins

from .serializers import UrlSerializer


def _render_index(request, form: Optional[UrlForm] = None):
    """
    Render the index page

    :param request: HttpRequest
    :param form: UrlForm
    :return: the rendered index page
    """
    # List all the urls
    urls = Url.objects.order_by('-created_at')

    # Create a new form
    if form is None:
        form = UrlForm()

    context = {
        'urls': urls,
        'form': form
    }
    return render(request, 'heyurl/index.html', context)


def index(request):
    """
    Render the index page

    :param request: HttpRequest
    :return: the rendered index page
    """
    return _render_index(request)


def store(request):
    """
    Validate the form and store the url
    :param request: HttpRequest
    :return: the rendered index page
    """
    form = UrlForm(request.POST)

    if form.is_valid():
        # Get the cleaned data
        cleaned_data = form.cleaned_data

        # Check if the original url is valid
        error_message = Url.is_valid_url(cleaned_data['original_url'])

        if error_message is None:
            # Store the url
            Url.objects.create(
                original_url=cleaned_data['original_url'],
            )
            return _render_index(request)

        # Add the error message to the form
        form.add_error('original_url', error_message)

    # Render the index page with the error message
    return _render_index(request, form)


def short_url_click(request, short_url):
    """
    Redirect to the original url if the short url exists
    :param request: HttpRequest
    :param short_url: the short url clicked
    :return: the original url redirect
    """
    url = Url.objects.filter(short_url=short_url).first()
    if url is None:
        return render(request, 'heyurl/short_url_not_found_404.html')

    url.clicks += 1
    url.save()

    dt_now = timezone.now()

    Click.objects.create(
        url=url,
        browser=request.user_agent.browser.family,
        platform=request.user_agent.os.family,
        created_at=dt_now,
        updated_at=dt_now
    )

    return redirect(url.original_url)


def metric_panel(request, short_url):
    """
    Render the metric panel page

    :param request: HttpRequest
    :param short_url: the short url clicked
    :return: the rendered metric panel page
    """
    url = Url.objects.filter(short_url=short_url).first()
    if url is None:
        return render(request, 'heyurl/short_url_not_found_404.html')

    dt_now = timezone.now()
    # Get the first day of the current month
    first_day = dt_now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # Get the first day of the next month and subtract 1 day to get the last day of the current month
    last_day = dt_now.replace(month=dt_now.month + 1, day=1, hour=23, minute=59, second=59, microsecond=999999)
    last_day = last_day - timezone.timedelta(days=1)

    # Get all the clicks for the current month
    clicks = list(Click.objects.filter(url=url, created_at__range=[first_day, last_day])
                  .annotate(date=TruncDay('created_at')).values('date').annotate(count=Count('id'))
                  .values('date', 'count'))

    # Get all the user agents for the current month
    user_agents = list(Click.objects.filter(url=url, created_at__range=[first_day, last_day])
                       .values('browser', 'platform'))

    context = {
        'clicks': clicks,
        'user_agents': user_agents,
        'short_url': short_url,
        'month': dt_now.strftime('%B'),
    }
    return render(request, 'heyurl/metric_panel.html', context)


class UrlViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer
