CREATE TABLE course_types
(
  id   INTEGER NOT NULL,
  name VARCHAR(255) DEFAULT '' NOT NULL,
  PRIMARY KEY (id AUTOINCREMENT)
);

CREATE TABLE horses
(
  id          INTEGER NOT NULL,
  url         VARCHAR(255) DEFAULT '' NOT NULL,
  total_races INTEGER NOT NULL,
  total_wins  INTEGER NOT NULL,
  sex         VARCHAR(255) DEFAULT '' NOT NULL,
  age         INTEGER NOT NULL,
  user_rating REAL,
  PRIMARY KEY (id AUTOINCREMENT)
);

CREATE TABLE jockeys
(
  id                              INTEGER NOT NULL,
  career_1st_place_count          INTEGER NOT NULL,
  career_2nd_place_count          INTEGER NOT NULL,
  career_3rd_place_count          INTEGER NOT NULL,
  career_4th_place_or_below_count INTEGER NOT NULL,
  career_turf_race_count          INTEGER NOT NULL,
  career_turf_win_count           INTEGER NOT NULL,
  career_dirt_race_count          INTEGER NOT NULL,
  career_dirt_win_count           INTEGER NOT NULL,
  career_1st_place_rate           REAL    NOT NULL,
  career_1st_2nd_place_rate       REAL    NOT NULL,
  career_any_place_rate           REAL    NOT NULL,
  career_earnings                 INTEGER NOT NULL,
  PRIMARY KEY (id AUTOINCREMENT)
);

CREATE TABLE racetracks
(
  id   INTEGER NOT NULL,
  name VARCHAR(255) DEFAULT '' NOT NULL,
  PRIMARY KEY (id AUTOINCREMENT)
);

CREATE TABLE races
(
  id              INTEGER NOT NULL,
  racetrack_id    INTEGER NOT NULL,
  weather         VARCHAR(255) DEFAULT '' NOT NULL,
  direction       VARCHAR(255) DEFAULT '' NOT NULL,
  track_condition VARCHAR(255) DEFAULT '' NOT NULL,
  course_type_id  INTEGER NOT NULL,
  url             VARCHAR(255) DEFAULT '' NOT NULL,
  distance        INTEGER NOT NULL,
  date            DATE    NOT NULL,
  PRIMARY KEY (id AUTOINCREMENT),
  constraint races_racetracks_id_fk
  foreign key (racetrack_id) references racetracks,
  constraint races_course_types_id_fk
  foreign key (course_type_id) references course_types
);

CREATE TABLE trainers
(
  id                              INTEGER NOT NULL,
  career_1st_place_count          INTEGER NOT NULL,
  career_2nd_place_count          INTEGER NOT NULL,
  career_3rd_place_count          INTEGER NOT NULL,
  career_4th_place_or_below_count INTEGER NOT NULL,
  career_turf_race_count          INTEGER NOT NULL,
  career_turf_win_count           INTEGER NOT NULL,
  career_dirt_race_count          INTEGER NOT NULL,
  career_dirt_win_count           INTEGER NOT NULL,
  career_1st_place_rate           REAL    NOT NULL,
  career_1st_2nd_place_rate       REAL    NOT NULL,
  career_any_place_rate           REAL    NOT NULL,
  career_earnings                 INTEGER NOT NULL,
  PRIMARY KEY (id AUTOINCREMENT)
);

CREATE TABLE race_contenders
(
  id                INTEGER NOT NULL,
  horse_id          INTEGER NOT NULL,
  jockey_id         INTEGER NOT NULL,
  trainer_id        INTEGER NOT NULL,
  weight_carried    REAL    NOT NULL,
  post_position     INTEGER NOT NULL,
  order_of_finish   INTEGER NOT NULL,
  finish_time       INTEGER NOT NULL,
  horse_weight      INTEGER NOT NULL,
  horse_weight_diff INTEGER NOT NULL,
  popularity        INTEGER NOT NULL,
  first_place_odds  REAL    NOT NULL,
  race_id           INTEGER NOT NULL,
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
