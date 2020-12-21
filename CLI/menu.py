import click
from click_shell import shell
from terminaltables import SingleTable

from Network.user import User
from Network.scan import Scan
from Network.limit import Limiter
from Network.ARP_spoofing import ARP_spoofer

from utilities import get_interface, get_gateway, get_interface_MAC, cust_unit_to_barebits
from CLI.click_output import message_out, error_out

from utilities import *
from CLI.logo import NONET4U_logo


class Menu:
    def __init__(self, interface, gateway, iprange):
        self.interface = interface
        self.gateway = gateway
        self.iprange = iprange 
        # Storing users
        self.hosts = []
        self.limited = {}
        # Table to show pretty status
        self.table = None
        # Used to exclude own address
        self.own_mac = get_interface_MAC(self.interface)

        """
        Network tools
        """
        self.limiter = Limiter(self.interface)
        self.scanner = Scan(self.interface, self.iprange, self.own_mac)
        self.spoofer = ARP_spoofer(
        self.interface, self.gateway, get_interface_MAC(self.interface))


# Reference for the global Click Context: Stores all important data in the for of a Menu object (hosts, range, interface, etc)
# Also used as a reference for default values as well as passing data to the child commands through @click.pass_obj (@click.pass_obj = ctx.obj)


"""
 Click group
"""


@shell(prompt=click.style('>>', fg='red'))
@click.argument('interface')
@click.argument('gateway')
@click.argument('iprange')
@click.pass_context
def main_menu(ctx, interface, gateway, iprange):
    ctx.obj = Menu(interface,gateway,iprange)
    # Start the spoofer on creation
    ctx.obj.spoofer.start()


"""
 DEF CLICK_SCAN
 Used to scan the network for users
"""


@click.command()
@click.option('-n', '--network', help='Define required network range to scan (e.g. 192.16.7.0 - 192.15.7.10')
@click.pass_obj
def scan(ctx, network):
    """
    Scans the network for available users
    """

    _iprange = ctx.iprange
    ctx.hosts = ctx.scanner.scan_for_hosts(_iprange)


@click.command()
@click.argument('user', nargs=-1)
@click.argument('speed')
@click.option('-d', '--download')
@click.option('-u', '--upload')
@click.pass_obj
def limit(ctx, user, speed, download, upload):
    

    # Convert speed to string #TODO
    _speed = cust_unit_to_barebits(speed)
    direction = None
    user = list(user)

    # First, let's see the direction (up, down, both)
    if download is not None:
        direction = download
    elif upload is not None:
        direction = upload
    else:
        direction = 3
    
    direction  = 3

    # Secondly, let's see if all or just certain users need to be limited
    if user[0] == 'all':
        # check if there are users in the list - otherwise, prompt to scan!
        if ctx.hosts:
            # Set users to limited
            for user in ctx.hosts:
                _limited_user = ctx.limiter.limit(user, direction, _speed, ctx.limited)
                ctx.spoofer.add_user(user)

        else:
            error_out(
                'No users could be found! Try scanning first (click-scan')
    else:
        if ctx.hosts:
            # check if there is an user with the entered ID
            for _id in user:
                for _usr in ctx.hosts:
                    if int(_id) == _usr.host_id:
                        # Limit users
                        ctx.limiter.limit(_usr, direction, _speed, ctx.limited)
                        ctx.spoofer.add_user(_usr)
                
                message_out(str(_usr) + ' is limited to ' + str(speed))

        else:
            error_out('No users could be found! Try scanning first (click-scan)')


@click.command()
@click.argument('user', nargs=-1)
@click.pass_obj
def block(ctx, user):
    # turn tuple into list items
    user = list(user)

    if ctx.hosts:
        if user[0] == 'all':
            for _id in ctx.hosts:
                ctx.limiter.block(_id, ctx.limited)
                _id.isSpoofed = True
                ctx.spoofer.add_user(_id)
        else:
            for _user in user:
                for _id in list(ctx.hosts):
                    if int(_user) == _id.host_id:
                        ctx.limiter.block(_id, ctx.limited)
                        _id.isSpoofed = True
                        ctx.spoofer.add_user(_id)
                
                click.echo(ctx.limited)

    else:
        error_out('No users could be found! Try scanning first (click-scan)')


"""
Frees limited users
"""
@click.command()
@click.argument('user', nargs=-1)
@click.pass_obj
def free(ctx, user):
    """
    Frees blocked or limited users! 
    Usage: click-free all, 1 2 3
    """

    # turn tuple into list
    user = list(user)

    if ctx.hosts:
        if user[0] == 'all':
            for _limited_user in list(ctx.limited):
                ctx.limiter.unlimit(_limited_user, ctx.limited)
                ctx.spoofer.remove_user(_limited_user)

        else:
            for _user in user:
                for _limited_user in list(ctx.limited):
                    if int(_user) == _limited_user.host_id:
                        ctx.limiter.unlimit(_limited_user, ctx.limited)
                        ctx.spoofer.remove_user(_limited_user)
    else:
        error_out('No users could be found! Try scanning first (click-scan)')


"""
Lists scanned users. If no users have been scanned, error message will be thrown!
"""


@click.command()
@click.pass_obj
def users(ctx):
    """
    List scanned users with information and status in the form of a table
    """
    data = [['ID', 'Name', 'IP', 'Status']]
    table = SingleTable(data, title='SCANNED USERS')

    if ctx.hosts:
        for usr in ctx.hosts:
            _info = [usr.host_id, usr.name, usr.ip, usr.get_status()]
            data.append(_info)

        message_out(table.table)
    else:
        error_out('No users. Try scanning first!')


"""
 Clears the terminal and prints the logo
"""


@click.command()
def clear():
    """
    Used to clear the terminal
    """
    click.clear()
    message_out(NONET4U_logo)


main_menu.add_command(scan)
main_menu.add_command(block)
main_menu.add_command(limit)
main_menu.add_command(free)
main_menu.add_command(users)
main_menu.add_command(clear)


