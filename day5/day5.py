def main():
    with open("./day5/input") as file:
        lines = [line.rstrip() for line in file]
    
    # Split rules from page update orders
    rules = []
    page_update_orders = []
    still_rules = True

    for line in lines:
        # Blank line separates rules and page update orders
        if line is None or line == "":
            still_rules = False
            continue

        if still_rules:
            rules.append(line)
        else:
            page_update_orders.append(line)

    processed_rules = [rule.split("|") for rule in rules]
    process_page_update_orders = [page_update_order.split(",") for page_update_order in page_update_orders]
    sum = 0
    incorrectly_ordered_updates = []

    for process_page_update_order in process_page_update_orders:
        # Build index
        ordering_dict = {}
        for index, value in enumerate(process_page_update_order):
            ordering_dict[value] = index

        # Check if all rules apply else skip
        failed_rule = False
        for rule in processed_rules:
            if rule[0] in ordering_dict and rule[1] in ordering_dict and ordering_dict[rule[0]] > ordering_dict[rule[1]]:
                failed_rule = True
                break

        if failed_rule:
            incorrectly_ordered_updates.append(process_page_update_order)
            continue
        # Find middle
        middle = len(ordering_dict)//2
        middle_element = int(process_page_update_order[middle])

        # Add to sum
        sum += middle_element

    print(sum) # Part 1

    sum = 0
    # Re order updates to obey all rules
    while len(incorrectly_ordered_updates) > 0:
        incorrectly_ordered_update = incorrectly_ordered_updates.pop(0)

        # Build index
        ordering_dict = {}
        for index, value in enumerate(incorrectly_ordered_update):
            ordering_dict[value] = index

        failed_rule = False
        # Find the rule that it didn't obey
        for rule in processed_rules:
            if rule[0] in ordering_dict and rule[1] in ordering_dict and ordering_dict[rule[0]] > ordering_dict[rule[1]]:
                failed_rule = True
                break
        
        if failed_rule:
            # Swap the elements that failed to obey the rule to force the rule to be obeyed
            # Re-insert the inccorectly ordered update array for re-evaluation
            temp = incorrectly_ordered_update[ordering_dict[rule[0]]]
            incorrectly_ordered_update[ordering_dict[rule[0]]] = incorrectly_ordered_update[ordering_dict[rule[1]]]
            incorrectly_ordered_update[ordering_dict[rule[1]]] = temp
            incorrectly_ordered_updates.append(incorrectly_ordered_update)
            continue
        else:
            middle = len(incorrectly_ordered_update)//2
            middle_element = int(incorrectly_ordered_update[middle])
            sum += middle_element
    
    print(sum)
    

if __name__ == "__main__":
    main()
