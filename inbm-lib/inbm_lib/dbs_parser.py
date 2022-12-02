"""
    Module which runs the Docker Bench Security check on docker images and containers.
    
    Copyright (C) 2017-2022 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""
import logging
import re

from typing import List, Dict, Union
import traceback

logger = logging.getLogger(__name__)


def parse_docker_bench_security_results(dbs_output: str) -> Dict[str, Union[bool, str, List[str]]]:
    """Parse failed images and containers from DBS output.

    @param dbs_output: Output from DBS.

    @return: Dictionary with DBS results. Keys are success_flag (true/false--did DBS pass?); failed_images,
    failed_containers (lists of container/image names that failed); result (text summary of DBS result);
    and fails (text summary of DBS failures)
    """
    for line in traceback.format_stack():
        logger.debug(line.strip())
    logger.debug("############################# dbs_parser #################################")
    logger.debug(result)
    logger.debug(fails)
    result = "Test results: "
    fails = "Failures in: "
    logger.debug("############################# dbs_parser1 #################################")
    logger.debug(result)
    logger.debug(fails)
    logger.debug("############################# dbs_parser2 #################################")
    logger.debug(success_flag)
    logger.debug(prev_warn)
    success_flag = True
    prev_warn = False
    logger.debug("############################# dbs_parser3 #################################")
    logger.debug(success_flag)
    logger.debug(prev_warn)
    logger.debug("############################# dbs_parser4 #################################")
    logger.debug(failed_images)
    logger.debug(failed_containers)
    failed_images: List = []
    failed_containers: List = []
    logger.debug("############################# dbs_parser5 #################################")
    logger.debug(failed_images)
    logger.debug(failed_containers)
    for line in dbs_output.splitlines():
        logger.debug("############################# dbs_parser6 #################################")
        logger.debug(line)
        logger.debug(prev_warn)
        if _is_name_in_line(line, prev_warn):
            logger.debug("############################# dbs_parser7 #################################")
            logger.debug(line)
            logger.debug(failed_containers)
            logger.debug(failed_images)
            _fetch_names_for_warn_test(line, failed_containers, failed_images)
            logger.debug("############################# dbs_parser8 #################################")
            logger.debug(line)
            logger.debug(failed_containers)
            logger.debug(failed_images)
        if _is_test_warn(line):
            logger.debug("############################# dbs_parser9 #################################")
            logger.debug(line)
            logger.debug(fails)
            fails = _add_test_in_fails(line, fails)
            logger.debug("############################# dbs_parser10 #################################")
            logger.debug(line)
            logger.debug(fails)
            logger.debug(success_flag)
            logger.debug(prev_warn)
            success_flag = False
            prev_warn = True
            continue
        logger.debug("############################# dbs_parser11 #################################")
        logger.debug(prev_warn)
        prev_warn = False
        logger.debug("############################# dbs_parser12 #################################")
        logger.debug(success_flag)
        logger.debug(failed_images)
        logger.debug(failed_containers)
        logger.debug(result)
        logger.debug(fails)
    return {'success_flag': success_flag,
            'failed_images': failed_images,
            'failed_containers': failed_containers,
            'result': result,
            'fails': fails}


def _is_name_in_line(line: str, prev_warn: bool) -> bool:
    logger.debug("############################# dbs_parser__is_name_in_line #################################")
    logger.debug(line)
    logger.debug(prev_warn)
    return True if "*" in line and prev_warn else False


def _is_test_warn(line: str) -> bool:
     logger.debug("############################# dbs_parser__is_test_warn #################################")
     logger.debug(line)
     return True if "WARN" in line else False


def _fetch_names_for_warn_test(line: str, failed_containers: List[str], failed_images: List[str]) -> None:
    logger.debug("############################# dbs_parser__fetch_names_for_warn_test #################################")
    logger.debug(line)
    logger.debug(failed_images)
    if ": [" in line:
        logger.debug(line)
        logger.debug(failed_images)
        _append_image_name(line, failed_images)
        logger.debug(line)
        logger.debug(failed_images)
    elif ": " in line:
        logger.debug(line)
        logger.debug(failed_images)
        _append_container_name(line, failed_containers)
        logger.debug(line)
        logger.debug(failed_images)


def _add_test_in_fails(line: str, fails: str) -> str:
    logger.debug("############################# dbs_parser__add_test_in_fails #################################")
    logger.debug(fails)
    fails += line.split(" ")[1] + ","
    logger.debug(fails)
    return fails


DBS_CONTAINER_REGEX = "^.*\\[WARN\\].*: ([^[]*)$"


def _append_container_name(line, failed_containers):
    logger.debug("############################# dbs_parser_def _append_container_name #################################")
    logger.debug(DBS_CONTAINER_REGEX)
    logger.debug(line)
    logger.debug(matches)
    matches = re.findall(DBS_CONTAINER_REGEX, line)
    logger.debug(DBS_CONTAINER_REGEX)
    logger.debug(line)
    logger.debug(matches)
    if len(matches) == 1:
        logger.debug(name)
        logger.debug(matches)
        name = matches[len(matches) - 1]
        logger.debug(name)
        logger.debug(matches)
        if name not in failed_containers:
            logger.debug("############################# dbs_parser_def _append_container_name - 1 #################################")
            logger.debug(failed_containers)
            logger.debug(name)
            failed_containers.append(name)
            logger.debug(failed_containers)
            logger.debug(name)


DBS_IMAGE_REGEX = "^.*\\[WARN\\].*: \\[([^[\\]]*)\\]$"


def _append_image_name(line, failed_images):
    logger.debug("############################# dbs_parser_def _append_image_name #################################")
    logger.debug(DBS_CONTAINER_REGEX)
    logger.debug(line)
    logger.debug(matches)
    matches = re.findall(DBS_IMAGE_REGEX, line)
    logger.debug("############################# dbs_parser_def _append_image_name 1 #################################")
    logger.debug(DBS_CONTAINER_REGEX)
    logger.debug(line)
    logger.debug(matches)
    if len(matches) == 1:
        logger.debug("############################# dbs_parser_def _append_image_name 2 #################################")
        logger.debug(name)
        logger.debug(matches)
        name = matches[len(matches) - 1]
        logger.debug(name)
        logger.debug(matches)
        if name not in failed_images:
            logger.debug("############################# dbs_parser_def _append_image_name 2 #################################")
            logger.debug(name)
            logger.debug(failed_images)
            failed_images.append(name)
