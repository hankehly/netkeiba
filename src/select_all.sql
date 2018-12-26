SELECT
    -- race_contender
       c.id                                                          c_id,
       c.weight_carried                                              c_weight_carried,
       c.post_position                                               c_post_position,
       c.order_of_finish                                             c_order_of_finish,
       c.order_of_finish_lowered                                     c_order_of_finish_lowered,
       c.finish_time                                                 c_finish_time,
       c.horse_weight                                                c_horse_weight,
       c.horse_weight_diff                                           c_horse_weight_diff,
       c.popularity                                                  c_popularity,
       c.first_place_odds                                            c_first_place_odds,
    -- race
       r.id                                                          r_id,
       r.key                                                         r_key,
       r.distance                                                    r_distance,
       r.date                                                        r_date,

       (SELECT name FROM racetracks WHERE id = r.racetrack_id)       r_racetrack,
       (SELECT name FROM course_types WHERE id = r.course_type_id)   r_course_type,
       (SELECT name FROM weather_categories WHERE id = r.weather_id) r_weather,

       (SELECT name FROM dirt_condition_categories WHERE id = r.dirt_condition_id) r_dirt_condition,
       (SELECT name FROM turf_condition_categories WHERE id = r.turf_condition_id) r_turf_condition,
       (SELECT name FROM impost_categories WHERE id = r.impost_category_id)        r_impost_category,

       (SELECT EXISTS(SELECT id FROM non_winner_regional_horse_races WHERE race_id = r.id)) r_is_non_winner_regional_horse_allowed,
       (SELECT EXISTS(SELECT id FROM winner_regional_horse_races WHERE race_id = r.id))     r_is_winner_regional_horse_allowed,
       (SELECT EXISTS(SELECT id FROM regional_jockey_races WHERE race_id = r.id))           r_is_regional_jockey_allowed,
       (SELECT EXISTS(SELECT id FROM foreign_horse_races WHERE race_id = r.id))             r_is_foreign_horse_allowed,
       (SELECT EXISTS(SELECT id FROM foreign_trainer_horse_races WHERE race_id = r.id))     r_is_foreign_horse_and_trainer_allowed,
       (SELECT EXISTS(SELECT id FROM apprentice_jockey_races WHERE race_id = r.id))         r_is_apprentice_jockey_allowed,
       (SELECT EXISTS(SELECT id FROM female_only_races WHERE race_id = r.id))               r_is_female_only,
    -- horse
       h.id                                                          h_id,
       h.key                                                         h_key,
       h.total_races                                                 h_total_races,
       h.total_wins                                                  h_total_wins,
       (SELECT name FROM horse_sexes WHERE id = h.sex_id)            h_sex,
       h.birthday                                                    h_birthday,
       h.user_rating                                                 h_user_rating,
    -- jockey
       j.id                                                          j_id,
       j.key                                                         j_key,
    -- trainer
       t.id                                                          t_id,
       t.key                                                         t_key
FROM race_contenders c
       LEFT JOIN races r on c.race_id = r.id
       LEFT JOIN horses h on c.horse_id = h.id
       LEFT JOIN jockeys j on c.jockey_id = j.id
       LEFT JOIN trainers t on c.trainer_id = t.id
ORDER BY c_id;
