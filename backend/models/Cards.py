from enum import Enum, unique

@unique
class Card(Enum):
    herz_zwei   = (0, 'hearts/2.png')
    herz_drei   = (1, 'hearts/3.png')
    herz_vier   = (2, 'hearts/4.png')
    herz_fünf   = (3, 'hearts/5.png')
    herz_sechs  = (4, 'hearts/6.png')
    herz_sieben = (5, 'hearts/7.png')
    herz_acht   = (6, 'hearts/8.png')
    herz_neun   = (7, 'hearts/9.png')
    herz_zehn   = (8, 'hearts/10.png')
    herz_bube   = (9, 'hearts/Jack.png')
    herz_dame   = (10, 'hearts/Queen.png')
    herz_könig  = (11, 'hearts/King.png')
    herz_ass    = (12, 'hearts/Ace.png')
    pik_zwei    = (13, 'spades/2.png')
    pik_drei    = (14, 'spades/3.png')
    pik_vier    = (15, 'spades/4.png')
    pik_fünf    = (16, 'spades/5.png')
    pik_sechs   = (17, 'spades/6.png')
    pik_sieben  = (18, 'spades/7.png')
    pik_acht    = (19, 'spades/8.png')
    pik_neun    = (20, 'spades/9.png')
    pik_zehn    = (21, 'spades/10.png')
    pik_bube    = (22, 'spades/Jack.png')
    pik_dame    = (23, 'spades/Queen.png')
    pik_könig   = (24, 'spades/King.png')
    pik_ass     = (25, 'spades/Ace.png')
    karo_zwei   = (26, 'diamonds/2.png')
    karo_drei   = (27, 'diamonds/3.png')
    karo_vier   = (28, 'diamonds/4.png')
    karo_fünf   = (29, 'diamonds/5.png')
    karo_sechs  = (30, 'diamonds/6.png')
    karo_sieben = (31, 'diamonds/7.png')
    karo_acht   = (32, 'diamonds/8.png')
    karo_neun   = (33, 'diamonds/9.png')
    karo_zehn   = (34, 'diamonds/10.png')
    karo_bube   = (35, 'diamonds/Jack.png')
    karo_dame   = (36, 'diamonds/Queen.png')
    karo_könig  = (37, 'diamonds/King.png')
    karo_ass    = (38, 'diamonds/Ace.png')
    treff_zwei  = (39, 'clubs/2.png')
    treff_drei  = (40, 'clubs/3.png')
    treff_vier  = (41, 'clubs/4.png')
    treff_fünf  = (42, 'clubs/5.png')
    treff_sechs = (43, 'clubs/6.png')
    treff_sieben= (44, 'clubs/7.png')
    treff_acht  = (45, 'clubs/8.png')
    treff_neun  = (46, 'clubs/9.png')
    treff_zehn  = (47, 'clubs/10.png')
    treff_bube  = (48, 'clubs/Jack.png')
    treff_dame  = (49, 'clubs/Queen.png')
    treff_könig = (50, 'clubs/King.png')
    treff_ass   = (51, 'clubs/Ace.png')
    
    def __new__(cls, value, photo_link):
        obj = object.__new__(cls)
        obj._value_ = value  # 🔹 Ensures `Card(13)` works
        obj.photo_link = photo_link
        return obj