CREATE TABLE IF NOT EXISTS chats (
    id          BIGINT                                  PRIMARY KEY,
    title       VARCHAR                     NOT NULL,
    created_at  TIMESTAMP WITH TIME ZONE    NOT NULL,
    updated_at  TIMESTAMP WITH TIME ZONE    NOT NULL,
    type        VARCHAR                     NOT NULL
);


CREATE TABLE IF NOT EXISTS users (
    id              BIGINT                                  PRIMARY KEY,
    username        VARCHAR                     NOT NULL,
    first_name      VARCHAR,
    last_name       VARCHAR,
    language_code   VARCHAR,
    created_at      TIMESTAMP WITH TIME ZONE    NOT NULL,
    updated_at      TIMESTAMP WITH TIME ZONE    NOT NULL,
    deleted_at      TIMESTAMP WITH TIME ZONE,
    role            VARCHAR                     NOT NULL
);



CREATE TABLE IF NOT EXISTS messages (
    id              BIGINT                                  PRIMARY KEY,
    chat_id         BIGINT                      NOT NULL,
    user_id         BIGINT                      NOT NULL,
    text TEXT                                   NOT NULL,
    created_at      TIMESTAMP WITH TIME ZONE    NOT NULL,
    updated_at      TIMESTAMP WITH TIME ZONE    NOT NULL,
    deleted_at      TIMESTAMP WITH TIME ZONE,
    whine_value     FLOAT                       NOT NULL,
    old_versions    JSONB                       NOT NULL,
    FOREIGN KEY (chat_id) REFERENCES chats (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);
