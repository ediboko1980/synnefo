#
# Utility functions
#
# Various functions
#
# Copyright 2010 Greek Research and Technology Network
#

from db.models import VirtualMachine

from logic import credits

import synnefo.settings as settings

def id_from_instance_name(name):
    """Returns VirtualMachine's Django id, given a ganeti machine name.

    Strips the ganeti prefix atm. Needs a better name!

    """
    if not str(name).startswith(settings.BACKEND_PREFIX_ID):
        raise VirtualMachine.InvalidBackendIdError(str(name))
    ns = str(name).lstrip(settings.BACKEND_PREFIX_ID)
    if not ns.isdigit():
        raise VirtualMachine.InvalidBackendIdError(str(name))

    return int(ns)


def get_rsapi_state(vm):
    """Returns the RSAPI state for a virtual machine"""
    try:
        r = VirtualMachine.RSAPI_STATE_FROM_OPER_STATE[vm._operstate]
    except KeyError:
        return "UNKNOWN"
    # A machine is in REBOOT if an OP_INSTANCE_REBOOT request is in progress
    if r == 'ACTIVE' and vm._backendopcode == 'OP_INSTANCE_REBOOT' and \
        vm._backendjobstatus in ('queued', 'waiting', 'running'):
        return "REBOOT"
    return r

def update_state(self, new_operstate):
    """Wrapper around updates of the _operstate field

    Currently calls the charge() method when necessary.

    """

    # Call charge() unconditionally before any change of
    # internal state.
    credits.charge(self)
    self._operstate = new_operstate
