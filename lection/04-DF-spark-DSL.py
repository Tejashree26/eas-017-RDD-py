from time import sleep

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql import functions as F


spark = SparkSession. \
    builder. \
    appName("Data Sources"). \
    master("local"). \
    config("spark.jars", "../jars/postgresql-42.2.19.jar"). \
    config("spark.sql.legacy.timeParserPolicy", "LEGACY"). \
    config("spark.sql.autoBroadcastJoinThreshold", -1). \
    getOrCreate()

movies_df = spark.read.json("../sources/movies")


# def aggregations():
    # counting
    # all_movies_count_df = movies_df.selectExpr("count(Major_Genre)")
    # print("SIMPLE COUNT")
    # all_movies_count_df.show()
    # all_movies_count_df.explain()

    #  null not included
    # genres_count_df = movies_df.select(count(col("Major_Genre")))
    # print("SIMPLE COUNT Genre")
    # genres_count_df.show()
    # genres_count_df.explain()

    # genres_count_df_v2 = movies_df.selectExpr("count(*)")
    # print("SIMPLE COUNT Genre Expr")
    # genres_count_df_v2.show()

    #  null included
    # genres_count_number = movies_df.select("Major_Genre").count()
    # print("SIMPLE COUNT Genre wit select")
    # print(genres_count_number)

    # count distinct NOT WORKING
    # unique_genres_df = movies_df.select(F.countDistinct(F.col("Major_Genre")))
    # print("COUNT DISTINCT Genre wit select")
    # print(unique_genres_df)

    # unique_genres_df_v2 = movies_df.selectExpr("count(DISTINCT Major_Genre)")
    # print("COUNT DISTINCT Genre with Expression")
    # unique_genres_df_v2.show()
    #
    # # math aggregations
    # # min/max
    # max_rating_df = movies_df.select(max(col("IMDB_Rating")).alias("max value of IMDB Rating"))
    # print("max IMDB_Rating with functions")
    # max_rating_df.show()
    #
    # max_rating_df_v2 = movies_df.selectExpr("min(IMDB_Rating)").alias("mix value of IMDB Rating")
    # print("max IMDB_Rating with Expression")
    # max_rating_df_v2.show()

    # sum values in a column
    # us_industry_total_df = movies_df.select(sum(col("US_Gross")))
    # print("sum US_Gross")
    # us_industry_total_df.show()
    #
    #
    # us_industry_total_df_v2 = movies_df.selectExpr("sum(US_Gross)")
    # print("sum US_Gross Expr")
    # us_industry_total_df_v2.show()
    #
    # # avg
    # avg_rt_rating_df = movies_df.select(avg(col("Rotten_Tomatoes_Rating")))
    # print("avg Rotten_Tomatoes_Rating")
    # avg_rt_rating_df.show()



    # mean/standard dev
    # rt_stats_df = movies_df.agg(
    #     mean(col("Rotten_Tomatoes_Rating")),
    #     stddev(col("Rotten_Tomatoes_Rating"))
    # )
    # print("mean/standard dev")
    # rt_stats_df.show()
    #
    # # Grouping
    # # nulls are also considered
    # count_by_genre_df = movies_df. \
    #     groupBy(col("Major_Genre")). \
    #     count()
    # print("count group by dev")
    # count_by_genre_df.show()
    # count_by_genre_df.explain()
    #
    # avg_rating_by_genre_df = movies_df. \
    #     groupBy(col("Major_Genre")). \
    #     avg("IMDB_Rating")
    # print("count group by dev")
    # count_by_genre_df.show()
    # avg_rating_by_genre_df.show()
    # avg_rating_by_genre_df.explain()
    #
    #
    # # multiple aggregations
    # aggregations_by_genre_df = movies_df. \
    #     groupBy(col("Major_Genre")). \
    #     agg(
    #     # use strings here for column names
    #     count("*").alias("N_Movies"),
    #     avg("IMDB_Rating").alias("Avg_Rating")
    # )
    # aggregations_by_genre_df.show()


    # sorting
    # best_movies_df = movies_df.orderBy(col("IMDB_Rating").desc())
    # best_movies_df.show()
    # best_movies_df.explain()
    #
    # # sorting works for numerical, strings (lexicographic), dates
    #
    # # put nulls first or last
    # proper_worst_movies_df = movies_df.orderBy(col("IMDB_Rating").asc_nulls_last())
    # proper_worst_movies_df.show()

"""
    Exercises
        1. Sum up ALL the profits of ALL the movies in the dataset
        2. Count how many distinct directors we have
        3. Show the mean, stddev for US gross revenue
        4. Compute the average IMDB rating, average US gross PER DIRECTOR
        5. Show the average difference between IMDB rating and Rotten Tomatoes rating
"""

# avg(IMDB rating - Rotten Tomatoes) != avg(IMDB rating) - avg(Rotten Tomatoes)

guitars_df = spark.read.json("../sources/guitars")
guitar_players_df = spark.read.json("../sources/guitarPlayers")
bands_df = spark.read.json("../sources/bands")


def joins():
    # inner joins = all rows from the "left" and "right" DF for which the condition is true
    join_condition = guitar_players_df.band == bands_df.id
    guitarists_bands_df = guitar_players_df.join(bands_df, join_condition, "inner")
    #                     ^^ "left" DF            ^^ "right" DF
    # guitarists_bands_df.show()

    # node 1 => 1|    [1]|  1| Angus Young|     Sydney|
    # node 2 => 1|       AC/DC|1973|
    # node 3 => 1|    [1]|  1| Angus Young|     Sydney| 1|       AC/DC|1973|
    # node 4 => 2, 4
    # node 5 => 11, 12
    #
    # +----+-------+---+------------+-----------+---+------------+----+
    # |band|guitars| id|        name|   hometown| id|        name|year|
    # +----+-------+---+------------+-----------+---+------------+----+
    # |   1|    [1]|  1| Angus Young|     Sydney|  1|       AC/DC|1973|
    # |   0|    [0]|  0|  Jimmy Page|     London|  0|Led Zeppelin|1968|
    # |   3|    [3]|  3|Kirk Hammett|Los Angeles|  3|   Metallica|1981|
    # +----+-------+---+------------+-----------+---+------------+----+
    #


    # differentiate the "name" column - use the reference from the original DF
    guitarists_bands_upper_df = guitarists_bands_df.select(upper(bands_df.name))
    # guitarists_bands_upper_df.show()
    # guitarists_bands_upper_df.explain()


    # left outer = everything in the inner join + all the rows in the LEFT DF that were not matched (with nulls in the cols for the right DF)
    guitar_players_df.join(bands_df, join_condition, "left_outer")

    # right outer = everything in the inner join + all the rows in the RIGHT DF that were not matched (with nulls in the cols for the left DF)
    guitar_players_df.join(bands_df, join_condition, "right_outer")

    # full outer join = everythin in the inner join + all the rows in BOTH DFs that were not matched (with nulls in the other DF's cols)
    guitar_players_df.join(bands_df, join_condition, "outer")

    # join on a single column
    # guitar_players_df.join(bands_df, "id")

    # left semi joins = everything in the LEFT DF for which there is a row in the right DF for which the condition is true
    # more like a filter
    # equivalent SQL: select * from guitar_players WHERE EXISTS (...)
    guitar_players_df.join(bands_df, join_condition, "left_semi")

    # left anti joins = everything in the LEFT DF for which there is __NO__ row in the right DF for which the condition is true
    guitar_players_df.join(bands_df, join_condition, "left_anti")


driver = "org.postgresql.Driver"
url = "jdbc:postgresql://localhost:5432/spark"
user = "docker"
password = "docker"


def read_table(table_name):
    return spark.read. \
        format("jdbc"). \
        option("driver", driver). \
        option("url", url). \
        option("user", user). \
        option("password", password). \
        option("dbtable", "public." + table_name). \
        load()

# employees_df = read_table("employees")
# salaries_df = read_table("salaries")
# dept_managers_df = read_table("dept_manager")
# dept_emp_df = read_table("dept_emp")
# departments_df = read_table("departments")

"""
Exercises
Read the tables in the Postgres database: employees, salaries, dept_emp
1. show all employees and their max salary over time
2. show all employees who were never managers
3. for every employee, find the difference between their salary (current/latest) and 
    the max salary of their department (departments table)
"""

if __name__ == '__main__':
    joins()
    sleep(100000)
