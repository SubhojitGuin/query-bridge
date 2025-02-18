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
        "input": "Where was the British Grand Prix held?",
        "query": "SELECT name, location, country FROM circuits WHERE circuitId = (SELECT circuitId FROM races WHERE name LIKE '%British Grand Prix%' LIMIT 1);"
    },
    {
        "input": "Which constructor won the most races in 2021?",
        "query": "SELECT c.name, COUNT(cs.wins) AS total_wins FROM constructor_standings cs JOIN constructors c ON cs.constructorId = c.constructorId JOIN races r ON cs.raceId = r.raceId WHERE r.year = 2021 AND cs.wins > 0 GROUP BY c.name ORDER BY total_wins DESC LIMIT 1;"
    },
    {
        "input": "What is the fastest lap time recorded at the Monaco Grand Prix?",
        "query": "SELECT r.year, res.fastestLapTime FROM results res JOIN races r ON res.raceId = r.raceId WHERE r.name LIKE '%Monaco Grand Prix%' AND res.fastestLapTime IS NOT NULL ORDER BY res.fastestLapTime ASC LIMIT 1;"
    },
    {
        "input": "Which driver has the most pole positions in F1 history?",
        "query": "SELECT d.forename, d.surname, COUNT(q.position) AS pole_positions FROM qualifying q JOIN drivers d ON q.driverId = d.driverId WHERE q.position = 1 GROUP BY d.forename, d.surname ORDER BY pole_positions DESC LIMIT 1;"
    },
    {
        "input": "How many pit stops did Lewis Hamilton make in the 2022 season?",
        "query": "SELECT COUNT(*) AS total_pit_stops FROM pit_stops ps JOIN drivers d ON ps.driverId = d.driverId JOIN races r ON ps.raceId = r.raceId WHERE r.year = 2022 AND d.surname LIKE '%Hamilton%';"
    },
    {
        "input": "Which F1 season had the most races?",
        "query": "SELECT year, COUNT(*) AS total_races FROM races GROUP BY year ORDER BY total_races DESC LIMIT 1;"
    },
    {
        "input": "Which driver has the most fastest laps in a single season?",
        "query": "SELECT d.forename, d.surname, COUNT(res.fastestLap) AS total_fastest_laps FROM results res JOIN drivers d ON res.driverId = d.driverId JOIN races r ON res.raceId = r.raceId WHERE r.year = 2023 GROUP BY d.forename, d.surname ORDER BY total_fastest_laps DESC LIMIT 1;"
    },
    {
        "input": "What is the highest number of points ever scored by a constructor in a season?",
        "query": "SELECT r.year, c.name, SUM(cs.points) AS total_points FROM constructor_standings cs JOIN constructors c ON cs.constructorId = c.constructorId JOIN races r ON cs.raceId = r.raceId GROUP BY r.year, c.name ORDER BY total_points DESC LIMIT 1;"
    },
    {
        "input": "Which circuit has hosted the most F1 races?",
        "query": "SELECT c.name, COUNT(r.raceId) AS total_races FROM races r JOIN circuits c ON r.circuitId = c.circuitId GROUP BY c.name ORDER BY total_races DESC LIMIT 1;"
    },
    {
        "input": "Which drivers won the most races in the 2023 season?",
        "query": "SELECT d.forename, d.surname, COUNT(ds.wins) AS total_wins FROM driver_standings ds JOIN drivers d ON ds.driverId = d.driverId JOIN races r ON ds.raceId = r.raceId WHERE r.year = 2023 AND ds.wins > 0 GROUP BY d.forename, d.surname ORDER BY total_wins DESC;"
    },
    {
        "input": "Which F1 constructors scored the most points in the 2022 season?",
        "query": "SELECT c.name, SUM(cs.points) AS total_points FROM constructor_standings cs JOIN constructors c ON cs.constructorId = c.constructorId JOIN races r ON cs.raceId = r.raceId WHERE r.year = 2022 GROUP BY c.name ORDER BY total_points DESC LIMIT 5;"
    },
    {
        "input": "Which F1 race had the smallest gap between the top two qualifying drivers?",
        "query": "SELECT r.year, r.name, MIN(q2.q1 - q1.q1) AS min_time_gap FROM qualifying q1 JOIN qualifying q2 ON q1.raceId = q2.raceId AND q1.position = 1 AND q2.position = 2 JOIN races r ON q1.raceId = r.raceId WHERE q1.q1 IS NOT NULL AND q2.q1 IS NOT NULL GROUP BY r.year, r.name ORDER BY min_time_gap ASC LIMIT 1;"
    },
    {
        "input": "Which driver led the most laps in the 2021 season?",
        "query": "SELECT d.forename, d.surname, SUM(res.laps) AS total_laps_led FROM results res JOIN drivers d ON res.driverId = d.driverId JOIN races r ON res.raceId = r.raceId WHERE r.year = 2021 AND res.positionOrder = 1 GROUP BY d.forename, d.surname ORDER BY total_laps_led DESC LIMIT 1;"
    },
    {
        "input": "Which F1 constructor had the highest average position gain in the 2023 season?",
        "query": "SELECT c.name, AVG(res.grid - res.positionOrder) AS avg_position_gain FROM results res JOIN constructors c ON res.constructorId = c.constructorId JOIN races r ON res.raceId = r.raceId WHERE r.year = 2023 AND res.grid > 0 AND res.positionOrder > 0 GROUP BY c.name ORDER BY avg_position_gain DESC LIMIT 1;"
    },
    {
        "input": "In which F1 race was the fastest lap recorded at the highest speed?",
        "query": "SELECT r.year, r.name, MAX(res.fastestLapSpeed) AS max_speed FROM results res JOIN races r ON res.raceId = r.raceId WHERE res.fastestLapSpeed IS NOT NULL GROUP BY r.year, r.name ORDER BY max_speed DESC LIMIT 1;"
    },
    {
        "input": "In which races did Charles Leclerc finish in the top 3 in 2022?",
        "query": "SELECT r.year, r.name, res.position FROM results res JOIN drivers d ON res.driverId = d.driverId JOIN races r ON res.raceId = r.raceId WHERE r.year = 2022 AND d.surname LIKE 'Leclerc%' AND res.positionOrder BETWEEN 1 AND 3 ORDER BY r.date;"
    },
    {
        "input": "Which F1 driver has entered the most races without ever winning?",
        "query": "SELECT d.forename, d.surname, COUNT(res.raceId) AS total_races FROM results res JOIN drivers d ON res.driverId = d.driverId WHERE res.positionOrder > 1 GROUP BY d.forename, d.surname ORDER BY total_races DESC LIMIT 1;"
    },
    {
        "input": "What was the longest lap time recorded in the 2023 season?",
        "query": "SELECT r.year, r.name, l.driverId, MAX(l.milliseconds) AS longest_lap_time FROM lap_times l JOIN races r ON l.raceId = r.raceId WHERE r.year = 2023 GROUP BY r.year, r.name, l.driverId ORDER BY longest_lap_time DESC LIMIT 1;"
    },
    {
        "input": "Which F1 constructors participated in all races of the 2022 season?",
        "query": "SELECT c.name FROM constructors c JOIN results res ON c.constructorId = res.constructorId JOIN races r ON res.raceId = r.raceId WHERE r.year = 2022 GROUP BY c.name HAVING COUNT(DISTINCT r.raceId) = (SELECT COUNT(*) FROM races WHERE year = 2022);"
    },
    {
        "input": "Which drivers won the most races in 2023?",
        "query": "SELECT d.forename, d.surname, COUNT(r.resultId) AS wins FROM results r JOIN races ra ON r.raceId = ra.raceId JOIN drivers d ON r.driverId = d.driverId WHERE r.position = '1' AND ra.year = 2023 GROUP BY d.forename, d.surname ORDER BY wins DESC;"
    },
    {
        "input": "What is the total number of points scored by each constructor in the 2022 season?",
        "query": "SELECT c.name, SUM(cr.points) AS total_points FROM constructor_results cr JOIN races ra ON cr.raceId = ra.raceId JOIN constructors c ON cr.constructorId = c.constructorId WHERE ra.year = 2022 GROUP BY c.name ORDER BY total_points DESC;"
    },
    {
        "input": "What is the fastest lap time recorded by a driver in the 2023 season?",
        "query": "SELECT d.forename, d.surname, MIN(r.fastestLapTime) AS fastest_lap_time FROM results r JOIN races ra ON r.raceId = ra.raceId JOIN drivers d ON r.driverId = d.driverId WHERE ra.year = 2023 AND r.fastestLapTime IS NOT NULL GROUP BY d.forename, d.surname ORDER BY fastest_lap_time ASC LIMIT 1;"
    },
    {
        "input": "Which driver has the most pole positions (qualified 1st) in 2023?",
        "query": "SELECT d.forename, d.surname, COUNT(q.qualifyId) AS pole_positions FROM qualifying q JOIN races ra ON q.raceId = ra.raceId JOIN drivers d ON q.driverId = d.driverId WHERE ra.year = 2023 AND q.position = 1 GROUP BY d.forename, d.surname ORDER BY pole_positions DESC;"
    },
    {
        "input": "How many wins did each driver achieve across all seasons?",
        "query": "SELECT d.forename, d.surname, COUNT(r.resultId) AS wins FROM results r JOIN drivers d ON r.driverId = d.driverId WHERE r.position = '1' GROUP BY d.forename, d.surname ORDER BY wins DESC;"
    },
    {
        "input": "What is the average pit stop duration for each driver in the 2023 season?",
        "query": "SELECT d.forename, d.surname, AVG(ps.milliseconds) AS avg_pit_stop_duration FROM pit_stops ps JOIN races ra ON ps.raceId = ra.raceId JOIN drivers d ON ps.driverId = d.driverId WHERE ra.year = 2023 GROUP BY d.forename, d.surname ORDER BY avg_pit_stop_duration ASC;"
    },
    {
        "input": "Which driver had the fastest laps in the 2023 season?",
        "query": "SELECT d.forename, d.surname, COUNT(r.fastestLap) AS fastest_laps FROM results r JOIN races ra ON r.raceId = ra.raceId JOIN drivers d ON r.driverId = d.driverId WHERE ra.year = 2023 AND r.fastestLap IS NOT NULL GROUP BY d.forename, d.surname ORDER BY fastest_laps DESC;"
    },
    {
        "input": "Which drivers finished in the top 3 most frequently in 2023?",
        "query": "SELECT d.forename, d.surname, COUNT(r.resultId) AS podiums FROM results r JOIN races ra ON r.raceId = ra.raceId JOIN drivers d ON r.driverId = d.driverId WHERE ra.year = 2023 AND r.position IN ('1', '2', '3') GROUP BY d.forename, d.surname ORDER BY podiums DESC;"
    },
    {
        "input": "Which drivers are from the United Kingdom?",
        "query": "SELECT forename, surname FROM drivers WHERE nationality LIKE '%British%';"
    },
    {
        "input": "How many races were held in 2022?",
        "query": "SELECT COUNT(*) AS race_count FROM races WHERE year = 2022;"
    },
    {
        "input": "Which driver achieved the highest total points in 2023?",
        "query": "SELECT d.forename, d.surname, SUM(ds.points) AS total_points FROM driver_standings ds JOIN races ra ON ds.raceId = ra.raceId JOIN drivers d ON ds.driverId = d.driverId WHERE ra.year = 2023 GROUP BY d.forename, d.surname ORDER BY total_points DESC LIMIT 1;"
    },
    {
        "input": "Which constructors won at least one race in 2023?",
        "query": "SELECT DISTINCT c.name FROM results r JOIN races ra ON r.raceId = ra.raceId JOIN constructors c ON r.constructorId = c.constructorId WHERE r.position = '1' AND ra.year = 2023;"
    },
    {
        "input": "Which race in 2023 had the closest winning margin in milliseconds?",
        "query": "SELECT ra.name, ra.date, MIN(r.milliseconds) AS winning_time FROM results r JOIN races ra ON r.raceId = ra.raceId WHERE ra.year = 2023 AND r.position = '1' GROUP BY ra.name, ra.date ORDER BY winning_time ASC LIMIT 1;"
    },
    {
        "input": "Who is the winner of the last season?",
        "query": "SELECT DISTINCT d.forename, d.surname FROM driver_standings ds JOIN drivers d ON ds.driverId = d.driverId JOIN races r ON ds.raceId = r.raceId WHERE r.year = (SELECT MAX(year) FROM seasons) AND ds.position = 1;"
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



