# Uses conda brain-struct-db
from pymongo import MongoClient, TEXT as mongoText
from pymongo.errors import DuplicateKeyError
import json
from neo4j import GraphDatabase
import re


def load_json(file_name):
    with open(file_name) as json_file:
        content = json.load(json_file)

    # print(content)
    print("Read in json file with {} enteries.".format(len(content)))

    return content


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
    # create key
    first, *rest = re.split('_| |-|,|', data['name'])
    data['key'] = first + ''.join(word.capitalize() for word in rest)
    try:
        result = collection.insert_one(data)
        print('Inserted: {} (id:{})'.format(data['name'], result.inserted_id))
    except DuplicateKeyError:
        print('Failed to insert {}: already exists.'.format(data['name']))


# Load things into both db first time from json file
def connect_neo4j():
    uri = "bolt://localhost:7687"
    # uri = "bolt://localhost:7474"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
    return driver


def create_neo4j_struct(tx, struct):
    tx.run("MERGE (s:Structure {name: $struct});", struct=struct)


def create_neo4j_network(tx, network):
    tx.run("MERGE (n:Network {name: $network});", network=network)


def create_network_relation(tx, struct, network):
    tx.run("MATCH (s: Structure {name: $struct}), (n:Network {name: $network})"
           "MERGE (s)-[r:part_of]->(n);", struct=struct, network=network)


# Relates two structues using an arrow with netowork name
# SOooo many relations
def add_struct_relation(tx, struct1, struct2, network):
    qry = "MATCH (s1:Structure {name: $struct1}), (s2:Structure "
    qry += "{name: $struct2}) "
    qry += "MERGE (s1)-[r:{}]->(s2);".format(network)
    """
    tx.run("MATCH (s1:Structure {name: $struct1}), (s2:Structure "
           "{name: $struct2}) CREATE (s1)-[r:$network]->(s2);",
           struct1 = struct1, struct2 = struct2, network = network)
    """

    """
    # Code in addition part
    name = '_'.join(dic['name'].split(' '))
    name = '_'.join(name.split('-'))
    for i, struct1 in enumerate(structures):
        for j in range(i+1, len(structures)):
            # print('{} {} {}'.format(struct1, structures[j], name))
            session.write_transaction(add_struct_relation, struct1,
                                      structures[j], name)
    """
    tx.run(qry, struct1=struct1, struct2=struct2)


def load_dict_neo4j(driver, dic):
    structures = dic['structures']
    name = dic['name'].lower()
    print('Entering {} into Neo4j'.format(name))
    with driver.session() as session:
        session.write_transaction(create_neo4j_network, name)
        for struct in structures:
            struct = struct.lower()
            session.write_transaction(create_neo4j_struct, struct)
            session.write_transaction(create_network_relation, struct, name)
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


def clear_mongo():
    client, circ = connect_mongo()
    circ.drop()
    circ.create_index([('key', mongoText)], unique=True)
    client.close()


def clear_neo4j():
    driver = connect_neo4j()
    with driver.session() as session:
        session.run("MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n, r;")


# Clear both databases and set constraints on mongo unique
def init_dbs():
    clear_mongo()
    clear_neo4j()


if __name__ == '__main__':
    # load_json_mongo('networks.json')
    for data in load_json('networks.json'):
        load_dict_neo4j(data)
