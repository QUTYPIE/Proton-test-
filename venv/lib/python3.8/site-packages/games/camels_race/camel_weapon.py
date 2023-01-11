from enum import Enum

WeaponTakesEffect = Enum("WeaponTakesEffect", "NOW NEXT_ROUND")

AffectCamels = Enum("AffectCamels", "CHASER FORWARD BOTH")

EffectType = Enum("EffectType", "FIXED PERCENT")


class CamelWeapon(object):
    def __init__(self, name, impact,
                 affects=AffectCamels.BOTH,
                 takes_effect=WeaponTakesEffect.NOW,
                 effect_type=EffectType.PERCENT):
        self.name = name
        self.impact = impact
        self.affects = affects
        self.takes_effect = takes_effect
        self.effect_type = effect_type

    def __str__(self):
        return "Weapon:[name:{}, {}, {}, impact:{} {}]".format(
            self.name,
            self.affects,
            self.takes_effect,
            self.impact,
            self.effect_type)

    def __eq__(self, other):
        return self.name == other.name