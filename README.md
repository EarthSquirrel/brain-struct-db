# Brain Structure Database
This is a project for my advanced databases class. Information on brain networks, written in json files, is inserted into the database and a graph of connections between structures and networks is built. The idea is to look at which networks share common structures and if modification of said structures activity affects functionality of both networks. 

## Polyglot Persistence
This database uses both MongoDB and Neo4J to store data with MongoDB being the authoritative database. MongoDB stores more information on the brain networks such as name, structures, function, and citations. Neo4J only uses the name and structures to build a graph. 


## How to start?
1. Enter the brain structure information into a json file following the structure laid out in networks-structure.json. I put all my networks in networks.json
2. Run init\_dbs() (in the driver.py file) to clear out any existing data and create an index forcing brain networks to be unique.
3. Run json\_load\_dbs(‘networks.json’) with your json file name to insert data for the first time into both MongoDB and Neo4J. Both databases will simply pass over duplicate network information.
4. Run rebuild\_neo4j() to rebuild the graph in Neo4J from MongoDB.

## Example
Here is an example using the neuromodulatory systems, because they had higher connectivity than most networks did. More examples can be seen in example-networks. &nbsp; <br>
![](example-networks/neuromodulatory-systems.svg)

## Disclaimer
This is a very rough idea/draft for a course project. Most of the networks were entered by me skimming papers looking for structures to enter. For simplicity, I ignored if activity was increased or decreased as well as which hemisphere(s) activity was occurring in if they were given. There is no guarantee of accuracy. 
