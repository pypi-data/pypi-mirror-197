# Super Simple Plugin Manager - SSPM

## About SSPM

Super Simple Plugin Manager - SSPM is a library I created based off of Thibauld Nion's YAPSY. 
I liked how configurable YAPSY is and the inclusion of a configuration file to allow the plugin creator to include
details about their plugin. Unfortunately, I found that YAPSY had a lot of functionality that I didn't need, it is
out of date, and contains a lot of deprecated code. To address these issues I created SSPM. SSPM does not have the 
customization that yapsy has. However, it allows for much quicker implementation that I believe most people will 
find useful. It is meant to be a very simple hands-off plugin manager.

## Installation

The easiest way to install is to use pip:
	
	pip install SSPM

or if you have cloned the repo:
	
	cd <path to repo>
	pip install .

	or
	
	cd <path to repo>
	python setup.py install
	

## Basic Usage

1. Initialize the plugin manager

	``` shell
	plugin_manager = PluginManager(plugin_folder=\<INSERT PLUGINS DIR PATH HERE\>)
	```
	
2. Import the plugins in the plugins directory

	``` shell
	plugin_manager.import_plugins()
	```
 
3. Get the imported plugin

	```shell
	plugin = sspm.get_active_plugin("Plugin name")
	```
 
    or

    ```shell
    plugins = sspm.active_plugins
    ```
