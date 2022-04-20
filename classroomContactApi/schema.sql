DROP TABLE IF EXISTS "fulltext";

CREATE TABLE "fulltext" (
	"id"	INTEGER,
	"comments"	TEXT,
	"subject"	TEXT NOT NULL,
	"content"	TEXT NOT NULL,
	"updated"	TEXT NOT NULL,
	PRIMARY KEY("id")
)
