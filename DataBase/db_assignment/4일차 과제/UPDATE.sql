USE classicmodels;
-- 고급으로 해버리기~
-- (1) orders 테이블에서 지난 해의 모든 주문 상태를 갱신하세요.
-- (2) orderdetails 테이블에서 특정 주문의 모든 상세 정보를 갱신하세요.
-- (3) payments 테이블에서 지난 달의 모든 지불 내역을 갱신하세요.
-- (4) productlines 테이블에서 모든 제품 라인의 정보를 갱신하세요.
-- (5) customers 테이블에서 모든 고객의 주소를 갱신하세요.

-- 세이프 모드 때문에 변경이 안되니까 비활성화
SET SQL_SAFE_UPDATES = 0;

UPDATE orders
SET status = 'ON HOLD'
WHERE orderDate BETWEEN '2003-01-01' AND '2003-12-31';

-- DECIMAL(10,2)으로 제한된 스키마 때문에 ROUND함수로 자릿수를 맞춰주지 않으면 에러가 난다
UPDATE orderdetails
SET priceEach = ROUND(priceEach * 1.2, 2)
WHERE orderNumber = '10100';

UPDATE payments
SET paymentDate = '2024-11-03'
WHERE paymentDate BETWEEN '2003-01-01' AND '2003-12-31';

UPDATE productlines
SET image = '비둘?'
WHERE productLine IN (SELECT productLine FROM products WHERE quantityInStock > 10);
-- products 컬럼에 있는 quantittyInStock이 10 이상이면 productline 컬럼으로 조회하는데 조회한 자료와 productline과 일치하면 UPDATE한다

UPDATE customers
SET addressLine2 = '비둙?999'
WHERE customerNumber BETWEEN 100 AND 200;

SELECT * FROM customers;