CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    firstname VARCHAR(40) NOT NULL,
    login VARCHAR(40) UNIQUE NOT NULL,
    passhash VARCHAR(256) NOT NULL,
    ismale INT2,
    age INT2,
    growth INT2,
    avatar BYTEA,
    link_vk TEXT,
    link_inst TEXT,
    link_num TEXT
);

CREATE TABLE IF NOT EXISTS identikit (
    id INT8 PRIMARY KEY,
    brows INT2,
    eyes INT2,
    hair INT2,
    lips INT2,
    nose INT2,
    beard INT2,
    addition INT2
);

CREATE TABLE IF NOT EXISTS form (
    id INT8 PRIMARY KEY,
    sportattitude INT2,
    hobby1 INT2,
    hobby2 INT2,
    movieattitude1 INT2,
    movieattitude2 INT2,
    litattitude1 INT2,
    litattitude2 INT2
);

CREATE TABLE IF NOT EXISTS relations (
    ourid INT8,
    theirid INT8,
    status INT2,
    PRIMARY KEY(ourid, theirid)
);
