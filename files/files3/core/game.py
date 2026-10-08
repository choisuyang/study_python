"""가위바위보 규칙과 전적 계산 (화면/PyQt 코드가 전혀 없는 순수 로직).

그래서 UI 없이도 단독으로 테스트할 수 있습니다.
"""
import random

# 선택지: 이름 -> 이모지
CHOICES = {"가위": "✌️", "바위": "✊", "보": "✋"}
# 키가 값을 이긴다 (가위는 보를, 바위는 가위를, 보는 바위를 이김)
BEATS = {"가위": "보", "바위": "가위", "보": "바위"}


def random_choice():
    """컴퓨터의 선택을 무작위로 뽑는다."""
    return random.choice(list(CHOICES))


def judge(player, computer):
    """플레이어 입장에서 '승리' / '패배' / '무승부' 를 돌려준다."""
    if player == computer:
        return "무승부"
    return "승리" if BEATS[player] == computer else "패배"


class GameStats:
    """현재 플레이어의 승/패/무 기록과 승률을 관리한다."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.wins = 0
        self.losses = 0
        self.draws = 0

    def add(self, result):
        """대결 결과('승리'/'패배'/'무승부')를 한 판 반영한다."""
        if result == "승리":
            self.wins += 1
        elif result == "패배":
            self.losses += 1
        else:
            self.draws += 1

    @property
    def total(self):
        """총 대결 수"""
        return self.wins + self.losses + self.draws

    @property
    def win_rate(self):
        """승률(%) = 승리 / 전체 대결 수 (무승부도 전체에 포함)"""
        return (self.wins / self.total * 100) if self.total else 0.0
