def create_python_function(tags):
    code = ""

    if ("=", "ASSIGN") in tags:
        tag = tags.index(("=", "ASSIGN"))
        tags = tags[tag+1:]

    for tag in tags:

        if tag[1] == "ID":
            code += 'player["' + tag[0] + '"]'
        else:
            code += tag[0]

    return code

