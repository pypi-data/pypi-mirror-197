# mhyy.py

![LICENSE](https://img.shields.io/github/license/GuangChen2333/mhyy.py?style=flat-square)
![PyP](https://img.shields.io/pypi/v/mhyy.py?style=flat-square)
![Python](https://img.shields.io/pypi/pyversions/mhyy.py?style=flat-square)
![STARS](https://img.shields.io/github/stars/GuangChen2333/mhyy.py?style=flat-square).

Python 米哈云游（云原神）签到功能与相关方法的API

## 快速开始

- 从 `PyPi` 安装 `mhyy.py`

```shell
pip install mhyy.py
```

- 签到功能的实现

```python
from mhyy import User, Client

# 实例化一个客户端~
client = Client()

# 当然要有用户啦！
user = User(
    combo_token="",  # 对应 Headers 中的 x-rpc-combo_token
    sys_version="",  # 对应 Headers 中的 x-rpc-sys_version
    device_id="",  # 对应 Headers 中的 x-rpc-device_id
    device_name="",  # 对应 Headers 中的 x-rpc-device_name
    device_model="",  # 对应 Headers 中的 x-rpc-device_model
    nickname=""  # 这个是便于识别的昵称，选填~
)

# 执行签到并返回一个 SignInResult 对象
r = client.sign_in(user)

# 打印 SignInResult 返回的签到结果，结果是枚举 SignInResultTypes 的一个对象
print(r.result.name)
```

## 文档

### 关于 SignInResult

SignInResult 是一个只读对象，用于返回签到结果

#### 对象属性: 

- `result: SignInResultTypes` -> 签到结果
- `wallet_data: WalletData` -> 你的钱包数据
- `user: User` -> 所属用户

### 关于 WalletData

WalletData 是一个只读对象，用于返回你的钱包数据

#### 对象属性:

- `coin: int` -> 米云币
- `free_time: int` -> 免费时长
- `send_free_time: int` -> 新增的免费时长
- `is_play_card: bool` -> 是否是畅玩卡
- `coin_limit: int` -> 米云币上限
- `free_time_limit: int` -> 免费时长上限
- `user: User` -> 所属用户

#### 对象方法

- `format_free_time(__format: str) -> str` -> 获取格式化后的免费时间字符串
- `format_coin_time(__format: str) -> str` -> 获取格式化后的付费时间（米云币时间）字符串