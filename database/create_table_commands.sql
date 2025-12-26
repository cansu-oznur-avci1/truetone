CREATE TABLE "feedback_feedback" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "raw_text" text NOT NULL,           -- Ensures feedback content is never empty
    "normalized_text" text NOT NULL,  -- Ensures processed feedback is stored
    "category" varchar(20) NOT NULL,
    "severity" integer NOT NULL,        -- Domain Integrity
    "tone" varchar(20) NOT NULL,          -- Domain Integrity
    "intent" varchar(20) NOT NULL,        -- Domain Integrity
    "date" datetime NOT NULL,
    "service_id" bigint NOT NULL 
        REFERENCES "services_service" ("id"), -- Referential Integrity
    "user_id" bigint NOT NULL 
        REFERENCES "accounts_user" ("id"),    -- Referential Integrity
    
);

CREATE TABLE "services_service" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(100) NOT NULL,
    "category" varchar(50) NOT NULL,
    "description" text NOT NULL,
    "owner_id" bigint NOT NULL 
        REFERENCES "accounts_user" ("id") -- Ensures every service has an owner
);

CREATE TABLE "accounts_user" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "username" varchar(50) NOT NULL UNIQUE, -- Ensures usernames are unique
    "email" varchar(100) NOT NULL UNIQUE,   -- Ensures emails are unique
    "password" varchar(128) NOT NULL,
    "role" varchar(10) NOT NULL              -- Domain Integrity
);

CREATE TABLE "auth_group" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(150) NOT NULL UNIQUE
);

CREATE TABLE "accounts_user_groups" (
    "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") ON DELETE CASCADE,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id") ON DELETE CASCADE,
    PRIMARY KEY ("user_id", "group_id")
);
