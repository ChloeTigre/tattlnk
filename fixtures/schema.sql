CREATE TABLE code_index(
    code INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE code_table(
    code INTEGER NOT NULL REFERENCES code_index(code),
    data TEXT,
    version INTEGER NOT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY(code, version)
) WITHOUT ROWID;
