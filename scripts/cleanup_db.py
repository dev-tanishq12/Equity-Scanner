import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.database import get_engine
from sqlalchemy import text

engine = get_engine()

with engine.begin() as conn:
    result = conn.execute(text("SELECT COUNT(*) as cnt FROM equity_history;"))
    current_count = result.scalar()
    print(f"Current row count: {current_count:,}")
    
    print("\nTruncating table...")
    conn.exec_driver_sql("TRUNCATE TABLE equity_history;")
    
    result = conn.execute(text("SELECT COUNT(*) as cnt FROM equity_history;"))
    new_count = result.scalar()
    print(f"After truncate: {new_count:,}")

print("\nDatabase cleaned successfully.")
