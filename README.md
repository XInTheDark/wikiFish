<div align="center">
    <h3>wikiFish</h3>
    <h4> A fast and strong wiki speedrun bot. </h4>
</div>

## About
Wiki Speedrun is a fun game where players start with some Wikipedia article, and by clicking the hyperlinks
in the articles, try to get to some other article in the least amount of time and clicks possible.

wikiFish is a bot that plays this game for you. 

## Algorithm
Clearly, there is no way to find the *definitive* optimal route in a reasonable amount of time,
as that would mean getting the links from (almost) every single article on Wikipedia.
Hence, wikiFish compromises by fetching only a certain number of links from each article,
and also limiting the number of articles in total.

1. wikiBot fetches the links from the start article.
2. From each linked article, it fetches the links again, etc.
3. After it has constructed a reasonably sized graph, wikiBot efficiently finds the shortest path
from the starting article to the target article.

## Pre-generated tables
To drastically improve efficiency, wikiFish supports loading pre-generated adj files, which it can then do a direct search on. These tables can be generated using [construct.py](construct.py). Some examples can be found in [adj/public](adj/public).

