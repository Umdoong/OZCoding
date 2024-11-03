USE classicmodels;
-- 노가다 귀찮으니까 고급으로 해버리기~~
-- (1) customers 테이블에 새 고객을 추가하고 바로 주문을 추가하세요.
-- (2) employees 테이블에 새 직원을 추가하고 바로 그들의 매니저를 업데이트하세요.
-- (3) products 테이블에 새 제품을 추가하고 바로 그 제품에 대한 주문을 추가하세요.
-- (4) orders 테이블에 새 주문을 추가하고 바로 지불 정보를 추가하세요.
-- (5) orderdetails 테이블에 주문 상세 정보를 추가하고 바로 관련 제품의 재고를 감소시키세요.

INSERT INTO customers (customerNumber, customerName, contactLastName, contactFirstName, phone, addressLine1, addressLine2, city, state, postalCode, country, creditLimit)
VALUES (99999, '비둘기야 밥먹자', '비', '둘기', '123-456-7890', '길거리 Street', '비둘 1', 'City', 'Soeul', '99999', 'Korea', 99999.00);

INSERT INTO orders (orderNumber, orderDate, requiredDate, shippedDate, status, comments, customerNumber)
VALUES (99999, '2024-10-09', '2024-11-02', '2024-10-19', 'Shipped', '비둘기야 밥먹자', (SELECT customerNumber FROM customers WHERE customerName = '비둘기야 밥먹자'));

-- products.productLine가 FOREIGN KEY라니~~ NOT NULL 이라니~~~~~~~~~~~~~
INSERT INTO productlines (productLine, textDescription, htmlDescription, image)
VALUES ('비둘기라인', '구구구구구구구구구구구구', Null, Null);

-- orderdetails.productCode가 FOREIGN KEY라서 먼저 만들어야 됨~~ 과제 순서서로 진행이 불가능
INSERT INTO products(productCode, productName, productLine, productScale, productVendor, productDescription, quantityInStock, buyPrice, MSRP)
VALUES ('BDG_9999', '9999 MK-비둘기', '비둘기라인', '1:99', '전설의 비둘기', '999구구99999999999구구구999999999', '9999', '99.99', '999.99');

-- products.productCode가 FOREIGN KEY
INSERT INTO orderdetails (orderNumber, productCode, quantityOrdered, priceEach, orderLineNumber)
VALUES ((SELECT orderNumber From orders WHERE customerNumber = 99999), (SELECT productCode From products WHERE productName = '9999 MK-비둘기'), 99, 99, 999);

UPDATE products
SET quantityInStock = quantityInStock - 3
WHERE productCode = 'S72_3212';

INSERT INTO offices (officeCode, city, phone, addressLine1, addressLine2, state, country, postalCode, territory)
VALUES (9, '비둘동', '+9 99 9999 9999', '999 Street', 'Level 9', '비둘시', 'Korea', 99999, 'KR');

-- offices.officeCode가 FOREIGN KEY
INSERT INTO employees (employeeNumber, lastName, firstName, extension, email, officeCode, reportsTo, jobTitle)
VALUES (999, '비둘기', '매니저', 'x9999', '비둘99@비둘기999.com', (SELECT officeCode From offices WHERE addressLine2 = 'Level 9'), NULL, '비둙');

INSERT INTO payments (customerNumber, checkNumber, paymentDate, amount)
VALUES ((SELECT customerNumber FROM customers WHERE customerName = '비둘기야 밥먹자'), 'BDG999999', '2024-09-09', 99999.99);