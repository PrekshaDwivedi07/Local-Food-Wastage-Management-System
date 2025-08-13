CREATE DATABASE Food_wastage;
USE Food_wastage;

SELECT * FROM receivers_data;
SELECT * FROM food_listings_data;
SELECT * FROM claims_data;

CREATE TABLE providers_data (
    provider_id INT PRIMARY KEY,
    name VARCHAR(100),
    type VARCHAR(500),
    address VARCHAR(255),
    city VARCHAR(500),
    contact VARCHAR(500)
);
SHOW VARIABLES LIKE 'secure_file_priv';

LOAD DATA 
INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/providers_data.csv'
INTO TABLE providers_data 
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT * FROM providers_data;

/*How many providers are there in each city*/
SELECT city , COUNT(*) AS total_providers
FROM providers_data
GROUP BY city
ORDER BY total_providers DESC;

/*How many food receivers are there in each city?*/
SELECT City, COUNT(*) AS total_receivers
FROM receivers_data
GROUP BY City
ORDER BY total_receivers DESC;

/*Which type of food provider contributes the most food listings?*/
SELECT Provider_Type, COUNT(*) AS food_listing
FROM food_listings_data
GROUP BY Provider_Type
ORDER BY food_listing DESC
LIMIT 1;

/* Contact information of food providers in a specific city*/
SELECT city,name,contact FROM providers_data;

/* Which receivers have claimed the most food?*/
SELECT r.name, COUNT(c.claim_id) AS total_claims
FROM claims_data c
JOIN receivers_data r ON c.receiver_id = r.receiver_id
GROUP BY r.name
ORDER BY total_claims DESC;

/*Total quantity of food available from all providers*/
SELECT SUM(Quantity) FROM food_listings_data;

/*7. Which city has the highest number of food listings?*/
SELECT location, COUNT(*) AS HIGHEST_NO
FROM food_listings_data
GROUP BY Location
ORDER BY HIGHEST_NO DESC
LIMIT 1; 

/*Most commonly available food types*/
SELECT Food_Type , COUNT(*) AS COUNT_OF_TYPE
FROM food_listings_data 
GROUP BY Food_Type
ORDER BY COUNT_OF_TYPE DESC
LIMIT 1;

/*How many food claims have been made for each food item*/
SELECT F.Food_Name , COUNT(C.Claim_ID) AS TOTAL_CLAIMS
FROM claims_data C 
JOIN food_listings_data F ON C.Food_ID = F.Food_ID
GROUP BY F.Food_Name
ORDER BY TOTAL_CLAIMS DESC
LIMIT 7;

/*Which provider has had the highest number of successful (Completed) food claims*/
SELECT p.name, COUNT(c.claim_id) AS successful_claims
FROM claims_data c
JOIN food_listings_data f ON c.food_id = f.food_id
JOIN providers_data p ON f.provider_id = p.provider_id
WHERE c.status = 'Completed'
GROUP BY p.name
ORDER BY successful_claims DESC
LIMIT 1;

/*Percentage of claims by status (Completed, Pending, Cancelled)*/
SELECT status,
       ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims_data)), 2) AS percentage
FROM claims_data
GROUP BY status;

/*Average quantity of food claimed per receiver*/
SELECT r.name, ROUND(AVG(f.quantity), 2) AS avg_quantity_claimed
FROM claims_data c
JOIN receivers_data r ON c.receiver_id = r.receiver_id
JOIN food_listings_data f ON c.food_id = f.food_id
GROUP BY r.name
ORDER BY avg_quantity_claimed DESC;

/*Which meal type is claimed the most?*/
SELECT f.meal_type, COUNT(c.claim_id) AS total_claims
FROM claims_data c
JOIN food_listings_data f ON c.food_id = f.food_id
GROUP BY f.meal_type
ORDER BY total_claims DESC;

/*Total quantity of food donated by each provider*/
SELECT p.name, SUM(f.quantity) AS total_quantity_donated
FROM food_listings_data f
JOIN providers_data p ON f.provider_id = p.provider_id
GROUP BY p.name
ORDER BY total_quantity_donated DESC;

/*Top 5 cities with highest demand (most claims)*/
SELECT f.location AS city, COUNT(c.claim_id) AS total_claims
FROM claims_data c
JOIN food_listings_data f ON c.food_id = f.food_id
GROUP BY f.location
ORDER BY total_claims DESC
LIMIT 5;












