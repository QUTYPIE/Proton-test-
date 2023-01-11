from abc import ABCMeta, abstractproperty
from constants import TerrainTypes
from camel_weapon import CamelWeapon, AffectCamels, EffectType, WeaponTakesEffect


class Camel(object):
    __metaclass__ = ABCMeta

    def __init__(self, name, player, max_position):
        self._position = 0
        self.max_position = max_position
        self.name = name
        self.player = player
        self.received_attacks = []
        self.forward_camels = []  # camels names immediately forward
        self.chaser_camels = []  # camels names immediately chasing
        self.weapon = None  # will be created by equip_weapon()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        """ ensure camel stays within race lanes limits"""
        if value > self.max_position:
            self._position = self.max_position
        elif value < 0:
            self._position = 0
        else:
            self._position = value

    @abstractproperty
    def icon(self):
        """ 3 rows * 9 columns """
        # we could check icons provided by son classes are 3x9
        # at __init__ of Camel object
        pass

    @abstractproperty
    def strength(self): pass

    @abstractproperty
    def default_boost(self):pass

    @abstractproperty
    def terrain_boost(self):pass

    @abstractproperty
    def favorite_terrain(self):pass

    def get_turbo_boost(self, terrain):
        if terrain == self.favorite_terrain:
            return self.terrain_boost
        else:
            return self.default_boost

    @abstractproperty
    def weapon_name(self):pass

    @abstractproperty
    def weapon_impact(self):pass

    @abstractproperty
    def weapon_affects(self):pass

    @abstractproperty
    def weapon_takes_affect(self):pass

    @abstractproperty
    def weapon_effect_type(self):pass

    def reset(self):
        self.position = 0
        self.chaser_camels = []
        self.forward_camels = []
        self.received_attacks = []

    def equip_weapon(self, impact=None):
        """ camels almost have all the info to create their weapons
        but we may need external data such as X from game object
        only overwrite value is self.wepon_impact is None"""
        if impact and not self.weapon_impact:
            self.weapon_impact = impact

        self.weapon = CamelWeapon(self.weapon_name,
                                  self.weapon_impact,
                                  affects=self.weapon_affects,
                                  takes_effect=self.weapon_takes_affect,
                                  effect_type=self.weapon_effect_type)

    def use_weapon(self, camels):
        if self.weapon.affects == AffectCamels.BOTH:
            for camel_name, camel in camels.items():
                if camel_name in self.chaser_camels + self.forward_camels:
                    camel.received_attacks.append(self.weapon)
        elif self.weapon.affects == AffectCamels.FORWARD:
            for camel_name, camel in camels.items():
                if camel_name in self.forward_camels:
                    camel.received_attacks.append(self.weapon)
        elif self.weapon.affects == AffectCamels.CHASER:
            for camel_name, camel in camels.items():
                if camel_name in self.chaser_camels:
                    camel.received_attacks.append(self.weapon)

    def absorb_attacks(self):
        """ returns accumulated effect of attacks from weapon
        with immediate effect, and delete theses attacks.
        also, change attacks with effect on next round
        to WeaponTakesEffect.now so they will be absorbed on the next round

        returns dict with accumulated effect per type
        """
        effect ={"absolute": 0 ,
                 "percent":0}

        for weapon in self.received_attacks:
            if weapon.takes_effect == WeaponTakesEffect.NOW:
                if weapon.effect_type == EffectType.FIXED:
                    effect["absolute"]+= weapon.impact
                else:
                    effect["percent"] += weapon.impact
                self.received_attacks.remove(weapon)

            else:
                weapon.takes_effect = WeaponTakesEffect.NOW

        return effect

    def __eq__(self, other):
        return (self.name == other.name and
                self.player == other.player and
                self.weapon == other.weapon)

    def __str__(self):
        weapon_name = "not equiped"
        if self.weapon:
            weapon_name = self.weapon.name
        return ("Camel: [name:{}, player:{}, position:{},\n "
                "   immediate forward{} chasers{}\n "
                "   recieved attacks{}"
                "   weapon {}]".format(
            self.name, self.player, self.position,
            self.forward_camels, self.chaser_camels,
            [a.name for a in self.received_attacks],
            weapon_name))


class BactrianCamel(Camel):
    strength = 20
    default_boost = 15
    terrain_boost = 30
    favorite_terrain = TerrainTypes.Mud
    weapon_name = "kick"
    weapon_impact = None # X should be set externally
    weapon_affects = AffectCamels.CHASER
    weapon_takes_affect = WeaponTakesEffect.NOW
    weapon_effect_type = EffectType.FIXED

    icon =(" /^^\ oo=",
           "+------' ",
           " |###|   ")

    def __init__(self,name, player, max_position):
        super(BactrianCamel, self).__init__(name, player,max_position)


class DomesticCamel(Camel):
    strength = 10
    default_boost = 20
    terrain_boost = 30
    favorite_terrain = TerrainTypes.Grass
    weapon_name = "sound"
    weapon_impact = 50
    weapon_affects = AffectCamels.BOTH
    weapon_takes_affect = WeaponTakesEffect.NEXT_ROUND
    weapon_effect_type = EffectType.PERCENT
    icon = (" /^^\ oo=",
            "-------' ",
            " ]---[   ")

    def __init__(self,name, player, max_position):
        super(DomesticCamel, self).__init__(name, player, max_position)


class DromedaryCamel(Camel):
    strength = 0
    default_boost = 25
    terrain_boost = 35
    favorite_terrain = TerrainTypes.Sand
    weapon_name = "spit"
    weapon_impact = 100  # That camel will not move forward during the next round
    weapon_affects = AffectCamels.FORWARD
    weapon_takes_affect = WeaponTakesEffect.NEXT_ROUND
    weapon_effect_type = EffectType.PERCENT
    icon = ( "  /^\ oo=",
             ".------' ",
             " |   |   ")

    def __init__(self,name, player, max_position):
        super(DromedaryCamel, self).__init__(name, player, max_position)


class CamelTypes(object):
    """ Enum like with class mapping for camel types"""
    Bactrian, Domestic, Dromedary = ["Bactrian", "Domestic", "Dromedary"]
    class_map = {Bactrian: BactrianCamel, Domestic: DomesticCamel, Dromedary: DromedaryCamel}
