import time

class Transaction():
    def __init__(self) -> None:
        self.first_party = None
        self.party_b = None
        self.content = None

    def set_content(self, content):
        self.content = content
    

class Block():
    def __init__(self) -> None:
        self.block_info = {}
        self.transaction = None
        self.timestamp = time.time()
        self.previous_hash = None
        self.voting_result = [] # 所有参与者们的投票结果 默认是通过的，只有当出现特殊情况时，区块会被用户拒绝审核
        self.permission = None  # 是否被允许加入区块链


class BlockChain():
    def __init__(self) -> None:
        self.current_chain = None
        pass

    def persistence(self):
        pass

    def load_chain(self):
        pass

    def verify_chain(self):
        pass