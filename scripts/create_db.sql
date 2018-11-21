CREATE TABLE course_types
(
  id   INTEGER      NOT NULL,
  name VARCHAR(255) NOT NULL,
  PRIMARY KEY (id AUTOINCREMENT)
);

CREATE TABLE horses
(
  id          INTEGER      NOT NULL,
  key         VARCHAR(255) NOT NULL,
  url         VARCHAR(255),
  total_races INTEGER,
  total_wins  INTEGER,
  sex         VARCHAR(255),
  birthday    DATE,
  user_rating REAL,
  PRIMARY KEY (id AUTOINCREMENT)
);

CREATE UNIQUE INDEX horses_key_uindex
  ON horses (key);

CREATE TABLE jockeys
(
  id                              INTEGER      NOT NULL,
  key                             VARCHAR(255) NOT NULL,
  url                             VARCHAR(255),
  career_1st_place_count          INTEGER,
  career_2nd_place_count          INTEGER,
  career_3rd_place_count          INTEGER,
  career_4th_place_or_below_count INTEGER,
  career_turf_race_count          INTEGER,
  career_turf_win_count           INTEGER,
  career_dirt_race_count          INTEGER,
  career_dirt_win_count           INTEGER,
  career_1st_place_rate           REAL,
  career_1st_2nd_place_rate       REAL,
  career_any_place_rate           REAL,
  career_earnings                 REAL,
  PRIMARY KEY (id AUTOINCREMENT)
);

CREATE UNIQUE INDEX jockeys_key_uindex
  ON jockeys (key);

CREATE TABLE racetracks
(
  id   INTEGER      NOT NULL,
  name VARCHAR(255) NOT NULL,
  PRIMARY KEY (id AUTOINCREMENT)
);

CREATE TABLE races
(
  id                                   INTEGER      NOT NULL,
  key                                  VARCHAR(255) NOT NULL,
  racetrack_id                         INTEGER      NOT NULL,
  course_type_id                       INTEGER      NOT NULL,
  weather                              VARCHAR(255),
  url                                  VARCHAR(255),
  distance                             INTEGER,
  date                                 DATE,
  dirt_condition                       VARCHAR(255),
  turf_condition                       VARCHAR(255),

  -- 負担重量 (馬齢|定量|別定|ハンデ)
  impost_category                      VARCHAR(255),

  -- (指定) [地]が出走できるレースで、かつ地方競馬所属の騎手が騎乗できる(特指)以外のレース
  is_non_winner_regional_horse_allowed TINYINT,

  -- (特指) JRAが認定した地方競馬の競走で第1着となった[地]が出走できるレースで、かつ地方競馬所属の騎手が騎乗できるレース
  is_winner_regional_horse_allowed     TINYINT,

  -- [指定] 地方競馬所属の騎手が騎乗できるレース
  is_regional_jockey_allowed           TINYINT,

  -- (混合) 内国産馬にマル外が混合して出走できるレースのこと
  is_foreign_horse_allowed             TINYINT,

  -- (国際) 内国産馬に(外)および[外]が混合して出走できるレース
  is_foreign_horse_and_trainer_allowed TINYINT,

  -- (見習騎手) 若手騎手が騎乗できるレース
  is_apprentice_jockey_allowed         TINYINT,

  -- (牝) 牝馬しか出走できないレース
  is_female_only                       TINYINT,

  PRIMARY KEY (id AUTOINCREMENT),
  constraint races_racetracks_id_fk
  foreign key (racetrack_id) references racetracks,
  constraint races_course_types_id_fk
  foreign key (course_type_id) references course_types
);

CREATE UNIQUE INDEX races_key_uindex
  ON races (key);

CREATE TABLE trainers
(
  id                              INTEGER      NOT NULL,
  key                             VARCHAR(255) NOT NULL,
  url                             VARCHAR(255),
  career_1st_place_count          INTEGER,
  career_2nd_place_count          INTEGER,
  career_3rd_place_count          INTEGER,
  career_4th_place_or_below_count INTEGER,
  career_turf_race_count          INTEGER,
  career_turf_win_count           INTEGER,
  career_dirt_race_count          INTEGER,
  career_dirt_win_count           INTEGER,
  career_1st_place_rate           REAL,
  career_1st_2nd_place_rate       REAL,
  career_any_place_rate           REAL,
  career_earnings                 REAL,
  PRIMARY KEY (id AUTOINCREMENT)
);

CREATE UNIQUE INDEX trainers_key_uindex
  ON trainers (key);

CREATE TABLE race_contenders
(
  id                      INTEGER NOT NULL,
  horse_id                INTEGER NOT NULL,
  jockey_id               INTEGER NOT NULL,
  trainer_id              INTEGER NOT NULL,
  race_id                 INTEGER NOT NULL,
  weight_carried          REAL,
  post_position           INTEGER,
  order_of_finish         INTEGER,
  order_of_finish_lowered TINYINT,
  finish_time             INTEGER,
  horse_weight            INTEGER,
  horse_weight_diff       INTEGER,
  popularity              INTEGER,
  first_place_odds        REAL,
  PRIMARY KEY (id AUTOINCREMENT),
  constraint race_contenders_horses_id_fk
  foreign key (horse_id) references horses,
  constraint race_contenders_jockeys_id_fk
  foreign key (jockey_id) references jockeys,
  constraint race_contenders_trainers_id_fk
  foreign key (trainer_id) references trainers,
  constraint race_contenders_races_id_fk
  foreign key (race_id) references races
);

CREATE UNIQUE INDEX race_contenders_horse_id_jockey_id_trainer_id_race_id_uindex
  ON race_contenders (horse_id, jockey_id, trainer_id, race_id);

INSERT INTO course_types (name) VALUES
  ('turf'),
  ('dirt'),
  ('obstacle');

INSERT INTO racetracks (name)
VALUES
  ('sapporo'),
  ('hakodate'),
  ('fuma'),
  ('niigata'),
  ('tokyo'),
  ('nakayama'),
  ('chukyo'),
  ('kyoto'),
  ('hanshin'),
  ('ogura');
