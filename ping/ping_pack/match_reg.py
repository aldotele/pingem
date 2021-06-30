import re


def is_regex(input_str):
    try:
        re.compile(input_str)
        return True
    except re.error:
        return False


def is_matching(regexp, content):
    out = re.search(regexp, content)
    return out


if __name__ == '__main__':

    test = 'The rain in Spain'
    pattern = re.compile("^([A-Z][0-9]+)+$")
    #print(pattern.match(test))

    x = re.search("^The.*Spain$", test)
    #print(x)


    y = re.search("[arn]", test)
    #print(y)

    print(re.search("[", "ciao"))

    try:
        re.compile('[a]')
        is_valid = True
    except re.error:
        is_valid = False
    #print(is_valid)