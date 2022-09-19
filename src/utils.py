# as of September 2022 it appears that some utils are better provided centrally to all grfs
# with utils repeated across 5 or so grfs, it's a tradeoff of
# 1. managing possible incompatibilities if the API changes to a util
# 2. managing drift, where the utils in each project are subtly different as changes made in one are not copied to the other
# although utils don't change often, the balance is tipped towards central provision, and updating projects for API changes when needed

def echo_message(*args, message_type=None):
    # use to raise messages from templates to standard out (can't print directly from template render)
    # magically wraps these messages in ANSI colour to make them visible - they are only intended for noticeable messages, not general output
    if message_type == "info":
        color = "\033[36m"  # cyan
    else:
        color = "\033[33m"  # yellow
    print(color + " ".join(args) + "\033[0m")
