import driver as meth


def list_all_structs():
    client, circ = meth.connect_mongo()
    data = circ.find({}, {'structures': 1})
    structs = []
    for d in data:
        structs.extend(d['structures'])
    client.close()

    structs = list(set(structs))
    structs.sort()
    return structs


def list_all_networks():
    client, circ = meth.connect_mongo()
    data = circ.find({}, {'name': 1})
    networks = []
    for d in data:
        networks.append(d['name'])
    client.close()

    networks.sort()
    return networks
