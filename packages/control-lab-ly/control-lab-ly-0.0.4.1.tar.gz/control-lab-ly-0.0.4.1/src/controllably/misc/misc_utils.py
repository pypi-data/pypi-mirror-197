# %% -*- coding: utf-8 -*-
"""
Created: Tue 2022/11/02 17:13:35
@author: Chang Jie

Notes / actionables:
-
"""
# Standard library imports
from datetime import datetime
import importlib
import json
import numpy as np
import os
import pandas as pd
from pathlib import Path
import pkgutil
from shutil import copytree
import time
import uuid

# Third party imports
import serial.tools.list_ports # pip install pyserial
import yaml # pip install pyyaml

# Local application imports
from . import decorators
print(f"Import: OK <{__name__}>")

here = str(Path(__file__).parent.absolute()).replace('\\', '/')

class Helper(object):
    """
    Helper class with miscellaneous methods
    """
    def __init__(self):
        self.safety_countdown = 3
        self.safety_mode = None
        pass
    
    # Static methods
    @staticmethod
    def create_folder(parent_folder:str = None, child_folder:str = None):
        """
        Check and create folder if it does not exist

        Args:
            parent_folder (str, optional): parent folder directory. Defaults to None.
            child_folder (str, optional): child folder directory. Defaults to None.
        """
        main_folder = datetime.now().strftime("%Y-%m-%d_%H%M")
        if parent_folder:
            main_folder = '/'.join([parent_folder, main_folder])
        folder = '/'.join([main_folder, child_folder]) if child_folder else main_folder
        if not os.path.exists(folder):
            os.makedirs(folder)
        return main_folder
    
    @staticmethod
    def get_class(module, dot_notation:str):
        """
        Retrieve the relevant class from the sub-package

        Args:
            module (module): sub-package
            dot_notation (str): dot notation of class / module / package

        Returns:
            class: relevant class
        """
        print('\n')
        top_package = __name__.split('.')[0]
        import_path = f'{top_package}.{module}.{dot_notation}'
        package = importlib.import_module('.'.join(import_path.split('.')[:-1]))
        _class = getattr(package, import_path.split('.')[-1])
        return _class
        
    @staticmethod
    def get_method_names(obj):
        """
        Get the names of the methods in object (class/instance)

        Args:
            obj (any): object of interest

        Returns:
            list: list of method names
        """
        method_list = []
        # attribute is a string representing the attribute name
        for attribute in dir(obj):
            # Get the attribute value
            attribute_value = getattr(obj, attribute)
            # Check that it is callable; Filter all dunder (__ prefix) methods
            if callable(attribute_value) and not attribute.startswith('__'):
                method_list.append(attribute)
        return method_list
    
    @staticmethod
    def get_node():
        """
        Display the machine's unique identifier

        Returns:
            str: machine unique identifier
        """
        return str(uuid.getnode())
    
    @staticmethod
    def get_ports():
        """
        Get available ports

        Returns:
            list: list of connected serial ports
        """
        com_ports = []
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            com_ports.append(str(port))
            print(f"{port}: {desc} [{hwid}]")
        if len(ports) == 0:
            print("No ports detected!")
            return ['']
        return com_ports
    
    @staticmethod
    def is_overrun(start_time:float, timeout:float):
        """
        Check whether the process has timed out

        Args:
            start_time (float): start time in seconds since epoch
            timeout (float): timeout duration

        Returns:
            bool: whether process has overrun
        """
        if timeout!=None and time.time() - start_time > timeout:
            return True
        return False
    
    @staticmethod
    def pretty_print_duration(total_time:float):
        """
        Display time duration (s) as HH:MM:SS text

        Args:
            total_time (float): duration in seconds

        Returns:
            str: formatted time string
        """
        m, s = divmod(total_time, 60)
        h, m = divmod(m, 60)
        return f'{int(h)}hr {int(m)}min {int(s):02}sec'
    
    @staticmethod
    def read_json(json_file:str, package:str = None):
        """
        Read JSON file

        Args:
            json_file (str): JSON filepath
            package (str, optional): name of package to look in. Defaults to None.

        Returns:
            dict: dictionary loaded from JSON file
        """
        if package is not None:
            jsn = pkgutil.get_data(package, json_file).decode('utf-8')
        else:
            with open(json_file) as file:
                jsn = file.read()
        return json.loads(jsn)
    
    @staticmethod
    def read_yaml(yaml_file:str, package:str = None):
        """
        Read YAML file

        Args:
            yaml_file (str): YAML filepath
            package (str, optional): name of package to look in. Defaults to None.

        Returns:
            dict: dictionary loaded from YAML file
        """
        if package is not None:
            yml = pkgutil.get_data(package, yaml_file).decode('utf-8')
        else:
            with open(yaml_file) as file:
                yml = file.read()
        return yaml.safe_load(yml)
    
    @staticmethod
    def zip_inputs(primary_keyword:str, **kwargs):
        """
        Checks and zips multiple keyword arguments of lists into dictionary

        Args:
            primary_keyword (str): primary keyword to be used as key

        Raises:
            Exception: Inputs have to be of the same length

        Returns:
            dict: dictionary of (primary keyword, kwargs)
        """
        input_length = len(kwargs[primary_keyword])
        keys = list(kwargs.keys())
        for key, value in kwargs.items():
            if type(value) != list:
                if type(value) in [tuple, set]:
                    kwargs[key] = list(value)
                else:
                    value = [value]
                    kwargs[key] = value * input_length
        if not all(len(kwargs[key]) == input_length for key in keys):
            raise Exception(f"Ensure the lengths of these inputs are the same: {', '.join(keys)}")
        kwargs_df = pd.DataFrame(kwargs)
        kwargs_df.set_index(primary_keyword, drop=False, inplace=True)
        return kwargs_df.to_dict('index')
    
    # Class methods
    @classmethod
    def get_details(cls, configs:dict, addresses:dict = {}):
        """
        Decode dictionary of configuration details to get np.ndarrays and tuples

        Args:
            configs (dict): dictionary of configuration details
            addresses (dict, optional): dictionary of registered addresses. Defaults to {}.

        Returns:
            dict: dictionary of configuration details
        """
        for name, details in configs.items():
            settings = details.get('settings', {})
            
            for key,value in settings.items():
                if key == 'component_config':
                    value = cls.get_details(value, addresses=addresses)
                if type(value) == str:
                    if key in ['cam_index', 'port'] and value.startswith('__'):
                        settings[key] = addresses.get(key, {}).get(settings[key], value)
                if type(value) == dict:
                    if "tuple" in value:
                        settings[key] = tuple(value['tuple'])
                    elif "array" in value:
                        settings[key] = np.array(value['array'])

            configs[name] = details
        return configs
    
    @classmethod
    def get_machine_addresses(cls, registry:dict):
        """
        Get the appropriate addresses for current machine

        Args:
            registry (str): dictionary of yaml file with com port addresses and camera ids

        Returns:
            dict: dictionary of com port addresses and camera ids for current machine
        """
        node_id = cls.get_node()
        addresses = registry.get('machine_id',{}).get(node_id,{})
        if len(addresses) == 0:
            print("\nAppend machine id and camera ids/port addresses to registry file")
            print(yaml.dump(registry))
            raise Exception(f"Machine not yet registered. (Current machine id: {node_id})")
        return addresses
    
    @classmethod
    def get_plans(cls, config_file:str, registry_file:str = None, package:str = None):
        """
        Read configuration file (yaml) and get details

        Args:
            config_file (str): filename of configuration file
            registry_file (str, optional): filename of registry file. Defaults to None.
            package (str, optional): name of package to look in. Defaults to None.

        Returns:
            dict: dictionary of configuration parameters
        """
        configs = cls.read_yaml(config_file, package)
        registry = cls.read_yaml(registry_file, package)
        addresses = cls.get_machine_addresses(registry=registry)
        configs = cls.get_details(configs, addresses=addresses)
        return configs
    
    @classmethod
    def load_components(cls, config:dict):
        """
        Load components of compound tools

        Args:
            config (dict): dictionary of configuration parameters

        Returns:
            dict: dictionary of component tools
        """
        components = {}
        for name, details in config.items():
            _module = details.get('module')
            if _module is None:
                continue
            _class = cls.get_class(_module, details.get('class', ''))
            settings = details.get('settings', {})
            components[name] = _class(**settings)
        return components
    
    # Instance methods
    def safety_measures(self, func):
        return decorators.safety_measures(mode=self.safety_mode, countdown=self.safety_countdown)(func=func)
    
    # NOTE: DEPRECATE
    @classmethod
    def display_ports(cls):
        """
        Get available ports

        Returns:
            list: list of connected serial ports
        """
        print("'display_ports' method to be deprecated. Use 'get_ports' instead.")
        return cls.get_ports()

HELPER = Helper() 
"""NOTE: importing HELPER gives the same instance of the 'Helper' class wherever you import it"""


class Logger(object):
    """
    Logger class with miscellaneous methods
    """
    def __init__(self):
        self.all_logs = []
        self.logs = {}
        pass
    
    # Instance methods
    def log_now(self, message:str, group=None):
        """
        Add log with timestamp

        Args:
            message (str): message to be logged
            group (str, optional): message group. Defaults to None.

        Returns:
            str: log message with timestamp
        """
        log = time.strftime("%H:%M:%S", time.localtime()) + ' >> ' + message
        self.all_logs.append(log)
        if group:
            if group not in self.logs.keys():
                self.logs[group] = []
            self.logs[group].append(message)
        return log

    def reset_logs(self):
        """
        Reset all logs
        """
        self.all_logs = []
        self.logs = {}
        return

    def save_logs(self, groups=[], folder=''):
        """
        Write logs into txt files

        Args:
            groups (list, optional): list of log messages. Defaults to [].
            folder (str, optional): folder to save to. Defaults to ''.
        """
        dst_folder = '/'.join([folder, 'logs'])
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)
        
        with open(f'{dst_folder}/activity_log.txt', 'w') as f:
            for line in self.all_logs:
                f.write(line + '\n')
        
        for group in groups:
            if group not in self.logs.keys():
                print(f"'{group}' not found in log groups!")
                continue
            with open(f'{dst_folder}/{group}_log.txt', 'w') as f:
                for line in self.logs[group]:
                    f.write(line + '\n')
        return

LOGGER = Logger() 
"""NOTE: importing LOGGER gives the same instance of the 'Logger' class wherever you import it"""


# Core functions
def create_configs():
    """
    Create new configs folder
    """
    cwd = os.getcwd().replace('\\', '/')
    src = f"{here}/templates/configs"
    dst = f"{cwd}/configs"
    if not os.path.exists(dst):
        print("Creating configs folder...\n")
        copytree(src=src, dst=dst)
        node_id = Helper.get_node()
        print(f"Current machine id: {node_id}")
    return

def create_setup(setup_name:str = None):
    """
    Create new setup folder

    Args:
        setup_name (str, optional): name of new setup. Defaults to None.
    """
    cwd = os.getcwd().replace('\\', '/')
    if setup_name is None:
        setup_num = 1
        while True:
            setup_name = f'Setup{str(setup_num).zfill(2)}'
            if not os.path.exists(f"{cwd}/configs/{setup_name}"):
                break
            setup_num += 1
    src = f"{here}/templates/setup"
    cfg = f"{cwd}/configs"
    dst = f"{cfg}/{setup_name}"
    if not os.path.exists(cfg):
        create_configs()
    if not os.path.exists(dst):
        print(f"Creating setup folder ({setup_name})...\n")
        copytree(src=src, dst=dst)
    return

@decorators.named_tuple_from_dict
def load_setup(config_file:str, registry_file:str = None):
    """
    Load and initialise setup

    Args:
        config_file (str): config filename
        registry_file (str, optional): registry filename. Defaults to None.

    Returns:
        dict: dictionary of loaded devices
    """
    config = Helper.get_plans(config_file=config_file, registry_file=registry_file)
    setup = Helper.load_components(config=config)
    shortcuts = config.get('SHORTCUTS',{})
    
    for key,value in shortcuts.items():
        parent, child = value.split('.')
        tool = setup.get(parent)
        if tool is None:
            print(f"Tool does not exist ({parent})")
            continue
        if 'components' not in tool.__dict__:
            print(f"Tool ({parent}) does not have components")
            continue
        setup[key] = tool.components.get(child)
    return setup

def load_deck(device, layout_file:str, get_absolute_filepath:bool = True):
    """
    Load the deck information from layout file

    Args:
        device (object): device object that has the deck attribute
        layout_file (str): layout file name
        get_absolute_filepath (bool, optional): whether to extend the filepaths defined in layout file to their absolute filepaths. Defaults to True.

    Returns:
        object: device with deck loaded
    """
    layout_dict = Helper.read_json(layout_file)
    if get_absolute_filepath:
        get_repo_name = True
        root = ''
        for slot in layout_dict['slots'].values():
            if get_repo_name:
                repo_name = slot.get('filepath','').replace('\\', '/').split('/')[0]
                root = layout_file.split(repo_name)[0]
                get_repo_name = False
            slot['filepath'] = f"{root}{slot['filepath']}"
    device.loadDeck(layout_dict=layout_dict)
    return device

def set_safety(safety_level:str = None, safety_countdown:int = 3):
    """
    Set safety level of session

    Args:
        safety_level (str): 'high' - pauses for input before every move action; 'low' - waits for safety timeout before every move action
        safety_countdown (int, optional): safety timeout in seconds. Defaults to 3.
    """
    safety_mode = None
    if safety_level == 'high':
        safety_mode = 'pause'
    elif safety_level == 'low':
        safety_mode = 'wait'
    HELPER.safety_mode = safety_mode
    HELPER.safety_countdown = safety_countdown
    return