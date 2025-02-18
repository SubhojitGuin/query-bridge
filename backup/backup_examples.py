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
    },
    {
        "input": "Get the details of all races held in a specific circuit.",
        "query": "SELECT r.name, r.year, r.round, r.date, r.time, c.name AS circuit_name, c.location, c.country FROM races r JOIN circuits c ON r.circuitId = c.circuitId WHERE c.name LIKE 'Circuit_X%';"
    },
    {
        "input": "List the top 3 drivers with the most wins in a specific race.",
        "query": "SELECT d.forename, d.surname, COUNT(*) AS wins FROM results res JOIN drivers d ON res.driverId = d.driverId JOIN races r ON res.raceId = r.raceId WHERE r.name LIKE 'Race_X%' AND res.position = 1 GROUP BY d.driverId ORDER BY wins DESC LIMIT 3;"
    },
    {
        "input": "Get the constructors and their points in a specific race.",
        "query": "SELECT cons.name, consRes.points FROM constructorResults consRes JOIN constructors cons ON consRes.constructorId = cons.constructorId JOIN races r ON consRes.raceId = r.raceId WHERE r.name LIKE 'Race_X%';"
    },
    {
        "input": "Find the driver standings for a specific race.",
        "query": "SELECT d.forename, d.surname, dStand.points, dStand.position FROM driverStandings dStand JOIN drivers d ON dStand.driverId = d.driverId JOIN races r ON dStand.raceId = r.raceId WHERE r.name LIKE 'Race_X%' ORDER BY dStand.position;"
    },
    {
        "input": "Get the fastest lap time and driver details for a specific race.",
        "query": "SELECT d.forename, d.surname, res.fastestLapTime FROM results res JOIN drivers d ON res.driverId = d.driverId JOIN races r ON res.raceId = r.raceId WHERE r.name LIKE 'Race_X%' AND res.fastestLapTime IS NOT NULL ORDER BY res.fastestLapTime LIMIT 1;"
    },
    {
        "input": "List all drivers who participated in a specific race.",
        "query": "SELECT DISTINCT d.forename, d.surname FROM results res JOIN drivers d ON res.driverId = d.driverId JOIN races r ON res.raceId = r.raceId WHERE r.name LIKE 'Race_X%';"
    },
    {
        "input": "Retrieve the constructor standings for a specific race.",
        "query": "SELECT cons.name, cStand.points, cStand.position FROM constructorStandings cStand JOIN constructors cons ON cStand.constructorId = cons.constructorId JOIN races r ON cStand.raceId = r.raceId WHERE r.name LIKE 'Race_X%' ORDER BY cStand.position;"
    },
    {
        "input": "Get the number of pit stops made by each driver in a specific race.",
        "query": "SELECT d.forename, d.surname, COUNT(*) AS pit_stops FROM pitStops p JOIN drivers d ON p.driverId = d.driverId JOIN races r ON p.raceId = r.raceId WHERE r.name LIKE 'Race_X%' GROUP BY d.driverId ORDER BY pit_stops DESC;"
    },
    {
        "input": "Find the average lap time of each driver in a specific race.",
        "query": "SELECT d.forename, d.surname, AVG(l.milliseconds) AS avg_lap_time FROM lapTimes l JOIN drivers d ON l.driverId = d.driverId JOIN races r ON l.raceId = r.raceId WHERE r.name LIKE 'Race_X%' GROUP BY d.driverId ORDER BY avg_lap_time;"
    },
    {
        "input": "Get the qualifying positions of drivers in a specific race.",
        "query": "SELECT d.forename, d.surname, q.position, q.q1, q.q2, q.q3 FROM qualifying q JOIN drivers d ON q.driverId = d.driverId JOIN races r ON q.raceId = r.raceId WHERE r.name LIKE 'Race_X%' ORDER BY q.position;"
    },
    {
        "input": "Find the driver with the most wins across all races.",
        "query": "SELECT d.forename, d.surname, COUNT(*) AS wins FROM results res JOIN drivers d ON res.driverId = d.driverId WHERE res.position = 1 GROUP BY d.driverId ORDER BY wins DESC LIMIT 1;"
    },
    {
        "input": "Get the constructor with the most championship points across all races.",
        "query": "SELECT cons.name, SUM(consStand.points) AS total_points FROM constructorStandings consStand JOIN constructors cons ON consStand.constructorId = cons.constructorId GROUP BY cons.name ORDER BY total_points DESC LIMIT 1;"
    },
    {
        "input": "List all races won by a specific driver.",
        "query": "SELECT r.name, r.year, r.date FROM results res JOIN races r ON res.raceId = r.raceId JOIN drivers d ON res.driverId = d.driverId WHERE d.surname LIKE 'Driver_X%' AND res.position = 1;"
    },
    {
        "input": "Find the driver with the fastest average lap time in a specific race.",
        "query": "SELECT d.forename, d.surname, AVG(l.milliseconds) AS avg_lap_time FROM lapTimes l JOIN drivers d ON l.driverId = d.driverId JOIN races r ON l.raceId = r.raceId WHERE r.name LIKE 'Race_X%' GROUP BY d.driverId ORDER BY avg_lap_time LIMIT 1;"
    },
    {
        "input": "Retrieve all race winners along with their constructors for a specific year.",
        "query": "SELECT r.name, d.forename, d.surname, cons.name AS constructor FROM results res JOIN races r ON res.raceId = r.raceId JOIN drivers d ON res.driverId = d.driverId JOIN constructors cons ON res.constructorId = cons.constructorId WHERE r.year = 2023 AND res.position = 1;"
    }
]