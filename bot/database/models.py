table_client = """
CREATE TABLE "client" (
	"user_id"	INTEGER NOT NULL,
	"balance"	INTEGER NOT NULL,
	"referrer_id"	INTEGER,
	"register_time"	TEXT NOT NULL,
	"username"	TEXT,
	"status"	TEXT NOT NULL,
	PRIMARY KEY("user_id")
)
"""

table_activated_promo = """
CREATE TABLE "activated_promo" (
	"user_id"	INTEGER NOT NULL,
	"promo"	TEXT NOT NULL
)
"""

table_completed_task = """
CREATE TABLE "completed_task" (
	"user_id"	INTEGER NOT NULL,
	"task_id"	INTEGER NOT NULL
)
"""

table_promocodes = """
CREATE TABLE "promocodes" (
	"promo"	TEXT NOT NULL,
	"reward"	INTEGER NOT NULL,
	PRIMARY KEY("promo")
)
"""

table_tasks = """
CREATE TABLE "tasks" (
	"task_id"	INTEGER NOT NULL,
	"description"	TEXT NOT NULL,
	"reward"	INTEGER NOT NULL,
	"channel_id"	TEXT,
	"file_id"	TEXT,
	PRIMARY KEY("task_id")
)
"""