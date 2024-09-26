from dataclasses import dataclass, field, asdict


@dataclass
class CartProduct:
    """カート内商品用のクラス"""

    id: int
    name: str
    price: int


@dataclass
class Cart:
    """カート用のクラス"""

    # インスタンス生成時のデフォルト値を必ず空のリストにする
    product_list: list[CartProduct] = field(default_factory=list)

    def add(self, product):
        """商品を追加する"""
        cart_product = CartProduct(
            id=product.id, name=product.name, price=product.price
        )
        self.product_list.append(cart_product)

    def clear(self):
        """カート内を空にする"""
        self.product_list.clear()

    def to_data(self):
        """セッションに格納する辞書形式に変換する"""
        return asdict(self)["product_list"]

    @classmethod
    def from_data(cls, lst):
        """セッション内に格納しておいたデータ list[dict] からCartインスタンスを作る"""
        cart = cls()
        for data in lst:
            cart_product = CartProduct(**data)
            cart.add(cart_product)
        return cart

    @classmethod
    def from_session(cls, session_data, key):
        """セッションからカートを生成"""
        # Sessionインスタンス(辞書ライクなオブジェクト)からカートデータを取得
        cart_data = session_data.get(key)
        if cart_data:
            # 既存データがあれば Cart.from_data メソッドでCartインスタンスを復元
            cart = cls.from_data(cart_data)
        else:
            # 無ければ新規
            cart = cls()
        return cart

    def save_session(self, session_data, key):
        """セッションにカートデータを保存する"""
        session_data[key] = self.to_data()

    def __str__(self):
        return f"Cart:{self.product_list}"
