# 11-26-19
* Installed Neo4J on a Mac and got the graph algorithm package working. (brew install neo4j)
* [Github page with install instructions](https://github.com/neo4j-contrib/neo4j-graph-algorithms)
* [Website I downloaded graph algorithm package from](https://neo4j.com/download-center/)

# 12-5-19
#### TODO
* Test Neo4j graph commands
* Write methods to execute them (?)
* Write out requirenments
* PUT CONFIG FILES ONTO MAC!!!!
* Figure out how to get mongodb working....


###### Installed MongoDB
* [Brew tap tutorial](https://github.com/mongodb/homebrew-brew)
* FAILED

# 12-6-19
## Chapter 5: Centrality Algorithms
* help understand roles of specific nodesin graph and impact on network
* identify most important nodes 
* identify network dynamics
	* credibility, accesbility, speed of spreading, bridges between groups
* Summaries
	* **Degree Centrality** baseline metric of connectedness
		* Measure number of relationships a node has
	* **Closeness Centrality** measuring how central a node is the the group
		* Calculate which nodes have the shortest paths to all other nodes
	* ** Betweenness Centrality** Finding control points
		* Measure number of shortest paths that pass through a node
	* **PageRank** Understand overall influence
		* Estimate a current node's importance from its lnked neighbors and their neighbors
* **If you use the wrong algorithm, you may get bad results**
	* Think about what you want to accomplish

### Degree Centrality
* Calculates incoming and outgoing degree of nodes
* Determines popularity

#### Reach 
* How many other nodes it touches
* More nodes it touches the more it can influence other things
* **average degree**: total number relationships/total number of nodes
	* skewed when some nodes have really high degrees
* **degree distribution**: probability a randomly selected node will have a certain number of relationships
* Two measures used to catagorize **scale-free networks** and **small-world networks**
	* TODO: scale-free networks:
	* TODO: small-world networks:

#### When Should I Use Degree Centrality?
* Analyze influence or popularity of individual nodes
* immediate connectedness or near-term probabilities (?)
* global analysis: minimum degree, max degree, mean degree, standard deviation accross whole graph
* Examples:
	* 

##### Tips
* dense nodes with lots of relationships don't add much additional info, increase computational comlexity, may want to remove from computation

##### Ideas for Neuroscience questions
* How many connections does a structure have on average?
* Which structure has the most connectsions? the least?
* Which structure participates in the most networks?

### Closeness Centrality
* Detect nodes that can effectivly spread information through a subgraph



## Chapter 2: Nodes and Edges
### 2.2 Mesoscale Connectomics



## Chapter 5: Centrality and Hubs
### 5.1 Centrality
* Different measures capture different aspects of what it means to be "central" in a network
* Most measures arrive at same conclusion when network is star-like (hub and spoke) networks
	* Central node will be identified as having the highest centrality
#### 5.1.1 Degree-Based Measure of Centrality
* Limitation: Doesn't take importance of neighbors into account
* PageRank
	* 

#### 5.1.5 Characterizing Centrality in Brain Networks
* some centrality measures make assumptions about how signals travel through network
	* Ex: Betweenness centrality assumes singals take shortest path
* Borgatti (2005) two different ways to classify information flow
	1. How information flows between nodes
		* Serial transfer
		* Serial duplication
		* Parallel duplication
		* Parallel transfer (diffusion)
	2. trajectory information follows
		* Shortest path
		* path < trail < walk
* Where do nervous systems fit withing this classification scheme?
	* parallel transfer (diffusion)
	* modeled as trail or walk
	* Neurons fire to multiple neighbors, then return to resting state
* What does parallel transfer model tell us about how to measure centrality in brain networks?
	* Degree centrality: characterize imediate affect node has on others
	* Closeness centrality: high values affect lots of other neurons in a shorter amount of time
	* PageRank: global spread of event, nodes more closely connected to other central nodes will be able to spread information to more nodes faster
	* 
	
	
	
# 
* [Neo4j 6.4](https://neo4j.com/docs/cypher-manual/current/query-tuning/cypher-index-values-order/) said that creating an index can reduce the number of dbHits, but it did not work for what I am doing. It was still 139 total hits.
* The number of db hits changes when I get rid of the algo.getNodeById() method. It goes to 1 in the first call. I think all the algorithms have the same execution plan, because they are all in the same structure. This means I probably need to look at the algorithm itself to figure out which one to best use?
* FUTURE: PageRank measures nodes with more incoming nodes as more important, maybe do the networks as nodes one too?
* Lowered PageRank dampening factor to 70%, because brain networks are more local than farther away
* Information I want to use to score:
	* Local analysis vs more global analysis
		* Degree centrality vs. PageRank
		* 
	* Information flow
		* 
	* Runtime
		* 
	* Accuracy
		* Betweenness would have lower real world accuracy, because it assumes shortest path and that is not always true
		* PageRank would have lower accuracy, because it may not always converge
	* 
	
* Characteristics of the algorithms I can use in picking which to run:
	* Degree Centrality
		* 
	* Closeness Centrality
		* 
	* Betweenness Centrality
		* 
	* PageRank
		* 





#### Cypher code
**Degree Centrality**


**Closeness Centrality**
'''
CALL algo.closeness.harmonic.stream("Structure", "")
yield nodeId, centrality
return algo.getNodeById(nodeId).name as structure, centrality
order by centrality desc
'''

**Betweenness Centrality**
'''
CALL algo.betweenness.stream("Structure", "")
yield nodeId, centrality
return algo.getNodeById(nodeId).name as structure, centrality
order by centrality desc
'''

**PageRank**