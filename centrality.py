import json
from neo4j import GraphDatabase
import driver as d


# Closeness Centrality pj 88
def closeness_centrality():
    qry = "CALL algo.closeness.harmonic.stream('Structure', '')"
    qry += "yield nodeId, centrality "
    qry += "return algo.getNodeById(nodeId).name as structure, centrality "
    qry += "order by centrality desc"
    
    driver = d.connect_neo4j()
    vals = []
    with driver.session() as session:
        res = session.run(qry)
        vals = res.values()
        vals.reverse()  # Easier to see highest if at bottom in terminal
        for v in vals:
            print("{}: {:0.5f}".format(v[0], v[1]))
    driver.close()


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


def betweenness_centrality():
    qry = "CALL algo.betweenness.stream('Structure', '') "
    qry += "yield nodeId, centrality "
    qry += "return algo.getNodeById(nodeId).name as structure, centrality "
    qry += "order by centrality desc"
    
    driver = d.connect_neo4j()
    vals = []
    with driver.session() as session:
        res = session.run(qry)
        vals = res.values()
        for v in vals:
            print("{}: {:0.5f}".format(v[0], v[1]))


def pagerank():
    qry = "CALL algo.pageRank.stream('Structure', '', {iterations:20, dampingFactor:0.70}) "
    qry += "YIELD nodeId, score "
    qry += "RETURN algo.getNodeById(nodeId).name AS page, score "
    qry += "ORDER BY score DESC"

    driver = d.connect_neo4j()
    vals = []
    with driver.session() as session:
        res = session.run(qry)
        vals = res.values()
        vals.sort(key = lambda x: x[1])
        for v in vals:
            print("{}: {:0.5f}".format(v[0], v[1]))
