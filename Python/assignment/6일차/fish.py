class BungeoppangShop:

    def __init__(self):  # 생성자, stock(초기 재고), prices, sales를 초기화 하는 역할
        self.stock = {"팥붕어빵": 10, "슈크림붕어빵": 8, "초코붕어빵": 5}  # 초기재고
        self.prices = {"팥붕어빵": 1000, "슈크림붕어빵": 1200, "초코붕어빵": 1500}  # 가격
        self.sales = {"팥붕어빵": 0, "슈크림붕어빵": 0, "초코붕어빵": 0}  # 초기판매량

    def menu_list(self):  # 메뉴판
        print(f'----------\n메뉴판\n{self.prices}')

    def check_stock(self):  # 현재 붕어빵 재고 출력
        print("----------\n현재 재고")
        for i in self.stock:
            print(f'{i} {self.stock[i]}개')

    def process_order(self, bread_type, bread_count):  # 주문
        try:
            if bread_count == '취소':
                return
            bread_count = int(bread_count)
        except ValueError:
            print("잘못된 입력입니다. 숫자로 적어주세요.")
            return

        else:

            if self.stock[bread_type] >= bread_count:  # 주문한 개수가 재고 개수 이하일 때
                self.stock[bread_type] -= bread_count  # 재고 개수 주문한 개수만큼 감소
                self.sales[bread_type] += bread_count  # 판매량 주문한 개수만큼 증가
                print(f'----------\n판매완료\n{bread_type}이 {bread_count}개 판매되었습니다.')
                print(f'----------\n총 판매량\n{self.sales}')

            elif self.stock[bread_type] < bread_count:  # 주문한 개수가 재고 개수 초과일 때
                print("재고가 모자랍니다.")

    def admin_mode(self, bread_type, add_stock):  # 붕어빵 추가하는 관리자 모드
        if add_stock == '뒤로':
            return

        try:  # 붕어빵 입력 시 에러 예외 처리
            self.stock[bread_type] += int(add_stock)
        except ValueError:
            print("잘못된 입력입니다. 숫자로 적어주세요.")
        else:
            print(f'----------\n재고주문\n{bread_type}이 {add_stock}개 만큼 증가했습니다.')

        self.check_stock()

    def calculate_total_sales(self):  # 총 매출을 계산하는 함수
        total_sales = sum(self.sales[i] * self.prices[i] for i in self.prices)
        """
        total_sales = 0
        for i in prices:
            total_sales += self.sales[i] * prices[i]
        """
        print(f'----------\n총 매출\n{total_sales}원 입니다.')


    def main(self):

        while True:
            check_mode = ["메뉴", "주문", "관리자", "종료"]  # 잘못된 모드 필터
            mode = input("모드|메뉴, 주문, 관리자, 종료|")

            if not mode in check_mode:
                print("\n잘못된 모드입니다.")

            else:
                if mode == "종료":
                    self.calculate_total_sales()
                    print("\n시스템이 종료됩니다.")
                    break

                if mode == "메뉴":
                    self.menu_list()

                if mode == "주문":
                    while True:
                        bread_type = input("메뉴를 입력해주세요(메뉴판|팥붕어빵, 슈크림붕어빵, 초코붕어빵, 뒤로|")
                        if bread_type == '뒤로':
                            break
                        if not bread_type in self.stock.keys():
                            print('없는 메뉴입니다.')
                            continue
                        bread_count = input("메뉴 개수를 입력해주세요. 취소하고 싶으시면 '취소'버튼을 눌러주세요")
                        self.process_order(bread_type, bread_count)

                if mode == "관리자":
                    while True:
                        admin = input("관리자 모드|재고추가, 재고확인, 뒤로|")

                        if admin == "재고추가":
                            while True:
                                admin_bread_type = input("추가할 재고 메뉴를 입력해주세요|팥붕어빵, 슈크림붕어빵, 초코붕어빵, 뒤로|")
                                if admin_bread_type == '뒤로':
                                    break
                                if not admin_bread_type in self.stock.keys():
                                    print('없는 메뉴입니다.')
                                    continue
                                add_stock =  input("얼마나 추가할지 입력해주세요. 뒤로 가길 원하시면 '뒤로'버튼을 눌러주세요")
                                self.admin_mode(admin_bread_type, add_stock)

                        if admin == "재고확인":
                            self.check_stock()

                        if admin == '뒤로':
                            break


bbshop = BungeoppangShop()

if __name__ == "__main__":
     bbshop.main()