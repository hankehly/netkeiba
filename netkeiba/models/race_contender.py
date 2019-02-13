from django.core.validators import validate_comma_separated_integer_list
from django.db import models

from netkeiba.models import BaseModel


class RaceContender(BaseModel):
    UNKNOWN = 'UNKNOWN'

    OK = 'OK'
    DISQUALIFIED = 'DISQUALIFIED'  # 失
    CANCELLED = 'CANCELLED'  # 取|除
    REMOUNT = 'REMOUNT'  # 再
    NO_FINISH = 'NO_FINISH'  # 中
    POSITION_LOWERED = 'POSITION_LOWERED'  # 降
    POSITION_STATE_CHOICES = (
        (OK, 'OK'),
        (DISQUALIFIED, 'Disqualified'),
        (CANCELLED, 'Cancelled'),
        (REMOUNT, 'Remount'),
        (NO_FINISH, 'Did not finish'),
        (POSITION_LOWERED, 'Position lowered'),
        (UNKNOWN, 'Unknown')
    )

    NOSE = 'NOSE'
    HEAD = 'HEAD'
    NECK = 'NECK'
    BS_00__1_2 = '0.5'
    BS_00__3_4 = '0.75'
    BS_01__0_0 = '1.0'
    BS_01__1_4 = '1.25'
    BS_01__1_2 = '1.5'
    BS_01__3_4 = '1.75'
    BS_02__0_0 = '2.0'
    BS_02__1_2 = '2.5'
    BS_03__0_0 = '3.0'
    BS_03__1_2 = '3.5'
    BS_04__0_0 = '4.0'
    BS_05__0_0 = '5.0'
    BS_06__0_0 = '6.0'
    BS_07__0_0 = '7.0'
    BS_08__0_0 = '8.0'
    BS_09__0_0 = '9.0'
    BS_10__0_0 = '10.0'
    LARGE = 'LARGE'
    MARGIN_CHOICES = (
        (NOSE, 'Nose'),
        (HEAD, 'Head'),
        (NECK, 'Neck'),
        (BS_00__1_2, '0.5'),
        (BS_00__3_4, '0.75'),
        (BS_01__0_0, '1.0'),
        (BS_01__1_4, '1.25'),
        (BS_01__1_2, '1.5'),
        (BS_01__3_4, '1.75'),
        (BS_02__0_0, '2.0'),
        (BS_02__1_2, '2.5'),
        (BS_03__0_0, '3.0'),
        (BS_03__1_2, '3.5'),
        (BS_04__0_0, '4.0'),
        (BS_05__0_0, '5.0'),
        (BS_06__0_0, '6.0'),
        (BS_07__0_0, '7.0'),
        (BS_08__0_0, '8.0'),
        (BS_09__0_0, '9.0'),
        (BS_10__0_0, '10.0'),
        (LARGE, 'Large'),
        (UNKNOWN, 'Unknown')
    )

    race = models.ForeignKey('netkeiba.Race', on_delete=models.CASCADE)
    horse = models.ForeignKey('netkeiba.Horse', on_delete=models.CASCADE)
    jockey = models.ForeignKey('netkeiba.Jockey', on_delete=models.CASCADE)
    trainer = models.ForeignKey('netkeiba.Trainer', on_delete=models.CASCADE)
    owner = models.ForeignKey('netkeiba.Owner', on_delete=models.CASCADE)
    order_of_finish = models.PositiveSmallIntegerField(null=True)
    position_state = models.CharField(max_length=255, choices=POSITION_STATE_CHOICES)
    post_position = models.PositiveSmallIntegerField()
    horse_number = models.PositiveIntegerField()
    weight_carried = models.FloatField()
    finish_time = models.FloatField(null=True)
    margin = models.CharField(max_length=255, choices=MARGIN_CHOICES, null=True)
    corner_pass_order = models.CharField(max_length=255, validators=[validate_comma_separated_integer_list], null=True)
    final_stage_time = models.FloatField(null=True)
    first_place_odds = models.FloatField(null=True)
    popularity = models.PositiveSmallIntegerField(null=True)
    horse_weight = models.FloatField(null=True)
    horse_weight_diff = models.FloatField(null=True)
    purse = models.FloatField(default=0.)

    class Meta:
        db_table = 'race_contenders'
        unique_together = ('race', 'horse', 'jockey', 'trainer', 'owner')
