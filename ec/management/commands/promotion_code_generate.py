import string, random

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, IntegrityError

from ec.models import PromotionCode


class Command(BaseCommand):
    help = "Generate 10 promotion codes"

    def handle(self, *args, **options):
        # プロモーションコードを10個作成
        for _ in range(10):
            self.create_unique_promotion_code()

        self.stdout.write(
            self.style.SUCCESS("プロモーションコードを10個生成しました。")
        )

    def create_unique_promotion_code(self):
        """プロモーションコードを生成してDBに保存する"""
        while True:
            try:
                # ランダムなコード生成
                code = self.generate_random_code(
                    length=7, uppercase=True, lowercase=True, digits=True
                )
                # ランダムな割引額生成
                discount = self.generate_random_discount(min=10, max=1000)

                # トランザクション開始
                with transaction.atomic():
                    # インスタンス保存
                    PromotionCode.objects.create(code=code, discount_amount=discount)
                    break  # 成功したらループ終了

            except IntegrityError:
                # 重複エラーが発生した場合、再度コードを生成
                self.stderr.write(
                    self.style.WARNING(
                        "プロモーションコードがすでに存在します。再生成中…"
                    )
                )
            except Exception as e:
                # 予期せぬ例外が発生した場合、強制終了
                raise CommandError(f"エラーが発生しました！：{str(e)}")

    # 参考：https://gist.github.com/ysko909/083cc7726f71c75df5a25a7e633a3f32#file-get_random_string-pyc
    def generate_random_code(
        self, length=7, uppercase=True, lowercase=True, digits=True
    ):
        """指定した桁数でランダムな文字列を生成する"""
        # 桁数チェック
        if length <= 0:
            raise ValueError("桁数は1以上の整数である必要があります。")

        # 文字種別のチェック
        if not (uppercase or lowercase or digits):
            raise ValueError(
                "引数の`uppercase` `lowercase` `digits`の少なくとも1つをTrueにする必要があります。"
            )

        # ベースとなる文字列生成
        seed_string = ""
        if uppercase:
            seed_string += string.ascii_uppercase  # 大文字 A〜Z
        if lowercase:
            seed_string += string.ascii_lowercase  # 小文字 a〜z
        if digits:
            seed_string += string.digits  # 数字 0〜9

        # 桁数に応じたランダムな文字列を生成
        return "".join(random.choices(seed_string, k=length))

    def generate_random_discount(self, min=10, max=1000):
        """ランダムな割引額を生成する"""
        # 型チェック
        if not isinstance(min, int) or not isinstance(max, int):
            raise TypeError("引数の`min`および`max`は整数である必要があります。")

        # 値のチェック
        if min < 0 or min >= max:
            raise ValueError(
                "引数`min`は自然数で、`max`は`min`より大きい値である必要があります。"
            )

        # 範囲内の数値に応じたランダムな整数を生成
        return random.randint(min, max)
