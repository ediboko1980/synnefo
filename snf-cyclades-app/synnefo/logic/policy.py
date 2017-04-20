# Copyright (C) 2010-2017 GRNET S.A.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db.models import Q
from synnefo.db import models
from snf_django.lib.api import faults


class Policy(object):
    model = None

    @classmethod
    def filter_list(cls, credentials, extend=None):
        queryset = cls.model.objects.all()
        if credentials.is_admin:
            return queryset

        _filter = (
            Q(userid=credentials.userid) |
            Q(shared_to_project=True, project__in=credentials.user_projects)
        )
        if extend:
            _filter |= extend
        return queryset.filter(_filter)


class VMPolicy(Policy):
    model = models.VirtualMachine


class NetworkPolicy(Policy):
    model = models.Network

    @classmethod
    def filter_list(cls, credentials, include_public=True):
        extend = Q(public=True) if include_public else Q()
        return super(NetworkPolicy, cls).filter_list(
            credentials, extend=extend)


class SubnetPolicy(Policy):
    model = models.Subnet

    @classmethod
    def filter_list(cls, credentials, include_public=True):
        networks = NetworkPolicy.filter_list(credentials, include_public)
        return cls.model.objects.filter(network__in=networks)


class IPAddressPolicy(Policy):
    model = models.IPAddress


class NetworkInterfacePolicy(Policy):
    model = models.NetworkInterface

    @classmethod
    def filter_list(cls, credentials):
        queryset = cls.model.objects.all()
        if credentials.is_admin:
            return queryset

        vms = VMPolicy.filter_list(credentials)
        networks = NetworkPolicy.filter_list(credentials).filter(public=False)
        ips = IPAddressPolicy.filter_list(credentials).filter(floating_ip=True)

        _filter = Q(userid=credentials.userid)
        _filter |= Q(machine__in=vms)
        _filter |= Q(network__in=networks)
        _filter |= Q(ips__in=ips)
        return queryset.filter(_filter)


class VolumePolicy(Policy):
    model = models.Volume
