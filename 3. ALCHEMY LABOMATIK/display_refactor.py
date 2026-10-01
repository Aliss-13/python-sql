from display_colors_and_rarities import COLORS, RESET


def group_data_under_same_id(items):

    groups = []
    current_item_id = None
    current_group = []

    for item in items:

        item_id = item[0]

        if current_item_id is None:
            current_item_id = item_id

        if current_item_id != item_id:
            groups.append(current_group)
            current_item_id = item_id
            current_group = []
        
        current_group.append((item))

    groups.append(current_group)

    return groups


def format_recipe_and_craft_items(item_list):

    item_text = ""  # on liste les items

    if not item_list:
        item_text = "Aucun"
                        
    else:
        for (item_name, item_quantity, item_color) in item_list:
            if item_text:
                item_text += " - "
            item_text += f"{COLORS[item_color]}{item_name}{RESET} x{item_quantity}"

    return item_text


def format_affinity_items(ac_list):

    ac_text = ""

    if not ac_list:
        ac_text = "Aucun"
                        
    else:
        for first, second in ac_list:
            if ac_text:
                ac_text += " - "
            ac_text += f"{first} {second}"

    return ac_text