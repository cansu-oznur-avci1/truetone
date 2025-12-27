
--All Users can see his/her all feedback entries by user_id
SELECT s.name AS service_name, f.severity, f.date, f.normalized_text, f.category
FROM feedback_feedback f
JOIN services_service s ON f.service_id = s.id
WHERE f.user_id = 6;

SELECT s.name AS service_name, f.severity, f.date, f.normalized_text, f.category
FROM feedback_feedback f
JOIN services_service s ON f.service_id = s.id
WHERE f.user_id = 1;

SELECT s.name AS service_name, f.severity, f.date, f.normalized_text, f.category
FROM feedback_feedback f
JOIN services_service s ON f.service_id = s.id
WHERE f.user_id = 7;

--All Users can filter his/her feedback entries by severity level
SELECT s.name AS service_name, f.severity, f.date, f.normalized_text, f.category 
FROM feedback_feedback f
JOIN services_service s ON f.service_id = s.id
WHERE f.severity = 1;

SELECT s.name AS service_name, f.severity, f.date, f.normalized_text, f.category 
FROM feedback_feedback f
JOIN services_service s ON f.service_id = s.id
WHERE f.severity = 2;

SELECT s.name AS service_name, f.severity, f.date, f.normalized_text, f.category 
FROM feedback_feedback f
JOIN services_service s ON f.service_id = s.id
WHERE f.severity = 3;

SELECT s.name AS service_name, f.severity, f.date, f.normalized_text, f.category 
FROM feedback_feedback f
JOIN services_service s ON f.service_id = s.id
WHERE f.severity = 4;

--All Users can search his/her feedback entries by keywords in raw_text
SELECT s.name AS service_name, f.severity, f.date, f.normalized_text, f.category 
FROM feedback_feedback f
JOIN services_service s ON f.service_id = s.id
WHERE raw_text LIKE '%Wi-Fi%';

--Service Owners can see all feedback entries for services they own by the service_id
SELECT s.name AS service_name, f.severity, f.date, f.normalized_text, f.category 
FROM feedback_feedback f
JOIN services_service s ON f.service_id = s.id 
WHERE s.name = "Library";

SELECT s.name AS service_name, f.severity, f.date, f.normalized_text, f.category 
FROM feedback_feedback f
JOIN services_service s ON f.service_id = s.id 
WHERE s.name = "IT Support";

SELECT s.name AS service_name, f.severity, f.date, f.normalized_text, f.category 
FROM feedback_feedback f
JOIN services_service s ON f.service_id = s.id 
WHERE s.name = "Cafeteria";

--Admins can see all feedback entries across all services
SELECT s.name AS service_name, f.severity, f.date, f.normalized_text, f.category 
FROM feedback_feedback f
JOIN services_service s ON f.service_id = s.id

-- Admins can filter feedback entries by date range for a specific service
--Service Owners can filter feedback entries by date range for their services
SELECT f.severity, COUNT(*) AS feedback_count
FROM feedback_feedback f
JOIN services_service s ON f.service_id = s.id
WHERE s.name = 'Library' 
  AND f.date BETWEEN '2025-12-01' AND '2025-12-31'
GROUP BY f.severity;

SELECT f.severity, COUNT(*) AS feedback_count
FROM feedback_feedback f
JOIN services_service s ON f.service_id = s.id
WHERE s.name = 'IT Support' 
  AND f.date BETWEEN '2025-12-01' AND '2025-12-31'
GROUP BY f.severity;

SELECT f.severity, COUNT(*) AS feedback_count
FROM feedback_feedback f
JOIN services_service s ON f.service_id = s.id
WHERE s.name = 'Cafeteria' 
  AND f.date BETWEEN '2025-12-01' AND '2025-12-31'
GROUP BY f.severity;