CREATE TABLE IF NOT EXISTS messages(
    chatID INT8,
    chatName TEXT,
    userID INT8,
    userName TEXT,
    text TEXT,
    dt timestamp default now()
);

