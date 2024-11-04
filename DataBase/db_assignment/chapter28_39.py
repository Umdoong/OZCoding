import pymysql

# execute로 쿼리를 보내는 것을 재활용하기 위해서 함수로 만들었다.
def execute_query(connection, query, args=None): # 정규표현식으로 값을 주기 위해 args를 매개변수로 넣어줌 기본값은 None
    with connection.cursor() as cursor:
        cursor.execute(query, args or ())
        if query.strip().upper().startswith('SELECT'):
            return cursor.fetchall()
        else:
            connection.commit()

def main():
	# cursor.close()로 닫아줄 필요 없게 with로 connect를 해준다.
	with pymysql.connect(host='localhost',
						 user='root',
						 password='0000',
						 db='airbnb',
						 charset='utf8mb4',
						 cursorclass=pymysql.cursors.DictCursor) as connection:

	# 1. 새로운 제품 추가 : Python 스크립트를 사용하여 'Products'테이블에 새로운 제품을 추가하세요.
	#						예를 들어, "Python Book"이라는 이름의 제품을 29.99달러 가격으로 추가합니다.

		execute_query(connection,'INSERT INTO Products(productName, price, stockQuantity)'
										  'VALUES(%s, %s, %s)', ('Python_Book', '29.99', '99' ))
		print('INSERT 됐는지 확인')


	# 2. 고객 목록 조회 : 'Customers'테이블에서 모든 고객의 정보를 조회하는 Python 스크립트를 작성하세요.
		customers_list = execute_query(connection, 'SELECT * FROM Customers')
		for row in customers_list:
			print(row)


	# 3. 제품 재고 업데이트 : 제품이 주문될 때마다 'Products'테이블의 해당 제품 재고를 감소시키는 Python 스크립트를 작성하세요.
		execute_query(connection, 'UPDATE Products'
								  'SET stockQuantity = stockQuantity - %s WHERE productID = %s', (sold_count, productID))


	# 4. 고객별 총 주문 금액 게산 : 'Orders'테이블을 사용하여 각 고객별로 총 주문 금액을 계산하는 Python 스크립트를 작성하세요.
		total_amount = execute_query(connection,'SELECT c.customerID, c.customerName, SUM(totalAmount) AS total_amount '
														'FROM Customers c '
														'JOIN Orders o ON c.customerID = o.customerID '
														'GROUP BY c.customerID, c.customerName '
														'ORDER BY c.customerID ASC')
		for row in total_amount:
			print(row)


	# 5. 고객 이메일 업데이트 : 고객의 이메일 주소를 업데이트하는 Python 스크립트를 작성하세요.
	#							고객 ID를 입력받고, 새로운 이메일 주소로 업데이트 합니다.
		execute_query(connection, 'UPDATE Customers '
										  'SET email = %s '
										  'WHERE customerID = %s', ('update@update.com', '1'))


	# 6. 주문 취소 : 주문을 취소하는 Python 스크립트를 작성하세요. 주문 ID를 입력받아 해당 주문을 'Orders'테이블에서 삭제합니다.
		execute_query(connection, 'DELETE FROM Orders '
								  'WHERE orderID = %s', (cancle_order))

	# 7. 특정 제품 검색 : 제품 이름을 기반으로 'Products'테이블에서 제품을 검색하는 Python 스크립트를 작성하세요.
		product = execute_query(connection, 'SELECT * FROM Products WHERE productName LIKE %s', (productName))
		for row in product:
			print(row)

	# 8. 특정 고객의 모든 주문 조회 : 고객 ID를 기반으로 그 고객의 모든 주문을 조회하는 Python 스크립트를 작성하세요.
		customer = execute_query(connection, 'SELECT * FROM Customers WHERE customerID LIKE %s', (customerID))
		for row in customer:
			print(row)


	# 9. 가장 많이 주문한 고객 찾기 : 'Orders'테이블을 사용하여 가장 많은 주문을 한 고객을 찾는 Python 스크립트를 작성하세요.
	# 가장 많은 주문을 한 고객이 2명 이상일 경우를 생각해서 LIMIT을 쓰지 않고 orderCount가 최대인 수를 출력하도록 했다.
		rich_customer = execute_query(connection,	'SELECT c.customerName, COUNT(o.orderID) AS orderCount '
															'FROM Customers c '
															'JOIN Orders o ON c.customerID = o.customerID '
															'GROUP BY c.customerName '
															'HAVING COUNT(o.orderID) = ('            # HAVING에서 COUNT(o.orderID)가 MAX(orderCount)일 경우 출력하도록 필터링
																						'SELECT MAX(orderCount) '
																						'FROM ('
																								'SELECT COUNT(o2.orderID) AS orderCount '
																								'FROM Customers c '
																								'JOIN Orders o2 ON c.customerID = o2.customerID '
																								'GROUP BY c.customerName '
																								') AS orderCounts'
									  													') '
															'ORDER BY C.customerName'

									  )

		for row in rich_customer:
			print(row)


if __name__ == '__main__':
	main()