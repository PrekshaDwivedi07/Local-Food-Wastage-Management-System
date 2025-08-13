# Local Food Waste Management - SQL Project

## Project Overview
The **Local Food Waste Management** project is a SQL-based data management and analysis system designed to help track, manage, and analyze food donations, providers, receivers, and claims.  
It focuses on reducing food waste by storing and processing data about food providers, receivers, and donation activities.

This database supports:
- Tracking **food providers** and **receivers**
- Managing **food listings**
- Recording **food claims**
- Analyzing food distribution patterns

---

## Database Structure

### **Database Name**
`Food_wastage`

### **Tables**
1. **`providers_data`**
   - Stores details of food providers including their name, type, address, city, and contact information.
2. **`receivers_data`**
   - Stores details of organizations/people receiving food.
3. **`food_listings_data`**
   - Stores details of available food, quantity, type, location, and provider.
4. **`claims_data`**
   - Stores information about claims made for food listings, including status and receiver details.

---

## Data Import
The project uses CSV files to populate the tables.  
Example for loading data into `providers_data`:
```sql
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/providers_data.csv'
INTO TABLE providers_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

---

## Key SQL Queries Included

### Data Insights
- **Providers per city**
```sql
SELECT city, COUNT(*) AS total_providers
FROM providers_data
GROUP BY city
ORDER BY total_providers DESC;
```
- **Receivers per city**
```sql
SELECT City, COUNT(*) AS total_receivers
FROM receivers_data
GROUP BY City
ORDER BY total_receivers DESC;
```
- **Top contributing food provider type**
```sql
SELECT Provider_Type, COUNT(*) AS food_listing
FROM food_listings_data
GROUP BY Provider_Type
ORDER BY food_listing DESC
LIMIT 1;
```
- **Top receiver by claims**
```sql
SELECT r.name, COUNT(c.claim_id) AS total_claims
FROM claims_data c
JOIN receivers_data r ON c.receiver_id = r.receiver_id
GROUP BY r.name
ORDER BY total_claims DESC;
```

### Performance Metrics
- Total quantity of food available  
- Most commonly available food type  
- Percentage of claims by status (Completed, Pending, Cancelled)  
- Average quantity claimed per receiver  
- Top 5 cities with highest food demand  

---

## Requirements
- **MySQL Server 8.0+**
- CSV data files for providers, receivers, food listings, and claims
- MySQL client or Workbench for executing queries

---

## How to Use
1. Clone this repository:
```bash
git clone https://github.com/yourusername/local-food-waste-management.git
```
2. Import `LocalFoodWasteManagement.sql` into MySQL:
```sql
SOURCE path_to_file/LocalFoodWasteManagement.sql;
```
3. Load the CSV data files into the respective tables.
4. Run the provided SQL queries to generate insights.

---

## Example Use Cases
- **Non-profit organizations** can identify high-demand cities.
- **Food providers** can track their donation impact.
- **Researchers** can study patterns of food distribution and wastage.

---

## License
This project is licensed under the **MIT License**.  
Feel free to use, modify, and distribute as per the license terms.

---

## Author
**Preksha Dwivedi**  
B.Tech CSE Student | Data & IoT Enthusiast
