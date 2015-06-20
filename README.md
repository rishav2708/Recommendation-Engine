# Recommendation-Engine
Internship Project

This project involves recommendation on spatial domain on different keyword search.
The engine posseses search on thread basis towards neo4j server. For a single query we try to create several threads 
and search the database in different domains. 

Initially, in the engine we are searching in only two domains that are (By Name and By Type)

For every type of search by the user the results are displayed on the ranking of the documents on the basis of
two categories.
  They are : 
   ~~~bash
    The randomness of the places in the particular category in the vicinty
    The relatedness of the place with the types (Name based search).
  ~~~
 The randomness means the availability of the search results. The type which is easily available and relates nearly 
 to the searching query is displayed first.
 We have also added a provision to cluster the places on the basis of ranking and hence it would also contribute
 to a parameter in a better response to the search query in future.
 
 Randomness is calculated on the basis of distance metric for the availability of same types of places in a given 
 spatial domain. 
 We have specially pondered over certain points to generate a proper algorithm to define randomness:
      
      
      The randomness score tells the distribution of similar kinds of places on a given geo spatial domain
      Less the randomness higher the score of the type/class becomes
      
  When the results are on the basis of names, we try to # predict the related types and other places that may belong to 
  the same category (following the concept of nearest neighbors)
 We are though concerned with only single word search till now and would try to improve on the query processing part.
 
