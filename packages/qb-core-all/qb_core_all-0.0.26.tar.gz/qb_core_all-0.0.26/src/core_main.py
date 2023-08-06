"""
use this module to initialize the whole app

Note setuptools is not picking this up
probably because this module is directly off of src
"""
import qb_core.oproc_pkg.oproc
import qb_core.rats_pkg.rats
import qb_core.ocra_pkg.ocra
from qb_core.common.plugin.plugin_manager import PluginManager


def initialize_app():
    # since this involves importing, it's good to do this upfront
    # PluginManager.setup_plugins("cook_persistence_plug_point", "qb_core.rats_pkg.cook.cook_persistence_core")
    # empty override dictionary implies just use core plugins
    # PluginManager.override_plugins({})
    # print(f'{PluginManager.get_plugin("cook_persistence_plug_point")}')

    qb_core.rats_pkg.rats.initialize_module()
    qb_core.oproc_pkg.oproc.initialize_module()
    qb_core.ocra_pkg.ocra.initialize_module()


