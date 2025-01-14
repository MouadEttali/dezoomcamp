# Module 1 Homework: Docker & SQL
from inside this folder (i.e 01-docker-terraform) run the next commands:

* To build the image 

```docker build -t taxi_ingest:v001 .```

* To run the image with the parameters to the entrypoint specified in the dockerfile: 

```docker run -it --network=postgres_network taxi_ingest:v001 --user root --password root --host postgres_container --port 5432 --db ny_taxi --table-name yellow_taxi_data --url ${URL}```

Note : I put some comments to explain the dockerfile 


Let's go over the homework questions : 


## Question 1. Understanding docker first run

Run docker with the python:3.12.8 image in an interactive mode, use the entrypoint bash.

Solution :  
 1- ```docker run -it --rm python:3.12.8 bash```  # this will open the terminal of this container and remove it after we're done with it 
 2- ```pip --version```  

The version of pip in this image is : 

* 24.3.1

## Question 2. Understanding Docker networking and docker-compose

Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?
I'll skip copying the docker-compose.yaml from the dezoomcamp repo :
the Solution is :
* postgres:5433
 
Why : postgres being the container_name it serves as the localhost inside the "implicit" network created by grouping pgadmin and postgres in the ```services:``` field of the docker compose


## Question 3. Trip Segmentation Count
During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, respectively, happened:

* Up to 1 mile = 104,802

```sql
SELECT 
    COUNT(*) AS trip_count
FROM 
    green_taxi_data
WHERE 
    (lpep_pickup_datetime >= '2019-10-01 00:00:00' 
    AND lpep_pickup_datetime < '2019-11-01 00:00:00')
	AND trip_distance <= 1;
```

* In between 1 (exclusive) and 3 miles (inclusive) = 198,924
```sql
SELECT 
    COUNT(*) AS trip_count
FROM 
    green_taxi_data
WHERE 
    (lpep_pickup_datetime >= '2019-10-01 00:00:00' 
    AND lpep_pickup_datetime < '2019-11-01 00:00:00')
	AND (trip_distance > 1 and trip_distance <=3);
```

* In between 3 (exclusive) and 7 miles (inclusive)= 110,612
```sql
SELECT 
    COUNT(*) AS trip_count
FROM 
    green_taxi_data
WHERE 
    (lpep_pickup_datetime >= '2019-10-01 00:00:00' 
    AND lpep_pickup_datetime < '2019-11-01 00:00:00')
	AND (trip_distance > 1 and trip_distance <=3);
```
* In between 7 (exclusive) and 10 miles (inclusive)= 27,678
```sql
SELECT 
    COUNT(*) AS trip_count
FROM 
    green_taxi_data
WHERE 
    (lpep_pickup_datetime >= '2019-10-01 00:00:00' 
    AND lpep_pickup_datetime < '2019-11-01 00:00:00')
	AND (trip_distance > 7 and trip_distance <=10);
```
* Over 10 miles = 35,202
```sql
SELECT 
    COUNT(*) AS trip_count
FROM 
    green_taxi_data
WHERE 
    (lpep_pickup_datetime >= '2019-10-01 00:00:00' 
    AND lpep_pickup_datetime < '2019-11-01 00:00:00')
	AND trip_distance > 10 ;
```

## Question 4. Longest trip for each day
Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.


Solution : 2019-10-31

```sql
SELECT lpep_pickup_datetime, trip_distance FROM public.green_taxi_data
ORDER BY trip_distance DESC
LIMIT 1;
```

## Question 5. Three biggest pickup zones
Which were the top pickup locations with over 13,000 in total_amount (across all trips) for 2019-10-18?

Consider only lpep_pickup_datetime when filtering by date.

Solution : 
- East Harlem North, East Harlem South, Morningside Heights
```sql
SELECT 
    SUM(g.total_amount) as sum_amount, 
    g."PULocationID", 
    z."Zone" AS pickup_zone
FROM public.green_taxi_data g
JOIN public.zone_data z
    ON g."PULocationID" = z."LocationID"  -- Joining on pickup location

WHERE g.lpep_pickup_datetime::date = '2019-10-18'  -- Filtering by specific date
GROUP BY pickup_zone, g."PULocationID" 
ORDER BY sum_amount DESC
LIMIT 3;
```

## Question 6. Largest tip
For the passengers picked up in Ocrober 2019 in the zone name "East Harlem North" which was the drop off zone that had the largest tip?

Solution : JFK Airport

```sql
SELECT 
	g."PULocationID", 
	g."DOLocationID", 
	g.lpep_pickup_datetime, 
	g.tip_amount, 
	z."Zone" AS pickup_zone 
FROM public.green_taxi_data g
JOIN public.zone_data z
ON g."DOLocationID" = z."LocationID"
WHERE 
(g.lpep_pickup_datetime::date BETWEEN '2019-10-01' AND '2019-10-31')
AND g."PULocationID" = 74
ORDER BY tip_amount DESC
LIMIT 1;
```
