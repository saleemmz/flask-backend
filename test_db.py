from sqlalchemy import create_engine, text

# Replace these credentials with yours if they change
DATABASE_URL = 'mysql+pymysql://saleemmz:mansnothot@localhost/SPT'

# Create the engine
engine = create_engine(DATABASE_URL)

# Connect and run a simple query
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DATABASE();"))
        print("✅ Connected to database:", result.scalar())
except Exception as e:
    print("❌ Connection failed:", e)
