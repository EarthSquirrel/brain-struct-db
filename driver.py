# Uses conda brain-struct-db
from pymongo import MongoClient, TEXT as mongoText
from pymongo.errors import DuplicateKeyError
import json
from neo4j import GraphDatabase
import re
import centrality as center


def load_json(file_name):
    with open(file_name) as json_file:
        content = json.load(json_file)

    # print(content)
    print("Read in json file with {} enteries.".format(len(content)))

    return content


#########################################################
#################### MongoDB Methods ####################
#########################################################
# connect to mongodb
def connect_mongo():
    client = MongoClient('localhost', 27017)
    # client = MongoClient('mongodb://localhost:27017')

    # will automaticaly create if doesn't exist
    db = client['circuitsDB']

    circuits = db.circuits

    return client, circuits


# insert single entry into mongodb
def insert_mongo(collection, data):
    # standardize punctuation
    split = re.split('_|-| ', data['name'].lower())
    data['name'] = ' '.join([x.capitalize() for x in split])
    structs = data['structures']
    new_structs = []
    for s in structs:
        s = s.lower()
        new_structs.append(' '.join([x.capitalize() for x in s.split(' ')]))
    data['structures'] = new_structs

    # create key
    first, *rest = re.split('_| |-|,', data['name'])
    data['key'] = first + ''.join(word.capitalize() for word in rest)
    try:
        result = collection.insert_one(data)
        print('Inserted: {} (id:{})'.format(data['name'], result.inserted_id))
    except DuplicateKeyError:
        print('Failed to insert {}: already exists.'.format(data['name']))


# ########################################################
# ##################### Neo4j Methods ####################
# ########################################################

# Load things into both db first time from json file
def connect_neo4j():
    uri = "bolt://127.0.0.1:7687"
    # uri = "bolt://localhost:7687"
    # uri = "bolt://localhost:7474"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
    return driver


def create_neo4j_struct(tx, struct):
    tx.run("MERGE (s:Structure {name: $struct});", struct=struct)
    # import ipdb; ipdb.set_trace()

def create_neo4j_network(tx, network):
    tx.run("MERGE (n:Network {name: $network});", network=network)


def create_network_relation(tx, struct, network):
    tx.run("MATCH (s: Structure {name: $struct}), (n:Network {name: $network})"
           "MERGE (s)-[r:part_of]->(n);", struct=struct, network=network)


def load_dict_neo4j_networks(driver, dic):
    structures = dic['structures']
    name = dic['name'].lower()
    print('Entering {} into Neo4j'.format(network))
    with driver.session() as session:
        session.write_transaction(create_neo4j_network, name)
        for struct in structures:
            struct = struct.lower()
            session.write_transaction(create_neo4j_struct, struct)
            session.write_transaction(create_network_relation, struct, name)
    print('\tEntered in {} structures.'.format(len(structures)))


# #####################################################
# Create connected structure graph with networks as relatons
# def create_neo4j_struct(tx, struct)


# Relates two structues using an arrow with netowork name
# SOooo many relations
def add_struct_relation(tx, struct1, struct2, network):
    # Code in addition part
    network = '_'.join(network.split(' '))
    network = '_'.join(network.split('-'))
    network = '_'.join(network.split('/'))
    qry = "MATCH (s1:Structure {name: $struct1}), (s2:Structure "
    qry += "{name: $struct2}) "
    qry += "MERGE (s1)-[r:{}".format(network)
    qry += "{name: $network}]->(s2);"
    tx.run(qry, struct1=struct1, struct2=struct2, network=network)
    


def load_dict_neo4j(driver, dic):
    structures = dic['structures']
    network = dic['name'].lower()
    print('Entering {} into Neo4j'.format(network))
    with driver.session() as session:
        for struct in structures:
            struct = struct.lower()
            session.write_transaction(create_neo4j_struct, struct)
            # session.write_transaction(create_network_relation, struct, network)
        # Connect all structures to each other with edge
        # labeled the network
        for struct in structures:
            struct = struct.lower()
            s2 = structures.copy()
            s2.remove(struct)
            for struct2 in s2:
                struct2 = struct2.lower()
                session.write_transaction(add_struct_relation, 
                                          struct, struct2, network)
                temp = struct
                struct2 = struct
                struct = temp
                session.write_transaction(add_struct_relation, 
                                          struct, struct2, network)

    print('\tEntered in {} structures.'.format(len(structures)))


def json_load_dbs(json_file):
    data = load_json(json_file)
    client, collection = connect_mongo()
    driver = connect_neo4j()
    for net in data:
        insert_mongo(collection, net)
        load_dict_neo4j(driver, net)
    driver.close()
    client.close()


def load_mongo_values(name, structs, citations, alieses=[], function="",
                      other=[]):
    # Create a dictionary
    data = {'name': name, 'structures': structs, 'citations': citations}
    if len(alieses) > 0:
        data['alieses'] = alieses
    if len(function) > 0:
        data['function'] = function
    if len(other) > 0:
        data['other'] = other

    # Do database inserting things
    client, collection = connect_mongo()
    driver = connect_neo4j()
    insert_mongo(collection, data)
    load_dict_neo4j(driver, data)
    driver.close()
    client.close()


def clear_mongo():
    client, circ = connect_mongo()
    circ.drop()
    circ.create_index([('key', mongoText)], unique=True)
    client.close()


def clear_neo4j():
    driver = connect_neo4j()
    with driver.session() as session:
        session.run("MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n, r;")
    driver.close()


# Clear both databases and set constraints on mongo unique
def init_dbs():
    # clear_mongo()
    clear_neo4j()


def rebuild_neo4j():
    client, circ = connect_mongo()
    driver = connect_neo4j()
    for c in circ.find({}, {"name": 1, "structures": 1}):
        load_dict_neo4j(driver, c)
    client.close()
    driver.close()


if __name__ == '__main__':
    # Clear the databases
    init_dbs()
    # load_json_mongo('networks.json')
    
    # Load database with data
    driver = connect_neo4j()
    for data in load_json('networks.json'):
        load_dict_neo4j(driver, data)
    driver.close()
    
    center.pagerank()
    center.betweenness_centrality()
    center.degree_centrality()
    center.closeness_centrality()
