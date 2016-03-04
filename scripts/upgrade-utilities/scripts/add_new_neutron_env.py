#!/usr/bin/env python
# Copyright 2016, Rackspace US, Inc.
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
import os
import yaml


def add_new_dict_data(original, new):
    """
    Adds new key/value entries to existing dictionaries, and appends
    new leaf values.
    """

    if not hasattr(new, 'items'):
        return

    for key, new_values in new.items():

        # Add our whole sub-dictionary into the tree
        if key not in original:
            original[key] = new_values
            return

        # Only populate missing values
        for val in new_values:
            if val not in original[key]:
                original[key].append(val)

        add_new_dict_data(original[key], new[key])

if __name__ == '__main__':

    # Calculate the repository root based on the script's location
    script_path = os.path.abspath(__file__)
    script_rel_path = os.path.relpath(__file__)
    # Removing the relative path's length from the end of the absolute path
    # gives us the root.
    root = script_path[:-len(script_rel_path)]

    kilo_file = '/etc/openstack_deploy.KILO/env.d/neutron.yml'
    liberty_file = os.path.join(root, 'etc/openstack_deploy/env.d/neutron.yml')
    flag_file = '/etc/openstack_deploy.KILO/NEUTRON_MIGRATED'

    with open(kilo_file, 'r') as f:
        kilo_dict = yaml.safe_load(f.read())

    with open(liberty_file, 'r') as f:
        liberty_dict = yaml.safe_load(f.read())

    for skel in ('component_skel', 'container_skel', 'physical_skel'):
        add_new_dict_data(kilo_dict[skel], liberty_dict[skel])

    with open(liberty_file, 'w') as f:
        f.write(yaml.safe_dump(kilo_dict, default_flow_style=False,
                               width=1000))

    with open(flag_file, 'w') as f:
        f.write('Neutron variables migrated from kilo to liberty.')