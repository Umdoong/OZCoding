USE classicmodels;
-- 고급 난이도로 해버리기~
-- (1) customers 테이블에서 각 지역별 고객 수를 계산하세요.
-- (2) products 테이블에서 각 제품 카테고리별 평균 가격을 계산하세요.
-- (3) employees 테이블에서 각 부서별 직원 수를 계산하세요.
-- (4) offices 테이블에서 각 사무실별 평균 직원 연봉을 계산하세요.
-- (5) orderdetails 테이블에서 가장 많이 팔린 제품 5개를 조회하세요.

SELECT city, COUNT(*) AS customerCount
FROM customers
GROUP BY city;

SELECT productline, AVG(buyPrice) AS avgPrice
FROM products
GROUP BY productline;

SELECT o.city, COUNT(*) AS employeeCount
FROM employees e
Join offices o ON e.officeCode = o.officeCode
GROUP BY o.city;

ALTER TABLE employees ADD COLUMN `salary` VARCHAR(50);
-- 컬럼을 만들어준 후 GUI의 위대함으로 편하게 값을 넣어줬다

-- 직원 연봉을 구하라는데 연봉정보가 없다....!!
SELECT officeCode, AVG(salary) AS avgSalary
FROM employees
GROUP BY officeCode
ORDER BY avgSalary DESC;

SELECT productCode, SUM(quantityOrdered) AS totalOrdered
FROM orderdetails
GROUP BY productCode
ORDER BY totalOrdered DESC
LIMIT 5;