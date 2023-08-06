import json
import os
from dataclasses import asdict

import click
import yaml
from click.exceptions import ClickException
from requests import ConnectionError

from .ethz_iam import ETH_IAM
from .group import RecertificationPeriod
from .utils import gen_password

from .verbose import VERBOSE

recertification_period_map = {
    "A": "Annual",
    "Y": "Annual",
    "Q": "Quarterly",
    "B": "Biennial",
    "N": "No recertification",
}


class Credentials(object):
    def __init__(self, username=None, password=None):
        self.username = username or click.prompt(
            text="Username",
            default=os.environ.get("USER", ""),
            show_default=True,
        )
        self.password = password or click.prompt(text="Password", hide_input=True)


pass_iam_credentials = click.make_pass_decorator(Credentials)


def _load_configuration(paths, filename=".ethz_iam_webservice"):
    if paths is None:
        paths = [os.path.expanduser("~")]

    # look in all config file paths
    # for configuration files and load them
    admin_accounts = []
    for path in paths:
        abs_filename = os.path.join(path, filename)
        if os.path.isfile(abs_filename):
            with open(abs_filename, "r") as stream:
                try:
                    config = yaml.safe_load(stream)
                    for admin_account in config["admin_accounts"]:
                        admin_accounts.append(admin_account)
                except yaml.YAMLError as exc:
                    raise ClickException(exc)

    return admin_accounts


def login(
    admin_username=None,
    admin_password=None,
):

    return ETH_IAM(
        admin_username,
        admin_password,
    )


def get_username_password(ctx):

    if ctx.obj["username"] is None:
        ctx.obj["username"] = os.environ.get("IAM_USERNAME", "") or click.prompt(
            text="Username",
            default=os.environ.get("USER", ""),
            show_default=True,
        )

    if ctx.obj["password"] is None:
        ctx.obj["password"] = os.environ.get("IAM_PASSWORD", "") or click.prompt(
            text="Password", hide_input=True
        )


@click.group()
@click.option(
    "-u",
    "--username",
    envvar="IAM_USERNAME",
    help="username of ETHZ IAM admin account or IAM_USERNAME env",
)
@click.option(
    "--password",
    envvar="IAM_PASSWORD",
    help="password of ETHZ IAM admin account or IAM_PASSWORD env",
)
@click.version_option(prog_name="IAM command line tool")
@click.pass_context
def cli(ctx, username, password=None):
    """ETHZ IAM command-line tool."""
    ctx.obj = Credentials(username, password)


@cli.command("person", help="manage persons")
@click.argument("identifier")
@click.option(
    "-a",
    "--add-user",
    is_flag=True,
    help="Add an addtional user (aka persona) to this Person",
)
@click.option(
    "--delete-user",
    is_flag=True,
    help="Delete a username (aka persona) of this Person",
)
@click.option("-u", "--username", help="Username")
@click.option("-p", "--initpw", help="Initial password")
@click.option("-m", "--mail", help="email address")
@click.option("-f", "--firstname", help="given name of this user")
@click.option("-l", "--lastname", help="surname of this user")
@click.option("-d", "--description", help="Description about the purpose of this user")
@pass_iam_credentials
def person(
    credentials,
    identifier,
    add_user,
    delete_user,
    username,
    initpw,
    mail,
    firstname,
    lastname,
    description,
):

    iam = login(credentials.username, credentials.password)
    try:
        person = iam.get_person(identifier)
    except ConnectionError as exc:
        raise ClickException(f"Cannot connect to IAM webservice at {exc.request.url}")
    except ValueError as exc:
        raise ClickException(f"No person found with this identifier: {identifier}")

    if add_user and username:
        try:
            person.new_user(
                username=username,
                password=initpw,
                description=description,
                mail=mail,
                firstname=firstname or person["firstname"],
                lanstame=lastname or person["lastname"],
            )
        except ValueError as exc:
            raise ClickException(exc)
        person = iam.get_person(identifier)
    elif delete_user:
        if not username:
            raise ClickException(
                "Please provide the username you want to delete with -u <username>"
            )
        iam.del_user(identifier=person.username, username=username)
        person = iam.get_person(identifier)

    print(json.dumps(person.data, indent=4, sort_keys=True))


@cli.command("groups", help="show all kinds of groups (in LDAP only)")
@click.option("-m", "--member", help="Username that is member of a group")
@click.option("-n", "--group-name", help="Name of the group. Supports wildcards *")
@click.option("-g", "--gidnumber", help="gidNumber of the group")
@click.option("-t", "--type", help="type of the group, e.g. custom, lz, realm, ")
@pass_iam_credentials
def get_groups(credentials, member, group_name, gidnumber, type):
    iam = login(credentials.username, credentials.password)
    groups = iam.search_groups(
        group_name=group_name, member=member, gidnumber=gidnumber, group_type=type
    )
    click.echo(
        json.dumps([asdict(group) for group in groups], indent=4, sort_keys=True)
    )


@cli.command("group", help="manage security groups")
@click.argument("name")
@click.option(
    "--new-name",
    help="New name for this group (only used when renaming an existing group)",
)
@click.option(
    "-d",
    "--description",
    help="Description about this group.",
)
@click.option(
    "--agroup",
    "--ag",
    help="Admingroup for this group, mandatory for new a group",
)
@click.option(
    "-t",
    "--target",
    help="Add target system for this group. Can be used multiple times: -t AD -t LDAP",
    multiple=True,
)
@click.option(
    "--remove-target",
    "--rt",
    help="Remove target system for this group. Can be used multiple times.",
    multiple=True,
)
@click.option(
    "--organizational-unit",
    "--ou",
    help="OU (organizational unit) for this group, e.g. AGRL, USYS, INFK etc. where this group should be stored. If not specified, this group will appear in OU=Custom,OU=ETHLists",
)
@click.option(
    "--certification-period",
    "--cp",
    help="Define a certification period, whithin this group needs to be verified. [A]nnually, [B]iennial, [Q]uarterly, [N]one (default)",
)
@click.option(
    "--certification-note",
    "--cn",
    help="Reason (certification note) in case you don't want to periodically certify this group",
)
@click.option(
    "-m",
    "--manager",
    help="Username of the group manager for this group. Can appear multiple times. -m '' to remove all managers",
    multiple=True,
)
@click.option(
    "-a",
    "--add",
    help="Add username as member to group. Can be used multiple times: -a user1 -a user2",
    multiple=True,
)
@click.option(
    "-r",
    "--remove",
    help="Remove username as member to group. Can be used multiple times: -r user1 -r user2",
    multiple=True,
)
@click.option(
    "--add-subgroup",
    "--as",
    help="Add subgroup as member to group. Can be used multiple times.",
    multiple=True,
)
@click.option(
    "--remove-subgroup",
    "--rs",
    help="Remove subgroup as member from group. Can be used multiple times.",
    multiple=True,
)
@click.option("--new", "-n", is_flag=True, help="Create a group")
@click.option("--update", is_flag=True, help="Update a group")
@click.option("--recertify", is_flag=True, help="Recertify a group")
@click.option("--delete", is_flag=True, help="Delete a group")
@pass_iam_credentials
def group(
    credentials,
    name,
    new_name=None,
    description=None,
    agroup=None,
    target=None,
    remove_target=None,
    organizational_unit=None,
    certification_period=None,
    certification_note="No recertification needed",
    manager=None,
    add=None,
    remove=None,
    add_subgroup=None,
    remove_subgroup=None,
    new=False,
    update=False,
    recertify=False,
    delete=False,
):
    """manage groups
    Name of the group must start with the admingroup's nickname,
    followed by a dash, e.g. agrl-xxxx
    """
    iam = login(credentials.username, credentials.password)
    try:
        group = iam.get_group(name)
    except ValueError:
        group = None
    except ConnectionError as exc:
        raise ClickException(exc)

    if certification_period:
        if certification_period.upper() not in recertification_period_map:
            raise ClickException(
                "Please specify [A]nnual, [B]iennial, [Q]uarterly or [N]o recertification period."
            )
        else:
            certification_period = recertification_period_map[
                certification_period.upper()
            ]

    if new:
        if certification_period is None:
            certification_period = RecertificationPeriod.NONE.value
        if group:
            raise ClickException(f"A group named {name} already exists.")
        if not agroup:
            raise ClickException("Please provide an admingroup with --agroup")
        if not description:
            raise ClickException(
                "Description of the group is missing. Use -d 'some description'"
            )
        try:
            group = iam.new_group(
                name=name,
                description=description,
                admingroup=agroup,
                targets=[t.upper() for t in target],
                group_ad_ou=organizational_unit,
                certification_period=certification_period,
                certification_note=certification_note,
                managers=manager,
            )
        except ValueError as exc:
            raise ClickException(exc)
        except ConnectionError as exc:
            raise ClickException(
                f"Cannot connect to IAM webservice at {exc.request.url}"
            )
    elif delete:
        group.delete()
        click.echo(f"Successfully deleted {name}")
        return
    elif recertify:
        group.recertify()
        click.echo(f"Group {name} successfully recertified.")
    elif update:
        if not group:
            raise ClickException(f"No group {name} exists.")
        try:
            new_group = group.update(
                current_name=group.name,
                new_name=new_name,
                description=description,
                group_ad_ou=organizational_unit,
                certification_period=certification_period,
                certification_note=certification_note,
                managers=list(manager),
            )
            group = new_group if new_group else group
        except ValueError as exc:
            raise ClickException(exc)

    if not group:
        raise ClickException(
            f"No group found with name {name}. Use --new if you want to create a new group."
        )

    if add or add_subgroup:
        group.add_members(users=add, subgroups=add_subgroup)
    if remove or remove_subgroup:
        group.remove_members(users=remove, subgroups=remove_subgroup)
    if target and not new:
        targets = [t.upper() for t in target]
        try:
            group.set_targets(targets)
        except ValueError as exc:
            if "already present" in str(exc):
                pass
            else:
                raise ClickException(exc)
    if remove_target:
        targets = [t.upper() for t in remove_target]
        try:
            group.remove_targets(targets)
        except ValueError as exc:
            if "already not present" in str(exc):
                pass
            else:
                raise ClickException(exc)

    print(json.dumps(asdict(group), indent=4, sort_keys=True))


@cli.group("guest", help="manage guests")
def guest():
    pass


@guest.command("list", help="return all guest users of a given host leitzahl")
@click.argument("leitzahl")
@pass_iam_credentials
def get_guests(credentials, leitzahl):
    iam = login(credentials.username, credentials.password)
    try:
        guests = iam.get_guests_of_lz(leitzahl)
    except Exception as exc:
        raise ClickException(exc)
    click.echo(
        json.dumps([asdict(guest) for guest in guests], indent=4, sort_keys=True)
    )


@guest.command("get", help="get an existing guest")
@click.argument("username")
@pass_iam_credentials
def get_guest(credentials, username):
    iam = login(credentials.username, credentials.password)
    try:
        guest = iam.get_guest(username)
    except ConnectionError as exc:
        raise ClickException(f"Cannot connect to IAM webservice at {exc.request.url}")
    except ValueError as exc:
        raise ClickException(f"No such guest: {username}")
    print(json.dumps(guest.data, indent=4, sort_keys=True))


@guest.command(
    "extend", help="extend validation of an existing guest. Default is today+1 year."
)
@click.option(
    "-e", "--end-date", help="specify end date of guest (YYYY-MM-DD or DD.MM.YYYY)."
)
@click.option(
    "-m", "--months", help="extend validation of an existing guest by this many months."
)
@click.argument("username")
@pass_iam_credentials
def extend_guest(credentials, end_date, months, username):
    iam = login(credentials.username, credentials.password)
    try:
        guest = iam.extend_guest(username=username, end_date=end_date, months=months)
        print(json.dumps(guest.data, indent=4, sort_keys=True))
    except Exception as exc:
        raise ClickException(exc)


@click.option("-d", "--description", help="")
@click.option("-h", "--host-username", help="ETHZ Username of host")
@click.option(
    "-a",
    "--host-admingroup",
    help="Name of the admin group this guest should be connected to. Default: same as the technical user which is creating this guest.",
)
@click.option(
    "-o",
    "--host-leitzahl",
    help="Leitzahl of host organization, see http://www.org.ethz.ch. Default: Leitzahl of the host.",
)
@click.option(
    "-c",
    "--technical-contact",
    help="email address of technical contact. Default: email of the host of this guest.",
)
@click.option(
    "-n",
    "--notification",
    help="g=guest, h=host, t=technical contact. Use any combination of the 3 chars. Defaults to «gh»",
)
@click.option(
    "-e", "--end-date", help="End date of guest (YYYY-MM-DD). Default: today+1 year"
)
@click.option(
    "--deactivation-start-date",
    help='Deactivation start date of guest (YYYY-DD-MM). Set it to "" to remove',
)
@click.option(
    "--deactivation-end-date",
    help='Deactivation end date of guest (YYYY-MM-DD). Set it to "" to remove',
)
@guest.command("update", help="update an existing guest")
@click.argument("username")
@pass_iam_credentials
def update_guest(
    credentials,
    description,
    host_leitzahl,
    host_username,
    technical_contact,
    host_admingroup,
    notification,
    end_date,
    username,
    deactivation_start_date,
    deactivation_end_date,
):

    iam = login(credentials.username, credentials.password)
    try:
        guest = iam.update_guest(
            username=username,
            host_username=host_username,
            host_admingroup=host_admingroup,
            description=description,
            technical_contact=technical_contact,
            notification=notification,
            host_leitzahl=host_leitzahl,
            end_date=end_date,
            deactivation_start_date=deactivation_start_date,
            deactivation_end_date=deactivation_end_date,
        )
        print(json.dumps(guest.data, indent=4, sort_keys=True))
    except ConnectionError as exc:
        raise ClickException(f"Cannot connect to IAM webservice at {exc.request.url}")


@guest.command("delete", help="delete an existing guest")
@click.argument("username")
@pass_iam_credentials
def delete_guest(
    credentials,
    username,
):

    iam = login(credentials.username, credentials.password)
    try:
        iam.delete_guest(username=username)
        click.echo(f"Guest {username} successfully deleted.")
    except ConnectionError as exc:
        raise ClickException(f"Cannot connect to IAM webservice at {exc.request.url}")


@guest.command("new", help="create a new guest")
@click.option("-f", "--firstname", required=True, help="given name")
@click.option("-l", "--lastname", required=True, help="surname")
@click.option("-m", "--mail", required=True, help="email address")
@click.option("-d", "--description", required=True, help="")
@click.option("-h", "--host-username", required=True, help="ETHZ Username of host")
@click.option(
    "-a",
    "--host-admingroup",
    required=True,
    help="Name of the administrative group that hosts this guest.",
)
@click.option(
    "-o",
    "--host-leitzahl",
    help="Leitzahl of host organization, see http://www.org.ethz.ch. If not provided, the leitzahl of the host will be used.",
)
@click.option(
    "-c",
    "--technical-contact",
    help="email address of technical contact. If not provided, the email address of the host will be used.",
)
@click.option(
    "-b",
    "--birth-date",
    help="birthdate in YYYY-MM-DD format. Default: Today's date + year 2000",
)
@click.option(
    "-n",
    "--notification",
    default="gh",
    help="g=guest, h=host, t=technical contact. Use any combination of the 3 chars. ",
)
@click.option(
    "-s", "--start-date", help="Start date of guest (YYYY-DD-MM). Default: today"
)
@click.option(
    "-e", "--end-date", help="End date of guest (YYYY-MM-DD). Default: today+1 year"
)
@click.option(
    "--init-password",
    is_flag=True,
    help="Set initial password and return it in cleartext",
)
@pass_iam_credentials
def new_guest(
    credentials,
    firstname,
    lastname,
    mail,
    description,
    birth_date,
    host_leitzahl,
    host_username,
    technical_contact,
    host_admingroup,
    notification,
    start_date,
    end_date,
    init_password,
):
    iam = login(credentials.username, credentials.password)
    try:
        pass
        guest = iam.new_guest(
            firstname=firstname,
            lastname=lastname,
            mail=mail,
            birth_date=birth_date,
            host_username=host_username,
            host_admingroup=host_admingroup,
            description=description,
            technical_contact=technical_contact,
            notification=notification,
            host_leitzahl=host_leitzahl,
            start_date=start_date,
            end_date=end_date,
        )
    except ConnectionError as exc:
        raise ClickException(f"Cannot connect to IAM webservice at {exc.request.url}")
    except ValueError as exc:
        raise ClickException(exc) from exc

    ldap_password = gen_password()
    vpn_password = gen_password()
    guest_data = guest.data

    if not guest.username:
        ClickException(
            "could not set inital password for the guest because the guest has no username."
        )

    if init_password:
        guest_user = iam.get_user(guest.username)
        try:
            guest_user.set_password(password=ldap_password, service_name="LDAP")
            guest_data["init_ldap_password"] = ldap_password
        except Exception as exc:
            print(exc)
            pass

        try:
            guest_user.set_password(password=vpn_password, service_name="VPN")
            guest_data["init_vpn_password"] = vpn_password
        except Exception as exc:
            print(exc)
            pass

    print(json.dumps(guest_data, indent=4, sort_keys=True))


@cli.command("user", help="manage users and their services")
@click.argument("username")
@click.option("-d", "--delete", is_flag=True, help="delete this user")
@click.option(
    "-i",
    "--info",
    is_flag=True,
    help="all information about the user",
)
@click.option(
    "-g",
    "--grant-service",
    multiple=True,
    help="grant a service to this user, e.g. AD, LDAPS, VPN. Use this option for every service you want to grant",
)
@click.option(
    "-r",
    "--revoke-service",
    multiple=True,
    help="revoke a service from this user, e.g. AD, LDAPS, VPN. Use this option for every service you want to revoke",
)
@click.option(
    "--init-password",
    is_flag=True,
    help="set the inital password(s) for this user (LDAPS and VPN). Returns the passwords in cleartext.",
)
@click.option(
    "--set-password",
    is_flag=True,
    help="set the password for that user. Use -s to specify for which service(s)",
)
@click.option(
    "-s",
    "--service",
    multiple=True,
    help="specify the service you want to set the password for",
)
@click.option(
    "-sp",
    "--service-password",
    help="set a password for the given service. Use the --service option to specify the service.",
)
@pass_iam_credentials
def user(
    credentials,
    username,
    delete,
    info,
    grant_service=None,
    revoke_service=None,
    init_password=None,
    set_password=None,
    service_password=None,
    service=None,
):
    iam = login(credentials.username, credentials.password)
    try:
        user = iam.get_user(username)
    except ConnectionError as exc:
        raise ClickException(f"Cannot connect to IAM webservice at {exc.request.url}")

    if delete:
        click.confirm("Do you really want to delete this user?", abort=True)
        user.delete()

    elif grant_service:
        for service_name in grant_service:
            user.grant_service(service_name)

    elif revoke_service:
        for service_name in revoke_service:
            user.revoke_service(service_name)
    elif init_password:
        ldap_password = gen_password()
        ad_password = gen_password()
        vpn_password = gen_password()
        init_pw = {}
        for service in user.data["services"]:
            if service.get("name") == "LDAP":
                try:
                    user.set_password(password=ldap_password, service_name="LDAP")
                    init_pw["init_ldap_password"] = ldap_password
                except Exception as exc:
                    pass
            elif service.get("name") in ["AD", "Active Directory", "Mailbox"]:
                try:
                    user.set_password(password=ad_password, service_name="AD")
                    init_pw["init_ad_password"] = ad_password
                except Exception as exc:
                    print(exc)
                    pass
            elif service.get("name") in ["WLAN_VPN"]:
                try:
                    user.set_password(password=vpn_password, service_name="VPN")
                    init_pw["init_vpn_password"] = vpn_password
                except Exception as exc:
                    pass
        print(json.dumps(init_pw, indent=4, sort_keys=True))

    elif service_password or set_password:
        if not service_password:
            service_password = click.prompt(text="Service Password", hide_input=True)
        if service:
            for s in service:
                try:
                    user.set_password(password=service_password, service_name=s)
                    print(f"successfully set password for service {s}")
                except ValueError as err:
                    print(err)
        elif "services" in user.data:
            for service in user.data["services"]:
                try:
                    user.set_password(
                        password=service_password, service_name=service["name"]
                    )
                    print(
                        "successfully set password for service {}".format(
                            service["name"]
                        )
                    )
                except ValueError as err:
                    print(err)
    else:
        print(json.dumps(user.data, indent=4, sort_keys=True))


if __name__ == "__main__":
    cli()
