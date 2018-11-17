CREATE TABLE course_types
(
  id   INTEGER      NOT NULL,
  name VARCHAR(255) NOT NULL,
  PRIMARY KEY (id AUTOINCREMENT)
);

CREATE TABLE horses
(
  id          INTEGER NOT NULL,
  url         VARCHAR(255),
  total_races INTEGER,
  total_wins  INTEGER,
  sex         VARCHAR(255),
  age         INTEGER,
  user_rating REAL,
  PRIMARY KEY (id AUTOINCREMENT)
);

CREATE TABLE jockeys
(
  id                              INTEGER NOT NULL,
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

CREATE TABLE racetracks
(
  id   INTEGER      NOT NULL,
  name VARCHAR(255) NOT NULL,
  PRIMARY KEY (id AUTOINCREMENT)
);

CREATE TABLE races
(
  id              INTEGER NOT NULL,
  racetrack_id    INTEGER NOT NULL,
  course_type_id  INTEGER NOT NULL,
  weather         VARCHAR(255),
  direction       VARCHAR(255),
  track_condition VARCHAR(255),
  url             VARCHAR(255),
  distance        INTEGER,
  date            DATE,
  PRIMARY KEY (id AUTOINCREMENT),
  constraint races_racetracks_id_fk
  foreign key (racetrack_id) references racetracks,
  constraint races_course_types_id_fk
  foreign key (course_type_id) references course_types
);

CREATE TABLE trainers
(
  id                              INTEGER NOT NULL,
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

CREATE TABLE race_contenders
(
  id                INTEGER NOT NULL,
  horse_id          INTEGER NOT NULL,
  jockey_id         INTEGER NOT NULL,
  trainer_id        INTEGER NOT NULL,
  weight_carried    REAL,
  post_position     INTEGER,
  order_of_finish   INTEGER,
  finish_time       INTEGER,
  horse_weight      INTEGER,
  horse_weight_diff INTEGER,
  popularity        INTEGER,
  first_place_odds  REAL,
  race_id           INTEGER,
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
