"""FDT Camera helpers."""


def to_dict(response):
    """Format response to dict."""
    if not isinstance(response, str):
        return

    # dict to return
    rdict = {}

    # remove single quotes and semi-collon characters
    response = response.replace('\'', '').replace(';', '')

    # eliminate 'var ' from response and create a list
    rlist = [l.split('var ', 1)[1] for l in response.splitlines()]

    # for each member of the list, remove the double quotes
    # and populate dictionary
    for item in rlist:
        key, value = item.replace('"', '').strip().split('=')
        rdict[key] = value

    return rdict
