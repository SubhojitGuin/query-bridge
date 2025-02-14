from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

examples = [
  {
    "input": "Which driver won the most races in the 2017 season?",
    "query": "select d.driverId, d.forename, d.surname, count(*) as wins from results res join races r on res.raceId = r.raceId join drivers d on res.driverId = d.driverId where r.year = 2017 and res.position = 1 group by d.driverId, d.forename, d.surname order by wins desc limit 1;"
  },
  {
    "input": "List all the constructors that participated in the 2016 season along with the number of races they participated in.",
    "query": "select c.constructorId, c.name as constructor_name, count(distinct r.raceId) as races_participated from results res join races r on res.raceId = r.raceId join constructors c on res.constructorId = c.constructorId where r.year = 2016 group by c.constructorId, c.name order by races_participated desc;"
  },
  {
    "input": "Which driver had the fastest lap time in the 2016 season?",
    "query": "select d.driverId, d.forename, d.surname, lt.lap, lt.milliseconds as fastest_lap_time from lap_times lt join races r on lt.raceId = r.raceId join drivers d on lt.driverId = d.driverId where r.year = 2016 order by lt.milliseconds asc limit 1;"
  },
  {
    "input": "What is the average pit stop duration for each race in the 2017 season?",
    "query": "select r.raceId, r.name as race_name, avg(ps.milliseconds) as average_pit_stop_duration from pit_stops ps join races r on ps.raceId = r.raceId where r.year = 2017 group by r.raceId, r.name order by average_pit_stop_duration;"
  },
  {
    "input": "Show the performance details of a specific driver (by driverId) in all races they participated in.",
    "query": "select r.raceId, r.name as race_name, r.date, res.position, res.points from results res join races r on res.raceId = r.raceId where res.driverId = ? order by r.date;"
  },
  {
    "input": "List the drivers who achieved a podium finish (top 3) in the 2015 season along with the number of podium finishes they have.",
    "query": "select d.driverId, d.forename, d.surname, count(*) as podium_finishes from results res join races r on res.raceId = r.raceId join drivers d on res.driverId = d.driverId where r.year = 2015 and res.position <= 3 group by d.driverId, d.forename, d.surname order by podium_finishes desc;"
  },
  {
    "input": "Find the total points scored by each driver across their career.",
    "query": "select d.driverId, d.forename, d.surname, sum(res.points) as total_points from drivers d join results res on d.driverId = res.driverId group by d.driverId, d.forename, d.surname order by total_points desc;"
  },
  {
    "input": "Which race in the 2010 season had the highest total points scored by drivers?",
    "query": "select r.raceId, r.name as race_name, r.date, sum(res.points) as total_points from races r join results res on r.raceId = res.raceId where r.year = 2010 group by r.raceId, r.name, r.date order by total_points desc limit 1;"
  },
  {
    "input": "List all the races where a specific constructor (by constructorId) won at least one race (finished with position 1) along with the date and name of the race.",
    "query": "select distinct r.raceId, r.name as race_name, r.date from results res join races r on res.raceId = r.raceId where res.constructorId = ? and res.position = 1 order by r.date;"
  },
  {
    "input": "For a given race, show the order of finish for all drivers along with their finishing positions and points earned.",
    "query": "select d.driverId, d.forename, d.surname, res.position, res.points from results res join drivers d on res.driverId = d.driverId where res.raceId = ? order by res.position;"
  }
]


def get_example_selector():
    example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    FAISS,
    k=5,
    input_keys=["input"],
)
    return example_selector



