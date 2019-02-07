from django.core.validators import validate_comma_separated_integer_list
from django.db import models

from server.models.base import BaseModel


class BettingTicket(BaseModel):
    WIN = 'WIN'  # 単勝
    SHOW = 'SHOW'  # 複勝
    QUINELLA = 'QUINELLA'  # 馬連
    BRACKET_QUINELLA = 'BRACKET_QUINELLA'  # 枠連
    DUET = 'DUET'  # ワイド
    EXACTA = 'EXACTA'  # 馬単
    TRIO = 'TRIO '  # 三連複
    TRIFECTA = 'TRIFECTA'  # 三連単
    BET_TYPES = (
        (WIN, 'Win'),
        (SHOW, 'Show'),
        (QUINELLA, 'Quinella'),
        (BRACKET_QUINELLA, 'Bracket Quinella'),
        (DUET, 'Duet'),
        (EXACTA, 'Exacta'),
        (TRIO, 'Trio'),
        (TRIFECTA, 'Trifecta'),
    )

    race = models.ForeignKey('server.Race', on_delete=models.CASCADE)
    bet_type = models.CharField(max_length=255, choices=BET_TYPES)
    horse_numbers = models.CharField(max_length=255, validators=[validate_comma_separated_integer_list])
    payoff = models.PositiveIntegerField()

    class Meta:
        db_table = 'betting_tickets'
        unique_together = ('race', 'bet_type', 'horse_number')
