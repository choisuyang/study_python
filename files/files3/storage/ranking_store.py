"""랭킹 데이터(ranking.json) 읽기/쓰기/정렬/삭제 전담 클래스.

저장 형식 (플레이어 이름이 key):
{
  "홍길동": {"best_rate": 66.7, "wins": 4, "total": 6, "photo": "photos/photo_xxx.png"}
}
"""
import json
import shutil

from config import MAX_RANK, PHOTO_DIR, RANK_FILE


class RankingStore:
    def __init__(self, rank_file=RANK_FILE, photo_dir=PHOTO_DIR):
        self.rank_file = rank_file
        self.photo_dir = photo_dir
        self.data = self._load()

    # ---------- 파일 입출력 ----------
    def _load(self):
        """파일이 없거나 깨져 있으면 빈 랭킹으로 시작한다."""
        try:
            with open(self.rank_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            return {}

    def save(self):
        with open(self.rank_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    # ---------- 조회 ----------
    def get(self, name):
        """플레이어 기록 1건 (없으면 None)"""
        return self.data.get(name)

    def top(self, limit=MAX_RANK):
        """최고 승률 순 [(이름, 기록), ...] — 승률이 같으면 대결 수가 많은 쪽이 위"""
        items = sorted(self.data.items(),
                       key=lambda kv: (kv[1]["best_rate"], kv[1]["total"]),
                       reverse=True)
        return items[:limit]

    # ---------- 변경 ----------
    def update_best(self, name, rate, wins, total):
        """플레이어의 최고 승률 기록을 갱신한다. (기존 사진 경로는 새 사진을 찍기 전까지 유지)"""
        old = self.data.get(name)
        self.data[name] = {
            "best_rate": rate,
            "wins": wins,
            "total": total,
            "photo": old["photo"] if old else None,
        }
        self.save()

    def set_photo(self, name, rel_path):
        """플레이어 기록에 기념사진 경로(상대 경로)를 연결한다."""
        self.data[name]["photo"] = rel_path
        self.save()

    def clear(self):
        """랭킹 전체 + 저장된 사진 폴더를 삭제한다."""
        self.data = {}
        self.save()
        shutil.rmtree(self.photo_dir, ignore_errors=True)
        # self.photo_dir에 지정된 폴더와 그안의 모든 폴더안에 사진파일 삭제
