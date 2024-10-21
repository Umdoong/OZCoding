stock = { "팥붕어빵": 10, "슈크림붕어빵": 8, "초코붕어빵": 5 } # 재고
prices = { "팥붕어빵": 1000, "슈크림붕어빵": 1200, "초코붕어빵": 1500 } # 가격
sales = { "팥붕어빵": 0, "슈크림붕어빵": 0, "초코붕어빵": 0 } # 판매량

class BungeoppangShop:
    def __init__(self, stock, prices, sales):  # 생성자, stock(초기 재고), prices, sales를 초기화 하는 역할
        self.stock = stock
        self.prices = prices
        self.sales = sales

    def menu_list(self):  # 메뉴판
        print(f'----------\n메뉴판\n{self.prices}')

    def check_stock(self):  # 현재 붕어빵 재고 출력
        print("----------\n현재 재고")
        for i in self.stock:
            print(f'{i} {stock[i]}개')

    def process_order(self, bread_type, bread_count):  # 주문
        try:
            self.bread_type = bread_type
            self.bread_count = int(bread_count)
        except ValueError:
            print("잘못된 입력입니다. 숫자로 적어주세요.")
        except KeyError:
            print("없는 메뉴입니다.")

        if not self.bread_type in self.stock.keys():  # 메뉴가 있으면 not True - > elif문으로 이동
            print("메뉴가 없습니다.")  # 메뉴가 있는지 가장 먼저 검사하고 싶어서 not 사용

        elif self.stock[self.bread_type] >= self.bread_count:  # 주문한 개수가 재고 개수 이하일 때
            self.stock[self.bread_type] -= self.bread_count  # 재고 개수 주문한 개수만큼 감소
            self.sales[self.bread_type] += self.bread_count  # 판매량 주문한 개수만큼 증가
            print(f'----------\n판매완료\n{self.bread_type}이 {self.bread_count}개 판매되었습니다.')
            print(f'----------\n총 판매량\n{sales}')

        elif self.stock[self.bread_type] < self.bread_count:  # 주문한 개수가 재고 개수 초과일 때
            print("재고가 모자랍니다.")

    def admin_mode(self, bread_type, additional_stock):  # 붕어빵 추가하는 관리자 모드
        self.bread_type = bread_type
        self.additional_stock = additional_stock

        try:  # 붕어빵 입력 시 에러 예외 처리
            self.stock[bread_type] += int(self.additional_stock)
        except ValueError:
            print("잘못된 입력입니다. 숫자로 적어주세요.")
        except KeyError:
            print("없는 메뉴입니다.")
        else:
            print(f'----------\n재고주문\n{self.bread_type}이 {self.additional_stock}만큼 증가했습니다.')

        self.check_stock()

    def calculate_total_sales(self):  # 총 매출을 계산하는 함수
        total_sales = 0
        for i in prices:
            total_sales += self.sales[i] * prices[i]
        print(f'----------\n총 매출\n{total_sales}원 입니다.')


def main():
    ppang = BungeoppangShop(stock, prices, sales)

    while True:
        check_mode = ["메뉴", "주문", "관리자", "종료"]  # 잘못된 모드 필터
        mode = input("모드|메뉴, 주문, 관리자, 종료|")

        if not mode in check_mode:
            print("\n잘못된 모드입니다.")

        else:

            if mode == "종료":
                ppang.calculate_total_sales()
                print("\n시스템이 종료됩니다.")
                break

            if mode == "메뉴":
                ppang.menu_list()

            if mode == "주문":
                ppang.process_order(input("메뉴를 입력해주세요(메뉴판|팥붕어빵, 슈크림붕어빵, 초코붕어빵|"), input("메뉴 개수를 입력해주세요"))

            if mode == "관리자":
                admin = input("관리자 모드|재고추가, 재고확인|")
                if admin == "재고추가":
                    ppang.admin_mode(input("추가할 재고 메뉴를 입력해주세요|팥붕어빵, 슈크림붕어빵, 초코붕어빵|"), input("얼마나 추가할지 입력해주세요"))

                if admin == "재고확인":
                    ppang.check_stock()


if __name__ == "__main__":
    main()