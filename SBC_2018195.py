#!/usr/bin/env python3

import re
import itertools

ROLLNUM_REGEX = "201[0-9]{4}"

class Graph(object):
    name = "Shubhi Singhal"
    email = "shubhi18195@iiitd.ac.in"
    roll_num = "2018195"

    def __init__ (self, vertices, edges):
        """
        Initializes object for the class Graph

        Args:
            vertices: List of integers specifying vertices in graph
            edges: List of 2-tuples specifying edges in graph
        """

        self.vertices = vertices
        
        ordered_edges = list(map(lambda x: (min(x), max(x)), edges))
        
        self.edges    = ordered_edges
        
        self.validate()

    def validate(self):
        """
        Validates if Graph if valid or not

        Raises:
            Exception if:
                - Name is empty or not a string
                - Email is empty or not a string
                - Roll Number is not in correct format
                - vertices contains duplicates
                - edges contain duplicates
                - any endpoint of an edge is not in vertices
        """

        if (not isinstance(self.name, str)) or self.name == "":
            raise Exception("Name can't be empty")

        if (not isinstance(self.email, str)) or self.email == "":
            raise Exception("Email can't be empty")

        if (not isinstance(self.roll_num, str)) or (not re.match(ROLLNUM_REGEX, self.roll_num)):
            raise Exception("Invalid roll number, roll number must be a string of form 201XXXX. Provided roll number: {}".format(self.roll_num))

        if not all([isinstance(node, int) for node in self.vertices]):
            raise Exception("All vertices should be integers")

        elif len(self.vertices) != len(set(self.vertices)):
            duplicate_vertices = set([node for node in self.vertices if self.vertices.count(node) > 1])

            raise Exception("Vertices contain duplicates.\nVertices: {}\nDuplicate vertices: {}".format(vertices, duplicate_vertices))

        edge_vertices = list(set(itertools.chain(*self.edges)))

        if not all([node in self.vertices for node in edge_vertices]):
            raise Exception("All endpoints of edges must belong in vertices")

        if len(self.edges) != len(set(self.edges)):
            duplicate_edges = set([edge for edge in self.edges if self.edges.count(edge) > 1])

            raise Exception("Edges contain duplicates.\nEdges: {}\nDuplicate vertices: {}".format(edges, duplicate_edges))

    def dict(self):
        d={}
        for i in vertices:
            d[i]=[]
            for j in edges:
                if i in j:
                    if j[0]==i:
                        d[i].append(j[1])
                    else:
                        d[i].append(j[0])
        return d

    def bfsandlevels(self,node):
        d=self.dict()
        v=node
        levels=[]
        bfs=[v]
        levels.append([v])
        levels.append(d[v])
        while (len(bfs)!=len(vertices)):
            listappend=[]
            for a in levels[len(levels)-1]:
                l=d[a]
                bfs.append(a)
                for i in l:
                    count=0
                    if i not in bfs and i not in listappend:
                        for j in range(len(levels)):
                            if i in levels[j]:
                               count+=1
                        if count==0:
                           listappend.append(i)
            levels.append(listappend)

        levelslist=[]
        for i in levels:
            if i!=[]:
                levelslist.append(i)
        
        return [bfs,levelslist]


    def min_dist(self, start_node, end_node):
        '''
        Finds minimum distance between start_node and end_node

        Args:
            start_node: Vertex to find distance from
            end_node: Vertex to find distance to

        Returns:
            An integer denoting minimum distance between start_node
            and end_node
        '''
        d=self.dict()
        b_and_l=self.bfsandlevels(start_node)
        bfs=b_and_l[0]
        levels=b_and_l[1]
       
        for i in range(len(levels)):
            if end_node in levels[i]:
                return i

    def all_shortest_paths(self, start_node, end_node):
        """
        Finds all shortest paths between start_node and end_node

        Args:
            start_node: Starting node for paths
            end_node: Destination node for paths

        Returns:
            A list of path, where each path is a list of integers.
        """
        s=self.min_dist(start_node,end_node)
        return self.all_paths(start_node,end_node,s,[])
        

    def all_paths(self, node, destination, dist, path):
        """
        Finds all paths from node to destination with length = dist

        Args:
            node: Node to find path from
            destination: Node to reach
            dist: Allowed distance of path
            path: path already traversed

        Returns:
            List of path, where each path is list ending on destination

            Returns None if there no paths
        """

        d=self.dict()
        p=[]
        for i in range(len(path)):
            p.append(path[i])
        p.insert(len(p),node)
    
        if len(p)-1==dist:
            if node==destination:
                return p
            else:
                return None

        my_paths=[]

        for a in d[node]:
            if a not in p:
                p1=self.all_paths(a,destination,dist,p)

                if p1!=None:
                    if isinstance(p1[0],list):
                        for i in range(len(p1)):
                            my_paths.append(p1[i])
                    else:
                        my_paths.append(p1)

        if len(my_paths)!=0:
            return my_paths
        else:
            return None



    def betweenness_centrality(self, node):
        """
        Find betweenness centrality of the given node

        Args:
            node: Node to find betweenness centrality of.

        Returns:
            Single floating point number, denoting betweenness centrality
            of the given node
        """
        l=[]
        b=0
        for i in vertices:
            if i!=node:
                l.append(i)
        comb=list(itertools.combinations(l,2))
        
        for c in comb:
            count=0
            l=self.all_shortest_paths(c[0],c[1])
            if l==None:
                print(c)
            for i in range(len(l)):
                if node in l[i]:
                    count+=1
            b+=count/len(l)

        return b

        

    def top_k_betweenness_centrality(self):
        """
        Find top k nodes based on highest equal betweenness centrality.

        
        Returns:
            List a integer, denoting top k nodes based on betweenness
            centrality.
        """
        d={}
        l=[]
        for v in vertices:
            a=self.betweenness_centrality(v)
            d[v]=a
            l.append(a)
        m=max(l)
        l1=[]
        for key in d:
            if d[key]==m:
                l1.append(key)

        return l1


if __name__ == "__main__":
    vertices = [1, 2, 3, 4, 5, 6]
    edges    = [(1, 2), (1, 5), (2, 3), (2, 5), (3, 4), (4, 5), (4, 6), (3,6)]
    graph = Graph(vertices, edges)
    print(graph.top_k_betweenness_centrality())