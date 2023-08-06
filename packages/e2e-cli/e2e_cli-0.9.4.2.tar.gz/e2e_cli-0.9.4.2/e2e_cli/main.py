import argparse
from functools import reduce

from e2e_cli.commands_routing import CommandsRouting
from e2e_cli.core.error_logs_service import ErrorLogs

class Main:
    def __init__(self):
        pass

    def FormatUsage(self, parser, action):
        format_string = "e2e_cli" + " alias"+ " " + action + " [-h]" + " {create,delete,list,edit/update} ... "
        parser.usage = format_string

    def FormatUsageCommand(self, parser, action, command):
        format_string = "e2e_cli" + " alias"+ " " + action + " [-h] " + command
        subparser_list = list(parser._subparsers._group_actions[0].choices.keys())
        subparser_string = "{ " + reduce(lambda a, b: a + ", " + b, subparser_list) + " }"
        format_string = "e2e_cli" + " alias=" + "<alias_name>"+ " " + action + " [-h]" + " " + subparser_string
        parser.usage = format_string

    def FormatUsageCommand(self, parser, action, command):
        format_string = "e2e_cli" + " alias=" + "<alias_name>"+ " " + action + " [-h] " + command
        parser.usage = format_string

    def config(self, parser):
        config_sub_parser = parser.add_subparsers(title="Config Commands", dest="config_commands")
        config_add_sub_parser = config_sub_parser.add_parser("add", help="To add api key and auth token")
        config_delete_sub_parser = config_sub_parser.add_parser("delete", help="To delete api key and auth token")
        config_view_sub_parser = config_sub_parser.add_parser("view", help="To view all alias and credentials")
        self.FormatUsageCommand(config_add_sub_parser, "config", "add")
        self.FormatUsageCommand(config_delete_sub_parser, "config", "delete")
        self.FormatUsageCommand(config_view_sub_parser, "config", "view")

    def node(self, parser):
        node_sub_parser = parser.add_subparsers(title="node Commands", dest="node_commands")
        node_action=parser.add_argument('-action', '--action', help="Type of action to be performed your node")
        node_create_sub_parser = node_sub_parser.add_parser("create", help="To create a new node")
        node_delete_sub_parser = node_sub_parser.add_parser("delete", help="To delete a specific node")
        node_list_sub_parser = node_sub_parser.add_parser("list", help="To get a list of all nodes")
        node_get_sub_parser = node_sub_parser.add_parser("get", help="To get a list of all nodes")
        self.FormatUsageCommand(node_action, "node", "actions")
        self.FormatUsageCommand(node_create_sub_parser, "node", "create")
        self.FormatUsageCommand(node_delete_sub_parser, "node", "delete")
        self.FormatUsageCommand(node_list_sub_parser, "node", "list")
        self.FormatUsageCommand(node_get_sub_parser, "node", "get")

    def lb(self, parser):
        node_sub_parser = parser.add_subparsers(title="LB Commands", dest="lb_commands")
        node_create_sub_parser = node_sub_parser.add_parser("create", help="To create a new node")
        node_delete_sub_parser = node_sub_parser.add_parser("delete", help="To delete a specific node")
        node_list_sub_parser = node_sub_parser.add_parser("list", help="To get a list of all nodes")
        node_edit_sub_parser = node_sub_parser.add_parser("edit", help="To get a list of all nodes")
        self.FormatUsageCommand(node_create_sub_parser, "node", "create")
        self.FormatUsageCommand(node_delete_sub_parser, "node", "delete")
        self.FormatUsageCommand(node_list_sub_parser, "node", "list")
        self.FormatUsageCommand(node_edit_sub_parser, "node", "edit")

    def bucket(self, parser):
        bucket_sub_parser = parser.add_subparsers(title="bucket Commands", dest="bucket_commands")
        bucket_create_sub_parser = bucket_sub_parser.add_parser("create", help="To create a new bucket")
        bucket_delete_sub_parser = bucket_sub_parser.add_parser("delete", help="To delete a specific bucket")
        bucket_delete_sub_parser = bucket_sub_parser.add_parser("list", help="To get a list of all buckets")
        self.FormatUsageCommand(bucket_create_sub_parser, "bucket", "create")
        self.FormatUsageCommand(bucket_delete_sub_parser, "bucket", "delete")
        self.FormatUsageCommand(bucket_delete_sub_parser, "bucket", "list")    


    def dbaas(self, parser):
        dbaas_sub_parser = parser.add_subparsers(title="DBaaS Commands", dest="dbaas_commands")
        dbaas_create_sub_parser = dbaas_sub_parser.add_parser("create", help="To launch a new dbaas")
        dbaas_delete_sub_parser = dbaas_sub_parser.add_parser("delete", help="To delete a created dbaas")
        dbaas_list_sub_parser = dbaas_sub_parser.add_parser("list", help="To list all of your dbaas")
        self.FormatUsageCommand(dbaas_create_sub_parser, "dbaas", "create")
        self.FormatUsageCommand(dbaas_list_sub_parser, "dbaas", "list")
        self.FormatUsageCommand(dbaas_delete_sub_parser, "dbaas", "delete")

        
def run_main_class():
    parser = argparse.ArgumentParser(description="E2E CLI")
    parser.add_argument("alias", type=str, help="The name of your API access credentials")
    sub_parsers = parser.add_subparsers(title="Commands", dest="command")
    config_parser = sub_parsers.add_parser("config", help="To add or delete api key and auth token")
    node_parser = sub_parsers.add_parser("node", help="To apply crud operations over Nodes")
    lb_parser = sub_parsers.add_parser("lb", help="To apply operations over Load-Balancer")
    bucket_parser = sub_parsers.add_parser("bucket", help="To add/delete/list buckets of the user")
    dbaas_parser = sub_parsers.add_parser("dbaas", help="To do operations over DBaaS service provided")
    m = Main()
    m.config(config_parser)
    m.bucket(bucket_parser)
    m.node(node_parser)
    m.dbaas(dbaas_parser)
    m.lb(lb_parser)

    m.FormatUsage(config_parser, "config")
    m.FormatUsage(node_parser, "node")
    m.FormatUsage(lb_parser, "lb")
    m.FormatUsage(bucket_parser, "bucket")
    m.FormatUsage(dbaas_parser, "dbaas")
    
    args = parser.parse_args()
    if(args.alias=="error_logs"):
            ErrorLogs.recent_errors()
    else:
        commands_route = CommandsRouting(args)
        commands_route.route()
