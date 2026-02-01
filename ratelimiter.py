from datetime import datetime, timezone
from db import get_db

RATE_LIMIT = 5  # requests
WINDOW_SECONDS = 3600  # 1 hour

def get_window_start():
    now = datetime.now(timezone.utc)
    return now.replace(minute=0, second=0, microsecond=0)

def rate_limit(user_id, api_name):
    window_start = get_window_start()
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT request_count
        FROM rate_limit
        WHERE user_id=%s AND api_name=%s AND window_start=%s
    """, (user_id, api_name, window_start))

    row = cursor.fetchone()

    if row:
        current_count = row[0]
        if current_count >= RATE_LIMIT:
            cursor.close()
            conn.close()
            return False, current_count 
            
        cursor.execute("""
            UPDATE rate_limit
            SET request_count = request_count + 1
            WHERE user_id=%s AND api_name=%s AND window_start=%s
            """, (user_id, api_name, window_start))
        current_count += 1
    else:
        cursor.execute("""
            INSERT INTO rate_limit(user_id, api_name, window_start, request_count)
            VALUES (%s, %s, %s, 1)    
        """, (user_id, api_name, window_start))
        current_count = 1
        
    conn.commit()
    cursor.close()
    conn.close()
    return True, current_count
