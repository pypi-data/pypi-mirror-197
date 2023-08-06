#!/usr/bin/env python
#
# Copyright 2023 StreamSets Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import logging

import docker
from docker.utils import kwargs_from_env
from streamsets.sdk import ControlHub

from streamsets.testframework import logger as streamsets_logger
from streamsets.testframework.constants import (DEFAULT_DOCKER_TIMEOUT,
                                                DATACOLLECTOR_TESTRUN_DOCKER_LABEL_ID)
from streamsets.testframework.utils import gethostname


# Get rid of handlers on the root logger to avoid duplicate output (see STF-959).
logging.getLogger().handlers.clear()

logger = logging.getLogger('streamsets.testframework.cli.stop_sdc')

docker_client = docker.APIClient(timeout=DEFAULT_DOCKER_TIMEOUT, **kwargs_from_env())


def _main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', action='store_true', help='Be noisier')
    parser.add_argument('--aster-server-url', help='Aster url')
    parser.add_argument('--sch-credential-id', help='StreamSets Control Hub component ID')
    parser.add_argument('--sch-token', help='StreamSets Control Hub auth token')
    parser.add_argument('--container-id', required=True, help='The SDC container ID.')
    args = parser.parse_args()

    streamsets_logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    sch = None
    if args.aster_server_url and args.sch_credential_id and args.sch_token:
        sch = ControlHub(credential_id=args.sch_credential_id,
                         token=args.sch_token,
                         aster_url=args.aster_server_url)

    container_data = docker_client.inspect_container(args.container_id)

    container_labels = container_data['Config']['Labels']

    testrun_id = container_labels.get(DATACOLLECTOR_TESTRUN_DOCKER_LABEL_ID)
    if testrun_id and sch:
        for data_collector in sch.data_collectors:
            if testrun_id in data_collector.labels:
                sch.delete_and_unregister_engine(data_collector)
                break

    # Cleanup SDC container
    logger.debug('Stopping and removing docker container %s', args.container_id)
    docker_client.stop(args.container_id)
    docker_client.remove_container(args.container_id, v=True, force=True)

    if testrun_id:
        # Cleanup lib containers
        logger.debug('Removing lib containers')
        for lib_container in docker_client.containers(all=True, filters=dict(status='created')):
            lib_labels = lib_container['Labels']
            if lib_labels.get(DATACOLLECTOR_TESTRUN_DOCKER_LABEL_ID) == testrun_id:
                docker_client.remove_container(lib_container['Id'], v=True, force=True)


if __name__ == '__main__':
    _main()
