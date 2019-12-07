import json
from neo4j import GraphDatabase
import driver as d


# Closeness Centrality pj 88
def closeness_centrality():
    driver = d.connect_neo4j()
    
    with driver.session() as session:
        result = session.run("MATCH ()-[r]-() return r;")
        # Get all the networks 
        networks = []
        values = result.values()
        for data in values:
            networks.append(data[0]['name'])
        networks = list(set(networks))
        
        # 
        sums = {}
        for i, net in enumerate(networks):
            qry = 'CALL algo.closeness.harmonic.stream("Structure", "{}") '.format(net)
            qry += 'YIELD nodeId, centrality '
            qry += 'RETURN nodeId, algo.getNodeById(nodeId).name, centrality ORDER BY centrality DESC'
            
            r = session.run(qry)
            vals = r.values()
            for v in vals:
                if i == 0:
                    sums[v[1]] = [v[2]]
                else:
                    sums[v[1]].append(v[2])
        for key in list(sums.keys()):
            total = sum(sums[key])
            print('{}: {:0.5f}'.format(key, total))
        # import ipdb; ipdb.set_trace()


def degree_centrality():
    driver = d.connect_neo4j()
    
    with driver.session() as session:
        result = session.run("MATCH (s:Structure) return s;")
        # Get all the networks 
        structs = []
        values = result.values()
        for data in values:
            structs.append(data[0]['name'])
        structs = list(set(structs))    
        # print(structs)
        
        degrees = []
        num_relations = session.run("MATCH ()-[r]-() return count(r)").values()[0][0]
        
        for s in structs:
            r = session.run("MATCH (s:Structure {name: $s})-[r]-() return count(r)", 
                            s=s)
            vals = r.values()
            deg = vals[0][0]
            # print('{}: {}, {}'.format(s, deg, num_relations))  # deg/num_relations))
            degrees.append([s, deg])

    degrees.sort(key=lambda x: x[1])
    for dd in degrees:
        print(dd[0], ": ", dd[1])
