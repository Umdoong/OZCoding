USE classicmodels;

-- (1) orders 테이블에서 지난 해의 모든 주문을 삭제하세요.
-- (2) orderdetails 테이블에서 가장 적게 팔린 제품의 모든 주문 상세를 삭제하세요.
-- (3) payments 테이블에서 특정 금액 이하의 모든 지불 내역을 삭제하세요.
-- (4) productlines 테이블에서 제품이 없는 모든 제품 라인을 삭제하세요.
-- (5) customers 테이블에서 최근 1년 동안 활동하지 않은 모든 고객을 삭제하세요.

-- orderNumber가 다른 column에서 FREIGN KEY로 참조되고 있어서 참조된 column을 먼저 삭제해야 삭제가 가능하다 다른 쿼리도 마찬가지
DELETE FROM orders
WHERE orderDate BETWEEN '2003-01-01' AND '2023-12-12';

DELETE FROM orderdetails
WHERE productCode IN (SELECT productCode FROM products ORDER BY quantityInStock ASC LIMIT 5);

DELETE FROM payments
WHERE amount < 10000;

DELETE FROM productlines
WHERE productlines NOT IN (SELECT DISTINCT productlines FROM products);

DELETE c
FROM customers c
JOIN orders o ON c.customerNumber = o.customerNumber
WHERE orderDate < '22-01-01';