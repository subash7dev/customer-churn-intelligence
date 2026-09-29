-- ============================================================
-- CUSTOMER CHURN INTELLIGENCE
-- SQL BUSINESS ANALYSIS
-- ============================================================


-- 1. Total Customers

SELECT
    COUNT(*) AS total_customers
FROM customers;


-- 2. Total Churned Customers

SELECT
    COUNT(*) AS churned_customers
FROM customers
WHERE churn = 1;


-- 3. Overall Churn Rate

SELECT
    ROUND(
        100.0 * SUM(churn) / COUNT(*),
        2
    ) AS churn_rate
FROM customers;


-- 4. Average Monthly Charges

SELECT
    ROUND(
        AVG(monthlycharges),
        2
    ) AS average_monthly_charges
FROM customers;


-- 5. Churn by Contract

SELECT
    contract,
    COUNT(*) AS customers,
    SUM(churn) AS churned_customers,
    ROUND(
        100.0 * SUM(churn) / COUNT(*),
        2
    ) AS churn_rate
FROM customers
GROUP BY contract
ORDER BY churn_rate DESC;


-- 6. Churn by Internet Service

SELECT
    internetservice,
    COUNT(*) AS customers,
    SUM(churn) AS churned_customers,
    ROUND(
        100.0 * SUM(churn) / COUNT(*),
        2
    ) AS churn_rate
FROM customers
GROUP BY internetservice
ORDER BY churn_rate DESC;


-- 7. Churn by Payment Method

SELECT
    paymentmethod,
    COUNT(*) AS customers,
    SUM(churn) AS churned_customers,
    ROUND(
        100.0 * SUM(churn) / COUNT(*),
        2
    ) AS churn_rate
FROM customers
GROUP BY paymentmethod
ORDER BY churn_rate DESC;


-- 8. Average Charges by Churn

SELECT
    churn,
    COUNT(*) AS customers,
    ROUND(
        AVG(monthlycharges),
        2
    ) AS avg_monthly_charges,
    ROUND(
        AVG(totalcharges),
        2
    ) AS avg_total_charges
FROM customers
GROUP BY churn;


-- 9. Churn by Tenure

SELECT
    CASE
        WHEN tenure <= 6
            THEN '0-6 Months'

        WHEN tenure <= 12
            THEN '7-12 Months'

        WHEN tenure <= 24
            THEN '13-24 Months'

        WHEN tenure <= 48
            THEN '25-48 Months'

        ELSE '49-72 Months'
    END AS tenure_group,

    COUNT(*) AS customers,

    SUM(churn) AS churned_customers,

    ROUND(
        100.0 * SUM(churn) / COUNT(*),
        2
    ) AS churn_rate

FROM customers

GROUP BY
    CASE
        WHEN tenure <= 6
            THEN '0-6 Months'

        WHEN tenure <= 12
            THEN '7-12 Months'

        WHEN tenure <= 24
            THEN '13-24 Months'

        WHEN tenure <= 48
            THEN '25-48 Months'

        ELSE '49-72 Months'
    END

ORDER BY churn_rate DESC;


-- 10. Revenue Associated With Churn

SELECT
    ROUND(
        SUM(monthlycharges),
        2
    ) AS monthly_revenue_at_risk

FROM customers

WHERE churn = 1;

-- ============================================================
-- ADVANCED BUSINESS ANALYSIS
-- ============================================================


-- 11. Churn by Gender

SELECT
    gender,
    COUNT(*) AS customers,
    SUM(churn) AS churned_customers,

    ROUND(
        100.0 * SUM(churn) / COUNT(*),
        2
    ) AS churn_rate

FROM customers

GROUP BY gender

ORDER BY churn_rate DESC;


-- 12. Churn by Senior Citizen

SELECT
    seniorcitizen,
    COUNT(*) AS customers,
    SUM(churn) AS churned_customers,

    ROUND(
        100.0 * SUM(churn) / COUNT(*),
        2
    ) AS churn_rate

FROM customers

GROUP BY seniorcitizen

ORDER BY churn_rate DESC;


-- 13. Churn by Tech Support

SELECT
    techsupport,
    COUNT(*) AS customers,
    SUM(churn) AS churned_customers,

    ROUND(
        100.0 * SUM(churn) / COUNT(*),
        2
    ) AS churn_rate

FROM customers

GROUP BY techsupport

ORDER BY churn_rate DESC;


-- 14. High-Value Churned Customers

SELECT
    customerid,
    tenure,
    contract,
    internetservice,
    monthlycharges,
    totalcharges

FROM customers

WHERE churn = 1

ORDER BY monthlycharges DESC

LIMIT 20;


-- 15. Customers With High Charges and Short Tenure

SELECT
    customerid,
    tenure,
    monthlycharges,
    contract,
    internetservice,
    churn

FROM customers

WHERE tenure <= 12

AND monthlycharges >= (
    SELECT AVG(monthlycharges)
    FROM customers
)

ORDER BY monthlycharges DESC;


-- 16. Revenue by Contract

SELECT
    contract,

    COUNT(*) AS customers,

    ROUND(
        SUM(monthlycharges),
        2
    ) AS monthly_revenue,

    ROUND(
        AVG(monthlycharges),
        2
    ) AS average_monthly_charge

FROM customers

GROUP BY contract

ORDER BY monthly_revenue DESC;


-- 17. Churned Revenue Percentage

SELECT

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN churn = 1
                THEN monthlycharges
                ELSE 0
            END
        )
        /
        SUM(monthlycharges),
        2
    ) AS revenue_percentage_from_churned_customers

FROM customers;