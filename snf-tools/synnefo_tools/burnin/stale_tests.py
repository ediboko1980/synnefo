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

"""
This is the burnin class that handles stale resources (Servers/Networks)

"""

from synnefo_tools.burnin.common import Proper, SNF_TEST_PREFIX
from synnefo_tools.burnin.cyclades_common import CycladesTests


# pylint: disable=too-many-public-methods
class StaleServersTestSuite(CycladesTests):
    """Handle stale Servers"""
    stale_servers = Proper(value=None)

    def test_001_show_stale_servers(self):
        """Show staled servers (servers left from previous runs)"""
        servers = self._get_list_of_servers(detail=True)
        self.stale_servers = [s for s in servers
                              if s['name'].startswith(SNF_TEST_PREFIX)]

        len_stale = len(self.stale_servers)
        if len_stale == 0:
            self.info("No stale servers found")
            return

        self.info("Found %s stale servers:", len_stale)
        for stl in self.stale_servers:
            self.info("  Server \"%s\" with id %s", stl['name'], stl['id'])

    def test_002_delete_stale_servers(self):
        """Delete staled servers (servers left from previous runs)"""
        len_stale = len(self.stale_servers)
        if not self.delete_stale and len_stale != 0:
            self.fail("Use --delete-stale flag to delete stale servers")
        elif len_stale == 0:
            self.info("No stale servers found")
        else:
            self.info("Deleting %s stale servers", len_stale)
            self._delete_servers(self.stale_servers, error=True)


# pylint: disable=too-many-public-methods
class StaleFloatingIPsTestSuite(CycladesTests):
    """Handle stale Floating IPs"""
    stale_ips = Proper(value=None)

    def test_001_show_stale_ips(self):
        """Show staled floating IPs"""
        floating_ips = self.clients.network.list_floatingips()
        # We consider all the floating ips that are not attached
        # anywhere as stale ips.
        self.stale_ips = [ip for ip in floating_ips
                          if ip['instance_id'] is None]

        len_stale = len(self.stale_ips)
        if len_stale == 0:
            self.info("No stale floating IPs found")
            return

        self.info("Found %s stale floating IPs:", len_stale)
        for stl in self.stale_ips:
            self.info("  Floating IP %s with id %s",
                      stl['floating_ip_address'], stl['id'])

    def test_002_delete_stale_ips(self):
        """Delete staled floating IPs"""
        len_stale = len(self.stale_ips)
        if not self.delete_stale and len_stale != 0:
            self.fail("Use --delete-stale flag to delete stale floating IPs")
        elif len_stale == 0:
            self.info("No stale floating IPs found")
        else:
            self.info("Deleting %s stale floating IPs", len_stale)
            self._delete_floating_ips(self.stale_ips)


# pylint: disable=too-many-public-methods
class StaleNetworksTestSuite(CycladesTests):
    """Handle stale Networks"""
    stale_networks = Proper(value=None)

    def test_001_show_stale_networks(self):
        """Show staled networks (networks left from previous runs)"""
        networks = self._get_list_of_networks()
        self.stale_networks = [n for n in networks
                               if n['name'].startswith(SNF_TEST_PREFIX)]

        len_stale = len(self.stale_networks)
        if len_stale == 0:
            self.info("No stale networks found")
            return

        self.info("Found %s stale networks:", len_stale)
        for stl in self.stale_networks:
            self.info("  Network \"%s\" with id %s", stl['name'], stl['id'])

    def test_002_delete_stale_networks(self):
        """Delete staled networks (networks left from previous runs)"""
        len_stale = len(self.stale_networks)
        if not self.delete_stale and len_stale != 0:
            self.fail("Use --delete-stale flag to delete stale networks")
        elif len_stale == 0:
            self.info("No stale networks found")
        else:
            self.info("Deleting %s stale networks", len_stale)
            self._delete_networks(self.stale_networks)


# pylint: disable=too-many-public-methods
class StaleVolumesTestSuite(CycladesTests):
    """Handle stale Volumes"""
    stale_volumes = Proper(value=None)

    def test_001_show_stale_volumes(self):
        """Show staled volumes (volumes left from previous runs)"""
        volumes = self._get_volume_list(detail=True)
        self.stale_volumes = [
            vlm for vlm in volumes if vlm['display_name'] is not None and
            vlm['display_name'].startswith(SNF_TEST_PREFIX)]

        if len(self.stale_volumes) == 0:
            self.info("No stale volumes found")
            return

        self.info("Found %s stale volumes:", len(self.stale_volumes))
        for stl in self.stale_volumes:
            self.info("  Volume \"%s\" with id %s", stl['display_name'],
                                                    stl['id'])

    def test_002_delete_stale_volumes(self):
        """Delete staled volumes (volumes left from previous runs)"""
        len_stale = len(self.stale_volumes)
        if not self.delete_stale and len_stale != 0:
            self.fail("Use --delete-stale flag to delete stale volumes")
            return
        elif len_stale == 0:
            self.info("No stale volumes found")
        else:
            self.info("Deleting %s stale volumes", len(self.stale_volumes))
            for vlm in self.stale_volumes:
                self._destroy_volume(vlm)

# pylint: disable=too-many-public-methods
class StaleKeypairsTestSuite(CycladesTests):
    """Handle stale Keypairs"""
    stale_keypairs = Proper(value=None)

    def test_001_show_stale_keypairs(self):
        """Show staled keypairs (keypairs left from previous runs)"""
        keypairs = self._get_keypairs()
        self.stale_keypairs = [
            key for key in keypairs if key['name'] is not None and
            key['name'].startswith(SNF_TEST_PREFIX)]

        if len(self.stale_keypairs) == 0:
            self.info("No stale keypairs found")
            return

        self.info("Found %s stale keypairs:", len(self.stale_keypairs))
        for stl in self.stale_keypairs:
            self.info("  Keypair \"%s\"", stl['name'])

    def test_002_delete_stale_keypairs(self):
        """Delete staled keypairs (keypairs left from previous runs)"""
        len_stale = len(self.stale_keypairs)
        if not self.delete_stale and len_stale != 0:
            self.fail("Use --delete-stale flag to delete stale keypairs")
            return
        elif len_stale == 0:
            self.info("No stale keypairs found")
        else:
            self.info("Deleting %s stale keypairs", len(self.stale_keypairs))
            for key in self.stale_keypairs:
                self._delete_keypair(key)
