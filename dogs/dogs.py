#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from ruamel.yaml import YAML
from dogs.droplet_manager import DropletManager

class DOGS:
  def __init__(self, config_path="config.yaml"):
      yaml = YAML()
      with open(config_path, 'r') as f:
          self.config = yaml.load(f)

  def get_droplet_manager(self, name: str) -> DropletManager:
      if name not in self.list_droplets():
          raise ValueError(f"Droplet '{name}' not found in config")
      return DropletManager(token=self.config['token'], droplet_name=name)

  def list_droplets(self):
      return [server['name'] for server in self.config["servers"]]
