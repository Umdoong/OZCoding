USE fish_shaped_bun_shop;

-- 유저 Banana Milk를 추가해주세요
INSERT INTO users (first_name, last_name, email, password, address, contact, gender, is_active, is_staff, is_orderable) 
VALUES ('banana', 'milk', 'banana@banana.com', 'bananamilk', 'banana123', '123-4567-8910', 1, 1, 1, 1);

-- 유저 Banana Milk 주소를 변경해주세요
UPDATE users
SET address = 'banana_scholl'
WHERE first_name = 'banana'; 

-- 유저 Banana Milk 주문을 생성해주세요
INSERT INTO sales_records(user_id) -- 주문서 생성
VALUES ((SELECT id FROM users WHERE first_name = 'banana'));

-- 상세 주문 입력
INSERT INTO sales_items(sales_record_id, product_id, quantity)
VALUES (
	(SELECT id 
     FROM sales_records
     WHERE user_id = (
					(SELECT id 
                     FROM users 
                     WHERE first_name = 'banana')
                     )
	),
    (SELECT id FROM products WHERE description = "The world's best bun"),
    5
);

INSERT INTO sales_items(sales_record_id, product_id, quantity)
VALUES (
	(SELECT id 
     FROM sales_records
     WHERE user_id = (
					(SELECT id 
                     FROM users 
                     WHERE first_name = 'banana')
                     )
	),
    (SELECT id FROM products WHERE name = 'Red Bean Bun'),
    3
);

INSERT INTO sales_items(sales_record_id, product_id, quantity)
VALUES (
	(SELECT id 
     FROM sales_records
     WHERE user_id = (
					(SELECT id 
                     FROM users 
                     WHERE first_name = 'banana')
                     )
	),
    (SELECT id FROM products WHERE name = 'Fish Bun'),
    2
);

-- 판매한 재료만큼 발주이력 생성
INSERT INTO order_records(user_id, raw_material_id, quantity)
VALUES (
		(SELECT id FROM users WHERE first_name = 'banana'),
		(SELECT id FROM raw_materials WHERE name = 'Red Bean Paste'),
        3
);

INSERT INTO order_records(user_id, raw_material_id, quantity)
VALUES (
		(SELECT id FROM users WHERE first_name = 'banana'),
		(SELECT id FROM raw_materials WHERE name = 'Cream'),
        2
);

INSERT INTO order_records(user_id, raw_material_id, quantity)
VALUES (
		(SELECT id FROM users WHERE first_name = 'banana'),
		(SELECT id FROM raw_materials WHERE name = 'special'),
        5
);

-- stocks에 새로운 데이터 생성하고 daily_records에 이용이력 추가 (판매)

-- red bean
UPDATE stocks
SET quantity = quantity - (SELECT quantity FROM sales_items
							WHERE product_id = (SELECT id FROM products WHERE name = 'Red Bean Bun') 
                            ORDER BY id DESC 
                            LIMIT 1)
WHERE raw_material_id = (SELECT id FROM raw_materials WHERE name = 'Red Bean Paste');

INSERT INTO daily_records(stock_id, change_quantity, change_type)
SELECT id, quantity, 'OUT'
FROM stocks 
WHERE raw_material_id = (SELECT id FROM raw_materials WHERE name = 'Red Bean Paste');

-- cream
UPDATE stocks
SET quantity = quantity - (SELECT quantity FROM sales_items
							WHERE product_id = (SELECT id FROM products WHERE name = 'Fish Bun') 
                            ORDER BY id DESC 
                            LIMIT 1)
WHERE raw_material_id = (SELECT id FROM raw_materials WHERE name = 'Cream');

INSERT INTO daily_records(stock_id, change_quantity, change_type)
SELECT id, quantity, 'OUT'
FROM stocks 
WHERE raw_material_id = (SELECT id FROM raw_materials WHERE name = 'Cream');

-- sepcial
UPDATE stocks
SET quantity = quantity - (SELECT quantity FROM sales_items
							WHERE product_id = (SELECT id FROM products WHERE name = 'mint choco pineapple Caviar corn cheese golden bun') 
                            ORDER BY id DESC 
                            LIMIT 1)
WHERE raw_material_id = (SELECT id FROM raw_materials WHERE name = 'special');

INSERT INTO daily_records(stock_id, change_quantity, change_type)
SELECT id, quantity, 'OUT'
FROM stocks 
WHERE raw_material_id = (SELECT id FROM raw_materials WHERE name = 'special');


-- stocks에 새로운 데이터 생성하고 daily_records에 이용이력 추가 (판매한 만큼 발주)
-- red bean
UPDATE stocks
SET quantity = quantity + (SELECT quantity FROM order_records 
							WHERE raw_material_id = (SELECT id FROM raw_materials WHERE name = 'Red Bean Paste') 
                            ORDER BY id DESC -- 가장 최근 것만
                            LIMIT 1) 
WHERE raw_material_id = (SELECT id FROM raw_materials WHERE name = 'Red Bean Paste');

INSERT INTO daily_records(stock_id, change_quantity, change_type)
SELECT id, quantity, 'IN'
FROM stocks 
WHERE raw_material_id = (SELECT id FROM raw_materials WHERE name = 'Red Bean Paste');

-- cream
UPDATE stocks
SET quantity = quantity + (SELECT quantity FROM order_records 
							WHERE raw_material_id = (SELECT id FROM raw_materials WHERE name = 'Cream') 
                            ORDER BY id DESC 
                            LIMIT 1) 
WHERE raw_material_id = (SELECT id FROM raw_materials WHERE name = 'Cream');

INSERT INTO daily_records(stock_id, change_quantity, change_type)
SELECT id, quantity, 'IN'
FROM stocks 
WHERE raw_material_id = (SELECT id FROM raw_materials WHERE name = 'Cream');

-- special
UPDATE stocks
SET quantity = quantity + (SELECT quantity FROM order_records 
							WHERE raw_material_id = (SELECT id FROM raw_materials WHERE name = 'special') 
                            ORDER BY id DESC 
                            LIMIT 1) 
WHERE raw_material_id = (SELECT id FROM raw_materials WHERE name = 'special');

INSERT INTO daily_records(stock_id, change_quantity, change_type)
SELECT id, quantity, 'IN'
FROM stocks 
WHERE raw_material_id = (SELECT id FROM raw_materials WHERE name = 'special');


-- Banana Milk가 주문한 내역을 조회해주세요(단, 비싼 금액의 상품순으로 나열해주세요)
SELECT sr.id AS sales_record_id, sr.created_at, u.first_name, u.last_name, si.product_id AS product_id, SUM(si.quantity) AS total, p.price * SUM(si.quantity) AS price
FROM users u
JOIN sales_records sr ON u.id = sr.user_id
JOIN sales_items si ON sr.id = si.sales_record_id
JOIN products p ON p.id = si.product_id
WHERE u.id = 251
GROUP BY sr.id, sr.created_at, u.first_name, u.last_name, si.product_id, si.quantity
ORDER BY price DESC;