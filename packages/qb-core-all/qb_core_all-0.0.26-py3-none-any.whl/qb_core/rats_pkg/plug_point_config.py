core_rats_plug_point_configuration = {
    "cook_persistence_plug_point": {
        "plugin": "qb_core.rats_pkg.cook.cook_persistence_core",
        "description": "provides a core persistence for cook entity",
        "pluggable": "cook_entity"  # python module that uses the plug point
    },
    # things to be added in the future
    # "menu_persistence_plug_point": {
    #     "plug_point": "menu_persistence",
    #     "plugin": "core_menu_persistence",
    #     "description": "provides a core persistence for menu entity",
    #     "pluggable": "menu_processor"
    # },
    # "cook_added_event_plug_point": {
    #     "plugin": "core_cook_added_event",
    #     "description": "provides a core persistence for menu entity",
    #     "pluggable": "cook_processor"
    # }
}
