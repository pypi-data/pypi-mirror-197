# Copyright 2021 StreamSets Inc.

import argparse
import getpass
import itertools
import logging
import os
import pathlib
from collections import namedtuple

import hvac

logger = logging.getLogger(__name__)

DEFAULT_VAULT_TOKEN_FILE = '/etc/testframework/vault_token'

# If a key starts with this it will be assumed to be an environmental variable and not an argument.
ENV_MARKER = 'env:'

# Reserved key to hold the element description.
DESCRIPTION_KEY = 'description'


class RunProfile:
    """Encapsulates a Run Profile loaded from an external source."""

    def __init__(self):
        self.args = []
        self.env = {}

    def add_argument(self, key, value):
        """
        Add an argument to the profile.

        Args:
            key (:obj:`str`): The argument key eg: '--something'.
            value (:obj:`str`): The argument value.
        """
        Arg = namedtuple('Arg', ['key', 'value'])
        self.args.append(Arg(key=key, value=value))

    def add_environment_variable(self, key, value):
        """
        Add an environmental variable to the profile.

        Args:
            key (:obj:`str`): The environmental variable name.
            value (:obj:`str`): The environmental variable value.
        """
        self.env[key] = value

    def merge(self, other):
        """
        Adds the content of another profile to this profile

        Args:
            other (:obj:`RunProfile`): The other profile whose content should be incorporated into this profile.
        """
        self.args.extend(other.args)
        self.env = {**self.env, **other.env}

    def has_content(self):
        """Returns true if this profile has any added state, false otherwise."""
        return bool(self.args or self.env)


class HashiCorpVaultProfileManager:
    """
    Retrieves run profiles from a KV v2 engine within a HashiCorp Vault instance.

    Args:
        url (:obj:`str`): The url used to connect to the Vault instance.
        secret_engine (:obj:`str`): The KV v2 secret engine containing the profile being retrieved.
        path_root (:obj:`str`): The root directory in the HashiCorp Vault secret engine containing all objects being
                                managed.
        token (:obj:`str`, optional): A HashiCorp Vault token used for authentication.
    """

    def __init__(self, url, secret_engine, path_root, token=None):
        self._secret_engine = secret_engine
        self._path_root = path_root

        client = hvac.Client(url=url, token=token)

        self._client = client

        # This cache will not attempt to handle evictions since it is only expected to live for as
        # long as it takes to retrieve the profiles (a minute or so).
        self._element_path_cache = []

    @property
    def element_root(self):
        """Returns the root path of all run elements."""
        return f'{self._path_root}/elements/'

    @property
    def profile_root(self):
        """Returns the root path of all run profiles."""
        return f'{self._path_root}/profiles/'

    def ldap_auth(self, username, password):
        """
        Authenticate using LDAP credentials.

        Args:
            username (:obj:`str`): Username used for authentication
            password (:obj:`str`): Password used for authentication
        """
        try:
            self._client.auth.ldap.login(username=username, password=password)
        except Exception as exception:
            raise ValueError('Caught exception while trying to authenticate with LDAP') from exception

    def okta_auth(self, username, password):
        """
        Authenticate using Okta credentials.

        Args:
            username (:obj:`str`): Username used for authentication
            password (:obj:`str`): Password used for authentication
        """
        try:
            self._client.auth.okta.login(username=username, password=password)
        except Exception as exception:
            raise ValueError('Caught exception while trying to authenticate with Okta') from exception

    def is_authenticated(self):
        """Returns whether or not the manager has successfully authethenticated with the server."""
        return self._client.is_authenticated()

    @property
    def token(self):
        """Returns the current authentication token if it exists."""
        return self._client.token

    def _filter_elements(self, filters=None):
        # Filters elements using globbing. The element paths start relative to `element_root`. If no `filters` are
        # provided all elements will be returned.
        #
        # Args:
        #     filters (list of :obj:`str`, optional): Filters used to narrow scope of returned elements.
        #
        # Returns:
        #     A (list of :obj:`str`) of the element paths matching `filters` such that each path is relative to
        #     `element_root`. Never `None`, possibly empty.

        if not self._element_path_cache:

            logger.debug('Building the cache for Hashicorp vault entries')

            # Unfortunately the list secrets API only returns the next level of secrets. If we want to support
            # globbing we will need to premptively crawl through all levels in order to build the paths. This can be
            # easily accomplished with a BFS traversal. We will cache the output so we can avoid duplicating the work
            # in the future and the large amount of IO that comes along with it.
            queue = ['/']
            all_secrets = []

            while queue:
                current = queue.pop(0)
                if current.endswith('/'):
                    response = self._client.secrets.kv.v2.list_secrets(path=self.element_root + current,
                                                                       mount_point=self._secret_engine)
                    contained_secrets = [current + key for key in response['data']['keys']]
                    queue.extend(contained_secrets)
                else:
                    # We will remove the leading slash to make the element names look nicer
                    all_secrets.append(current)

            # We want to sort the secrets to ensure the order stays stable during processing
            self._element_path_cache = sorted(all_secrets)
            logger.debug('Cache built for Hashicorp vault run elements')

        matched_secrets = []

        # Filter the cache and return all matching secrets making sure to not add a secret if its already been added
        if filters:
            for filter in filters:
                for secret in self._element_path_cache:
                    # Add leading slash to make matches act as full path matches and avoid matching the tailends
                    if secret not in matched_secrets and pathlib.PurePath(secret).match(f"/{filter}"):
                        matched_secrets.append(secret)
        else:
           # We are extending the list rather than setting it to protect the internal cache from mutation
           matched_secrets.extend(self._element_path_cache)

        # We will remove the leading slash to make the element names look nicer
        return [secret[1:] for secret in matched_secrets]

    def list_elements(self, filters=None):
        """
        Returns a list of run elements and optionally filters them to those that match a globbed path.

        Args:
            filters (:list:`str`, optional): A list of filters used to limit what elements are returned. A filter is
                                             essentially just a path with support for globbing syntax. If `None` then
                                             all elements will be returned.

        Returns:
            A list of 2-tuples (:obj:`tuple`) where the first object in the tuple is the element name (:obj:`string`)
            and the second object in the tuple is the element description (:obj:`string`). The order of the list is
            the order of which the elements were found. Never `None`, possibly empty.
        """
        matched_secrets = self._filter_elements(filters)
        element_list = []
        for secret in matched_secrets:
            response = self._client.secrets.kv.v2.read_secret_version(path=self.element_root + secret,
                                                                      mount_point=self._secret_engine)
            element = response['data']['data']
            element_list.append((secret, element.get(DESCRIPTION_KEY, '')))
        return element_list

    def load_elements(self, filters):
        """
        Loads all run element values that match the provided filters and merges them into single view.

        Args:
            filters (:list:`str`): A list of filters used to limit what elements are processed. A filter is
                                   essentially just a path with support for globbing syntax. Cannot be `None` or empty.

        Returns:
            A run profile (:obj:`RunProfile`) containing the content.

        """
        # Extremely unlikely that a user will want to load every element since elements can very easily
        # invalidate each other so we will assume that that is a programming error
        if not filters:
            raise ValueError('filters cannot be `None` or empty')

        matched_secrets = self._filter_elements(filters)

        profile = RunProfile()

        for secret in matched_secrets:
            logger.debug('Loading run element %s', secret)
            response = self._client.secrets.kv.v2.read_secret_version(path=self.element_root + secret,
                                                                      mount_point=self._secret_engine)
            element = response['data']['data']

            for key, value in element.items():
                if key == DESCRIPTION_KEY:
                    continue
                elif key.startswith(ENV_MARKER):
                    env_var = key[len(ENV_MARKER):].strip()
                    profile.add_environment_variable(env_var, value.strip())
                else:
                    profile.add_argument(key.strip(), value.strip())

        return profile

    def list_profiles(self):
        """
        Returns the definitions of the profiles available

        Returns:
            A (:obj:`dict`) such that each key is a profile name and and the corresponding vaule is a
            (:obj:`namedtuple`) where the `elements` attribute contains the list of elements contained within the
            profile and the `description` attribute contains a human readable description of the purpose of the profile.
        """
        response = self._client.secrets.kv.v2.list_secrets(path=self.profile_root,
                                                           mount_point=self._secret_engine)
        content = response['data']['keys']

        profiles = {}
        for profile_name in content:
            profile = self.get_profile_definition(profile_name)
            profiles[profile_name] = profile

        return profiles

    def get_profile_definition(self, profile_name):
        """
        Returns the profile's definition.

        Args:
            profile_name (:obj:`str`): The name of the desired profile. For example: 'AWS'

        Returns:
            A namedtuple (:obj:`namedtuple`) such that the `elements` attribute contains the list of elements contained
            within the profile and the `description` attribute contains a human readable description of the purpose of
            the profile.
        """
        logger.debug('Getting run profile definition of %s', profile_name)
        response = self._client.secrets.kv.v2.read_secret_version(path=self.profile_root + profile_name,
                                                                  mount_point=self._secret_engine)
        profile = response['data']['data']
        description = profile.get(DESCRIPTION_KEY, '')
        elements = profile.get('elements', '').split(',')
        ProfileDefintion = namedtuple('ProfileDefintion', ['elements', 'description'])
        return ProfileDefintion(elements=elements, description=description)

    def load_profiles(self, profile_names):
        """
        Loads all run profile values for the profiles provided and merges them into single view.

        Args:
            profile_names (:list:`str`): A list of profile names being loaded.

        Returns:
            A run profile (:obj:`RunProfile`) containing the content.
        """
        run_profile = RunProfile()
        for profile_name in profile_names:
            logger.debug('Loading run profile %s', profile_name)
            profile_def = self.get_profile_definition(profile_name)
            new_profile = self.load_elements(profile_def.elements)
            run_profile.merge(new_profile)
        return run_profile


def create_run_profile_manager(vault_url, secret_engine, path_root):
    """
    Creates and returns an authenticated profile manager. Will first attempt to authenticate with Vault using an
    existing token on the machine in either the file system or environment. If that fails it prompts to ask for Okta
    credentials and will then try to generate a token and save said token to disk for future use.


    Args:
        vault_url (:obj:`str`): The URL used to connect to the Vault instance.
        secret_engine (:obj:`str`): The secret engine containing the profiles being managed.
        path_root (:obj:`str`): The root directory of all objects being managed.

    Returns:
        A :py:obj:`HashiCorpVaultProfileManager` who has successfully authenticated with the provided Vault instance.
    """

    # We will start looking for a authentication token for vault
    vault_token = None

    # Check for a previously saved token
    if os.path.isfile(DEFAULT_VAULT_TOKEN_FILE):
        logger.debug('Loading Vault authentication token from %s', DEFAULT_VAULT_TOKEN_FILE)
        with open(DEFAULT_VAULT_TOKEN_FILE) as file:
            vault_token = file.readline().rstrip()

    manager = HashiCorpVaultProfileManager(vault_url,
                                           secret_engine,
                                           path_root,
                                           token=vault_token)

    if not manager.is_authenticated():
        while True:
            username = input('Okta Username: ')
            password = getpass.getpass('Okta Password: ')
            print("You may need to check your MFA device")
            try:
                manager.okta_auth(username, password)

                vault_token = manager.token
                logger.debug('Vault token successfully created. Saving to %s for future use',
                             DEFAULT_VAULT_TOKEN_FILE)
                with open(DEFAULT_VAULT_TOKEN_FILE, 'w') as file:
                    file.write(vault_token)
                break
            except Exception as excp:
                print(f'Login failed. Please try again: {excp}')
    return manager
