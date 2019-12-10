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
* Can I use the information in neuroscience graph book to come up with more parameters to run query optimization on?
	
# 12-7-19
* [Neo4j 6.4](https://neo4j.com/docs/cypher-manual/current/query-tuning/cypher-index-values-order/) said that creating an index can reduce the number of dbHits, but it did not work for what I am doing. It was still 139 total hits.
* The number of db hits changes when I get rid of the algo.getNodeById() method. It goes to 1 in the first call. I think all the algorithms have the same execution plan, because they are all in the same structure. This means I probably need to look at the algorithm itself to figure out which one to best use?
* FUTURE: PageRank measures nodes with more incoming nodes as more important, maybe do the networks as nodes one too?
* Lowered PageRank dampening factor to 70%, because brain networks are more local than farther away
* Information I want to use to score:
	* Local analysis vs more global analysis
		* Degree centrality vs. PageRank (highest, because walk/longer paths)
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

# 12-7-19
#### TODO
* Score algorithms according to parameters
* Make table of score reasons
* Make presentation
* Write outline draft thing of paper
* Runthrough of presentation



* [Time complexities](http://igraph.wikidot.com/algorithm-space-time-complexity) for centrality algorithms in a different program
	* Shortest Path (unweighted): O(n^2 + nm)
		* BFS O(n+m) n times
	* Degree Centrality: O(n + 2m)
		* Must visit n nodes and count the number of edges around them suming to m edges, but all edges are connected to 2 nodes, so 2m
	* Closeness Centrality: O(nm)
		* How are these less than the shortest path if they must calculate shortest paths???
	* Betweenness Centrality: O(nm)
		* [Runtime of Brande's algorithm](https://en.wikipedia.org/wiki/Betweenness_centrality)
		* [Sampled version algorithm used](https://neo4j.com/docs/graph-algorithms/current/labs-algorithms/betweenness-centrality/) 
	* PageRank: ?????????? O(itter(n+2m))
		* It must calculate the value for each node and to do that it must sum up the edges around the node, therefore 2m
		* It must do this for every node n for an some number of itterations
		* [Information about PageRank](https://cklixx.people.wm.edu/teaching/math410/google-pagerank.pdf)
* [Execution Plan Information](https://neo4j.com/docs/operations-manual/3.5/performance/statistics-execution-plans/)
#### Parameter Classification
**Speed:** Measured based on how fast an algoirthm preforms. Fastest have the highest rankings.

* ? Should Betweenness be slower than Closeness, because closeness only needs one shortest path while betweenness must count them all?
* **2** _Degree Centrality:_ O(n+2m)
* **0** _Closeness Centrality:_ O(nm)
* **0** _Betweenness Centrality:_ O(nm)
* **1** _PageRank:_ O(numItter(n+2m))
	
**Accuracy**: I have zero clue right now...

* **3** _Degree Centrality:_
* **?** _Closeness Centrality:_
* **?** _Betweenness Centrality:_ Last because it's using a sampling method in case the graph gets too large
* **?** _PageRank:_  

**Reach:** Refered to as global, because that's how I'm ranking it. The more globaly an algorithm measures, the higher its score will be.

* **3** _Degree Centrality:_
* **?** _Closeness Centrality:_
* **?**_Betweenness Centrality:_
* **1** _PageRank:_ 

**Randomness:** Does an algorithm follow specific rules to find the path

## Cypher code
**Degree Centrality**
'''
CALL algo.degree.stream("Structure", "")
yield nodeId, score
return algo.getNodeById(nodeId).name as structure, score
order by score desc
'''

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
'''
CALL algo.pageRank.stream('Structure', '', {iterations:20, dampingFactor:0.70}) 
YIELD nodeId, score
RETURN algo.getNodeById(nodeId).name AS page, score
ORDER BY score DESC
'''

# Graph Algs book
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



# Fundamentals of Brain Network Analysis
## Chapter 1: An Introduction to Brain Networks
### 1.2 Graph Theory and the Brain
* Matrix and graph representation of networks equivalent
#### The Neuron THeory and Connectivity at the Microscale
* Ramon y Cajal predicted neuron structure
* Brain networks select to minimize wiring cost and/or minimize metabolic expenditure
#### The Dawn of Connectomics
* Initical neural connectomics done in macaque monkey and cats
	* Required lots of studies, because of limitations of tracer injection
* Full mapping of nervous system of C. elegans
	* Short characteristic path length and highclustering 
	* global organization: small-world topology
* small-world brain organization
	* short path length: favor integrated processing of information over whole network
	* high clustering: favor segregated processing within functionally specialized cliques of nodes
	* functional segregation and integration
#### 1.2.4 Neuroimaging and Human Connectomics
* Simplest way is to look at two time points of activity and compare correlation coefficients
* **Functional Connectivity:** statistical dependence between the time series of measured neurophysiological signals

	


## Chapter 5: Centrality and Hubs
### 5.1 Centrality
* Different measures capture different aspects of what it means to be "central" in a network
* Most measures arrive at same conclusion when network is star-like (hub and spoke) networks
	* Central node will be identified as having the highest centrality
#### 5.1.1 Degree-Based Measure of Centrality
* Limitation: Doesn't take importance of neighbors into account
* PageRank
	* scales contributions that neighbors of node make by degree of those enighbors
	* accounts for biases if node connected to high degree vs low degree nodes
	* 

#### 5.1.5 Characterizing Centrality in Brain Networks
* some centrality measures make assumptions about how signals travel through network
	* Ex: Betweenness centrality assumes singals take shortest path
* Borgatti (2005) two different ways to classify information flow
	1. How information flows between nodes
		* Serial transfer: Letters through multiple post offices
		* Serial duplication: Viral infections (human to human)
		* Parallel duplication: Computer virus (email sends itself to multiple people)
		* Parallel transfer (diffusion): (? Does this belong here?)
	2. trajectory information follows
		* Shortest path: Letter travels shortest path during delivery
			* Implies knowledge of network layout
		* path < trail < walk
* Where do nervous systems fit withing this classification scheme?
	* parallel transfer (diffusion)
		* Neurons fire, cause neighbors to fire, but return to resting state
	* modeled as trail or walk
* What does parallel transfer model tell us about how to measure centrality in brain networks?
	* Degree centrality: characterize imediate affect node has on others
	* Closeness centrality: high values affect lots of other neurons in a shorter amount of time
	* PageRank: global spread of event, nodes more closely connected to other central nodes will be able to spread information to more nodes faster
	* 
	
	