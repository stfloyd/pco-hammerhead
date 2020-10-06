import os
from logging import getLogger
from argparse import ArgumentParser
import json
import time

import pypco

from webbot import Browser

from app import settings, logging
from app.cli import cli


logger = logging.get_logger(__name__)


def init(args):
    # If the config directory doesn't exist, create it.
    if not os.path.exists(settings.CONFIG_DIR):
        logger.warning(f'Config directory does not exist at: {settings.CONFIG_DIR}')
        try:
            os.makedirs(settings.CONFIG_DIR)
            logger.success('Created config directory')
        except IOError as ioe:
            logger.error(ioe)
            logger.failure('Unable to create config directory')
            raise ioe

    # If the config file doesn't exist, write the default config to it.
    if not os.path.exists(settings.CONFIG_FILE):
        logger.warning(f'Default config file does not exist at: {settings.CONFIG_FILE_PATH}')
        try:
            with open(settings.CONFIG_FILE, 'w+') as config_file:
                json.dump(settings.DEFAULT_CONFIG, config_file)
            logger.success('Created default config file')
        except IOError as ioe:
            logger.error(ioe)
            logger.failure('Unable to create default config file')
            raise ioe

    logger.success('App initialized')
    
    return True


def load_config(args):
    '''
    Load app configuration from JSON file.
    If JSON file cannot be found, it will return the default configuration
    from settings.py.
    '''

    config_path = args.config

    try:
        logger.info(f'Loading configuration from file: {config_path}')
        with open(config_path) as config_file:
            # Attempt to open the configuration file if it exists.
            config = json.load(config_file)
        logger.success('Configuration loaded')
    except (IOError, OSError) as e:
        # Configuration file does not exist, use default config.

        logger.failure(f'Failed to load configuration from file')

        # See if it's in config directory if that wasn't already specified.
        appended_path = os.path.join('config/', config_path)
        try:
            logger.info(f'Attempt #2: Loading configuration from file: {appended_path}')
            with open(appended_path) as config_file:
                config = json.load(config_file)
            logger.success('Configuration loaded')
        except (IOError, OSError) as e2:
            logger.error(e)
            logger.error(e2)
            logger.info(f'Using default configuration')
            config = settings.DEFAULT_CONFIG
    
    logger.debug(f'Configuration: {config}')
    return config


def process(args, config):
    # Get PCO API credentials.
    pco = pypco.PCO(
        config['pco_app_id'],
        config['pco_secret']
    )

    pco_username = config['pco_username']
    pco_password = config['pco_password']

    tag_groups = [
        (tg['data']['id'], tg['data']['attributes']['name']) for tg in list(pco.iterate('/groups/v2/tag_groups?per_page=100'))
    ]

    group_types = [
        (gt['data']['id'], gt['data']['attributes']['name']) for gt in list(pco.iterate('/groups/v2/group_types?per_page=100'))
    ]

    print('Group Types:')
    for i, gt in enumerate(group_types):
        print('\t', i, gt[1])
    
    gt_input = _validate_input(
        input(f'Please select a group type [0-{len(group_types) - 1}]: '),
        group_types
    )

    if gt_input is None:
        logger.error('Invalid input, must be type int and within bounds.')
        return -1
    
    gt_id = group_types[gt_input][0]
    
    groups = [
        [g['data']['id'], g['data']['attributes']['name']] for g in pco.iterate(f'/groups/v2/group_types/{gt_id}/groups')
    ]

    for i, g in enumerate(groups):
        tags = [t['data']['id'] for t in pco.iterate(f"/groups/v2/groups/{g[0]}/tags")]
        groups[i].append(tags)

    print('Tag Groups:')
    for i, gt in enumerate(tag_groups):
        print('\t', i, gt[1])
    
    tg_input = _validate_input(
        input(f'Please select a tag group [0-{len(tag_groups) - 1}]: '),
        tag_groups
    )

    if tg_input is None:
        logger.error('Invalid input, must be type int and within bounds.')
        return -1
    
    tg_id = tag_groups[tg_input][0]
    
    tags = [
        (t['data']['id'], t['data']['attributes']['name']) for t in list(pco.iterate(f'/groups/v2/tag_groups/{tg_id}/tags'))
    ]

    print('Tags:')
    for i, t in enumerate(tags):
        print('\t', i, t[1])
    
    t_input = _validate_input(
        input(f'Please select a tag [0-{len(tags) - 1}]: '),
        tags
    )

    if t_input is None:
        logger.error('Invalid input, must be type int and within bounds.')
        return -1
    
    _automate_browser_operation(config['pco_username'], config['pco_password'], groups, tags[t_input])

    logger.success('App finished processing')

    # Return successfully
    return os.EX_OK


def _validate_input(input, reference):
    try:
        input_int = int(input)
        if input_int < len(reference):
            return input_int
        else:
            return None
    except ValueError:
        return None


def _automate_browser_operation(pco_username, pco_password, groups, tag):
    web = Browser()
    web.go_to('https://login.planningcenteronline.com/login/new')
    web.type(pco_username, id='email')
    web.type(pco_password, id='password')
    web.press(web.Key.ENTER)

    for g in groups:
        if len(g[2]) > 0:
            skip_group = False
            for t in g[2]:
                if t == tag[0]:
                    skip_group = True
                    break
            if skip_group: continue

        web.go_to(f'https://groups.planningcenteronline.com/groups/{g[0]}/settings')
        time.sleep(2.0)
        web.click('Add tags', tag='span')
        web.click(tag[1], tag='label', classname='checkbox-label')
        time.sleep(3.0)
