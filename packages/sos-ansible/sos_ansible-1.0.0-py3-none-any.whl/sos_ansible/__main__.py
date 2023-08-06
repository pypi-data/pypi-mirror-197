#!/usr/bin/env python
"""
sos_ansible, main program
"""

import argparse
import os
import sys
import logging.config as loggerconf
from logging import getLogger
import inquirer
from sos_ansible.modules.file_handling import (
    read_policy,
    process_rule,
    validate_tgt_dir,
)
from sos_ansible.modules.locating_sos import LocateReports
from sos_ansible.modules.config_manager import ConfigParser, validator


config = ConfigParser()
config.setup()
validator(config.config_handler)

loggerconf.fileConfig(config.config_file)
logger = getLogger("root")


def get_user_input(sos_directory):
    """Select workdir"""
    choice = os.listdir(sos_directory)
    questions = [
        inquirer.List("case", message="Choose the sos directory", choices=choice),
    ]
    return inquirer.prompt(questions)["case"]


def data_input(sos_directory, rules_file, user_choice):
    """
    Load the external sosreport and policy rules
    """
    logger.critical("Validating sosreports at the source directory: %s", sos_directory)
    report_data = LocateReports()
    node_data = report_data.run(sos_directory, user_choice)
    logger.critical("Validating rules in place: %s", rules_file)
    curr_policy = read_policy(rules_file)
    return node_data, curr_policy


def rules_processing(node_data, curr_policy, user_choice, debug):
    """
    Read the rules.json file and load it on the file_handling modules for processing.
    """
    div = "\n--------\n"
    for hosts in node_data:
        hostname = hosts["hostname"]
        path = hosts["path"]
        analysis_summary = (
            f"Summary\n{hostname}:{div}Controller Node: {hosts['controller']}{div}"
        )
        logger.critical("Processing node %s:", hostname)
        for rules in curr_policy:
            match_count = int()
            iterator = curr_policy[rules]
            for files in iterator["files"]:
                to_read = f"{path}/{iterator['path']}/{files}"
                query = iterator["query"].replace(", ", "|")
                match_count += process_rule(
                    hostname, user_choice, rules, to_read, query
                )
                if debug:
                    logger.debug(
                        "Rule: %s, Result: %s, Query: %s, Source: %s",
                        rules,
                        match_count,
                        query,
                        to_read,
                    )
            analysis_summary += f"{rules}: {match_count}\n"
        logger.critical(analysis_summary)


def main():
    """
    Main function from sos_ansible. This will process all steps for sosreports reading
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        help="Directory containing sosreports",
        required=False,
        default="",
    )
    parser.add_argument(
        "-r",
        "--rules",
        type=str,
        help="Rules file with full path",
        required=False,
        default="",
    )
    parser.add_argument(
        "-c",
        "--case",
        type=str,
        help="Directory number to which the sosreport was extracted",
        required=False,
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug message logging",
        required=False,
        default=False,
    )
    params = parser.parse_args()

    if params.directory:
        sos_directory = os.path.abspath(params.directory)
    else:
        sos_directory = os.path.abspath(
            os.path.expanduser(config.config_handler.get("files", "source"))
        )
    if params.rules:
        rules_file = os.path.expanduser(params.rules)
    else:
        rules_file = os.path.expanduser(config.config_handler.get("files", "rules"))

    # In order to allow both container and standard command line usage must check for env
    try:
        if os.environ["IS_CONTAINER"]:
            if not params.case:
                logger.error("A case number must be used if running from a container")
                sys.exit("A case number must be used if running from a container")
    except KeyError:
        pass
    # if case number is not provided prompt if provided just use it
    if os.path.isdir(sos_directory) and not params.case:
        user_choice = get_user_input(sos_directory)
    elif os.path.isdir(sos_directory) and params.case:
        user_choice = params.case
    else:
        logger.error(
            "The selected directory %s doesn't exist."
            "Select a new directory and try again.",
            sos_directory,
        )
        sys.exit(1)
    validate_tgt_dir(user_choice)
    node_data, curr_policy = data_input(sos_directory, rules_file, user_choice)
    if not node_data:
        logger.error(
            "No sosreports found, please review the directory %s", sos_directory
        )
        sys.exit(1)
    logger.debug("Node data: %s", node_data)
    if params.debug:
        logger.debug("Current policy: %s", curr_policy)
    rules_processing(node_data, curr_policy, user_choice, params.debug)
    logger.critical(
        "Read the matches at %s/%s",
        config.config_handler.get("files", "target"),
        user_choice,
    )
    logger.critical("sos-ansible finished.")


if __name__ == "__main__":
    main()
