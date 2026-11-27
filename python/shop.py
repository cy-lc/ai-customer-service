# 商品类：封装单个商品的名称、价格、数量
class Product:
    def __init__(self, name, price, count):
        self.name = name
        self.price = price
        self.count = count


# 购物车管理类：负责商品的添加、修改、删除、查询
class ShoppingCart:
    def __init__(self):
        self.products = []  # 用列表保存 Product 对象

    # 1. 添加商品
    def add_product(self, name, price, count):
        self.products.append(Product(name, price, count))
        print("添加成功！")

    # 2. 按名称修改商品价格、数量
    def update_product(self, name):
        for p in self.products:
            if p.name == name:
                p.price = float(input("请输入该商品的新价格："))
                p.count = int(input("请输入该商品的新数量："))
                print("修改成功！")
                return
        print("未找到该商品！")

    # 3. 按名称删除商品
    def remove_product(self, name):
        for p in self.products:
            if p.name == name:
                self.products.remove(p)
                print("删除成功！")
                return
        print("未找到该商品！")

    # 4. 查询并展示所有商品
    def show_products(self):
        if not self.products:
            print("购物车为空！")
            return
        for p in self.products:
            print(f"商品名称：{p.name}，商品价格：{p.price}，商品数量：{p.count}")


# 控制台菜单交互
def main():
    cart = ShoppingCart()
    while True:
        print("=" * 20)
        print("1. 添加购物车")
        print("2. 修改购物车")
        print("3. 删除购物车")
        print("4. 查询购物车")
        print("5. 退出购物车")
        choice = input("请输入功能序号：")

        if choice == "1":
            name = input("请输入商品名称：")
            price = float(input("请输入商品价格："))
            count = int(input("请输入商品数量："))
            cart.add_product(name, price, count)
        elif choice == "2":
            name = input("请输入要修改的商品名称：")
            cart.update_product(name)
        elif choice == "3":
            name = input("请输入要删除的商品名称：")
            cart.remove_product(name)
        elif choice == "4":
            cart.show_products()
        elif choice == "5":
            print("已退出购物车，再见！")
            break
        else:
            print("输入无效，请重新输入！")


if __name__ == "__main__":
    main()
