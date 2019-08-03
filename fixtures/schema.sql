CREATE TABLE code_table(
    code INTEGER NOT NULL,
    data TEXT,
    version INTEGER NOT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY(code, version)
) WITHOUT ROWID;
