import os
from pathlib import Path

# 홈 디렉토리 기준
dbt_profiles_dir = Path.home() / ".dbt"
db_file_path =  "db/hm.duckdb"

# 프로필 내용 구성
profile_content = f"""
hm_analytics:
  outputs:
    dev:
      type: duckdb
      path: {db_file_path}
      threads: 1

    prod:
      type: duckdb
      path: {db_file_path}
      threads: 4

  target: dev
"""

# 디렉토리 생성
dbt_profiles_dir.mkdir(parents=True, exist_ok=True)

# 파일 저장
profile_path = dbt_profiles_dir / "profiles.yml"
profile_path.write_text(profile_content.strip())

print(f"✅ dbt profile successfully written to: {profile_path}")
print(f"📁 Using DuckDB file path: {db_file_path}")
