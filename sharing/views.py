# -*- coding: utf-8 -*-
from django.http import HttpResponseForbidden
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from core.mixins import OwnerRequiredMixin
from core.mixins import LoginRequiredMixin
from sharing.forms import HPFeedsChannelForm
from sharing.models import HPFeedsChannel
from sharing.models import HPFeedsPubQueue


class HPFeedsChannelCreateView(CreateView, LoginRequiredMixin):

    """
    A view class for creating HPFeeds channels.
    """

    model = HPFeedsChannel
    form_class = HPFeedsChannelForm
    template_name = 'channel/create.html'
    success_url = reverse_lazy('channel.list')

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        kwargs['user'] = self.request.user
        return form_class(**kwargs)

    def form_valid(self, form):
        # save the user of channel
        form.instance.user = self.request.user
        return super(HPFeedsChannelCreateView, self).form_valid(form)


class HPFeedsChannelListView(ListView, LoginRequiredMixin):

    """
    Listing all channels that own by an user.
    """

    model = HPFeedsChannel
    template_name = 'channel/list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class HPFeedsChannelUpdateView(UpdateView, OwnerRequiredMixin):

    """
    UpdateView for HPFeedsChannel.
    """

    model = HPFeedsChannel
    form_class = HPFeedsChannelForm
    template_name = 'channel/update.html'
    success_url = reverse_lazy('channel.list')

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        kwargs['user'] = self.request.user
        return form_class(**kwargs)


class HPFeedsChannelDeleteView(DeleteView, OwnerRequiredMixin):

    """
    DeleteView for HPFeedsChannel
    """

    model = HPFeedsChannel
    template_name = 'channel/delete.html'
    success_url = reverse_lazy('channel.list')


class HPFeedsPubQueueListView(ListView, LoginRequiredMixin):

    """
    Listing publishing queue of an user.
    Users are allowed to review queue own by them.
    """

    model = HPFeedsPubQueue
    template_name = 'queue/list.html'

    def get_queryset(self):
        return self.model.objects.filter(sample__user=self.request.user)

