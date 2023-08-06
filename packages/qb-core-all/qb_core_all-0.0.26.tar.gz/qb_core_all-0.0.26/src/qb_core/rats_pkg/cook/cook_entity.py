"""cook_entity.py"""
from qb_core.common.plugin.plugin_manager import PluginManager

"""
this provides cook service
basically all the functions related to cook are included here.
this is the pluggable class that invokes plug points 
"""


def add_cook(cook):
    # cook specific validations go here
    # example, are all fields correct?
    _get_cook_plugin().save_cook(cook)


def remove_cook(cook):
    # cook specific validations go here
    _get_cook_plugin().remove_cook(cook)


def _get_cook_plugin():
    """
    convinence method to get the plugin for this plug point
    :return:
    """
    # tip: don't save this in this class. when core initializes/imports this module
    # infrastructure code would not have had opportunity to override. this why it is
    # important to always go to plugin manager for the most current plugin
    return PluginManager.get_plugin("cook_persistence_plug_point")
