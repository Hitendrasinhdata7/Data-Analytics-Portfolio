--CREATE TABLE Employees (
--    EmployeeID INT PRIMARY KEY ,
--    FirstName VARCHAR(50),
--    LastName VARCHAR(50),
--    Gender VARCHAR(10),
--    StartDate DATE,
--    Years INT,
--    Department VARCHAR(50),
--    Country VARCHAR(50),
--    Center VARCHAR(50),
--    MonthlySalary DECIMAL(10, 2),
--    AnnualSalary DECIMAL(12, 2),
--    JobRate INT,
--    SickLeaves INT,
--    UnpaidLeaves INT,
--    OvertimeHours INT
--);

-------------------1. Average Employee Tenure----------
SELECT 
    AVG(Years) AS AverageTenure
FROM 
    Employees;


----------2. Department-wise Performance Ratings----------
SELECT 
    Department, 
    AVG(JobRate) AS AveragePerformanceRating
FROM 
    Employees
GROUP BY 
    Department
ORDER BY 
    AveragePerformanceRating DESC;


---------3. Employee Attrition Rate by Department----------
SELECT 
    Department,
    COUNT(EmployeeID) AS TotalEmployees,
    SUM(CASE WHEN Years < 5 THEN 1 ELSE 0 END) AS AttritionCount,
    (SUM(CASE WHEN Years < 5 THEN 1 ELSE 0 END) / COUNT(EmployeeID)) * 100 AS AttritionRate
FROM 
    Employees
GROUP BY 
    Department
ORDER BY 
    AttritionRate DESC;




----------4. Employee Sick Leave Analysis------------
SELECT 
    Department, 
    AVG(SickLeaves) AS AvgSickLeaves
FROM 
    Employees
GROUP BY 
    Department
ORDER BY 
    AvgSickLeaves DESC;

---------------5. Overtime Hours Analysis-----------
SELECT 
    FirstName, 
    LastName, 
    Department, 
    OvertimeHours, 
    JobRate
FROM 
    Employees
ORDER BY 
    OvertimeHours DESC


-------------6. Performance and Salary Correlation---------
SELECT 
    AVG(JobRate) AS AvgPerformance, 
    AVG(MonthlySalary) AS AvgMonthlySalary, 
    AVG(AnnualSalary) AS AvgAnnualSalary
FROM 
    Employees;



--------------7. Employees with Unpaid Leaves Above Average--------
WITH AvgUnpaidLeaves AS (
    SELECT AVG(UnpaidLeaves) AS avg_unpaid FROM Employees
)
SELECT 
    FirstName, 
    LastName, 
    UnpaidLeaves
FROM 
    Employees, AvgUnpaidLeaves
WHERE 
    UnpaidLeaves > avg_unpaid;



	
------------8. Department with the Most Overtime Hours----------
SELECT 
    Department, 
    SUM(OvertimeHours) AS TotalOvertime
FROM 
    Employees
GROUP BY 
    Department
ORDER BY 
    TotalOvertime DESC



------------9. Highest Paid Employees by Department------------
SELECT 
    E.Department, 
    E.FirstName, 
    E.LastName, 
    E.MonthlySalary
FROM 
    Employees E
JOIN (
    SELECT 
        Department, 
        MAX(MonthlySalary) AS MaxSalary
    FROM 
        Employees
    GROUP BY 
        Department
) AS MaxSalaries
    ON E.Department = MaxSalaries.Department 
    AND E.MonthlySalary = MaxSalaries.MaxSalary
ORDER BY 
    E.Department;


----10. Performance Review Distribution Across Departments----
SELECT 
    Department, 
    JobRate, 
    COUNT(*) AS CountOfEmployees
FROM 
    Employees
GROUP BY 
    Department, JobRate
ORDER BY 
    Department, JobRate;




---------Fast Query Using a JOIN with Aggregates (Optimized for Performance)----------
SELECT 
    E.Department, 
    E.FirstName, 
    E.LastName, 
    E.MonthlySalary
FROM 
    Employees E
JOIN (
    SELECT 
        Department, 
        MAX(MonthlySalary) AS MaxSalary
    FROM 
        Employees
    GROUP BY 
        Department
) AS MaxSalaries
    ON E.Department = MaxSalaries.Department 
    AND E.MonthlySalary = MaxSalaries.MaxSalary
ORDER BY 
    E.Department;



-----Query Using HAVING (Takes More Time)--------
SELECT 
    Department, 
    FirstName, 
    LastName, 
    MonthlySalary
FROM 
    Employees E1
GROUP BY 
    Department, 
    FirstName, 
    LastName, 
    MonthlySalary
HAVING 
    MonthlySalary = (
        SELECT 
            MAX(MonthlySalary)
        FROM 
            Employees E2
        WHERE 
            E2.Department = E1.Department
    )
ORDER BY 
    Department;

