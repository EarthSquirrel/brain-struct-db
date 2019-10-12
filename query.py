import driver as meth


def get_all_structs():
    client, circ = meth.connect_mongo()
    data = circ.find({}, {'structures': 1})
    structs = []
    for d in data:
        structs.extend(d['structures'])

    structs = list(set(structs))
    structs.sort()
    return structs
