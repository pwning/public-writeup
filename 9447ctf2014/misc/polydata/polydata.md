In this challenge we are asked to provide one input which not only is valid
input for a travelling salesman, knapsack, and maximum subsequence solver, but
which attains the same optimum value for each problem.

Approach
--------------

Our first approach to solving this challenge was to encode each problem as an
instance for an SMT solver such as Z3. Then we can simply ask Z3 to find a
solution which achieves the same value for each.

Although this should work, this seemed really annoying, so we went with the
other tried and true method of solving problems: mess around with it until it
works.

The first thing we know is that the knapsack problem takes in a knapsack size
and then pairs of numbers, the travelling salesman takes in triplets of numbers
and the maximum subsequence takes in any number list. That means we should make
our list 9 or 15 numbers long to keep things simple.

Next we want to construct a simple graph, either a triangle or square. In order
to ensure the maximum subsequence does not dominate the problem, we will use a
large negative number as a vertex label to break up the subsequences.

The knapsack we want to be large enough that we can fit multiple things in it.
However, we know immediately the knapsack size and the first element size can be
added together for the maximum subsequence, so we must be able to achieve that
value. 

Our general strategy is to make a valid list and try to break up the maximum
subsequence with large negative numbers. We can add duplicate edges on our TSP
graph with higher weights to increase the value for the knapsack without the
TSP value changing. Then we just fiddle with the numbers in order to get things
close together!

In the end we mess around with all these parameters for a while by hand, trying
to make something that works. We end up with the following graph

             (5)
         8 ----- 1
     (2) |       |  (8)
         |  (2)  |
         2 ----- -50
            (1)

A knapsack of size 8 with item-weight pairs of (1,5),(1,-50),(8,-50),(2,2),(2,8),(2,-50),(2,-1)

And a final list of 8, 1 5, 1, -50, 8, -50, 2, 2, 2, 8, 2, -50, 2, 1

Echoing this out to the server we get 

    $ echo "8 1 5    1 -50 8   -50 2 2    2 8 2   -50 2 1#" | nc  polydata.9447.plumbing 13371
    Congratulations! The flag is 9447{fun_fact_this_data_is_better_than_most_Australian_ACM_data}

