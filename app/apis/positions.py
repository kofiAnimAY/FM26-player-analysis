from abc import ABC

attributes=[
            'name',
            'crossing',
            'dribbling',
            'finishing',
            'first_touch',
            'free_kick_taking',
            'heading',
            'long_shots',
            'long_throws',
            'marking',
            'passing',
            'penalty_taking',
            'tackling',
            'technique',
            'corners',
            'aggression',
            'anticipation',
            'bravery',
            'composure',
            'concentration',
            'decisions',
            'determination',
            'flair',
            'leadership',
            'off_the_ball',
            'positioning',
            'teamwork',
            'vision',
            'work_rate',           
            'acceleration',
            'agility',
            'balance',
            'jumping_reach',
            'natural_fitness',
            'pace',
            'stamina',
            'strength',
            'aerial_reach',
            'command_of_area',
            'communication',
            'eccentricity',
            'handling',
            'kicking',
            'one_on_ones',
            'punching_tendency',
            'reflexes',
            'rushing_out_tendency',
            'throwing', 
        ]
class BasePosition(ABC):
    def __init__(self,name,category,weights):
        self.name=name
        self.category=category
        self.weights=weights
        
    
    def rating(self,player_doc):
        score=0
        divisor=0
        for key,value in self.weights.items():
            score += value*player_doc.get(key,0)
            divisor+=abs(value)
        return score/divisor
        
    

class GoalKeeper(BasePosition):
    def __init__(self):
        super().__init__("GoalKeeper","GK",{
            "throwing": 0.2,
            "reflexes": 0.5,
            "one_on_ones": 0.5,
            "kicking": 0.3,
            "handling": 0.4,
            "eccentricity": -0.1,
            "communication": 0.35,
            "command_of_area":0.45,
            "aerial_reach": 0.4,
            "strength": 0.1,
            "agility": 0.25,
            "decisions": 0.1,
            "concentration": 0.25,
            "positioning": 0.3,
            "anticipation": 0.2
        })

class SweeperKeeper(BasePosition):
    def __init__(self):
        super().__init__("Sweeper Keeper","GK",{
            "throwing": 0.2,
            "reflexes": 0.5,
            "one_on_ones": 0.5,
            "kicking": 0.3,
            "handling": 0.35,
            "eccentricity": 0.1,
            "communication": 0.3,
            "command_of_area":0.45,
            "aerial_reach": 0.35,
            "strength": 0.1,
            "agility": 0.25,
            "decisions": 0.1,
            "concentration": 0.25,
            "positioning": 0.3,
            "anticipation": 0.3,
            "passing": 0.15,
            "rushing_out_tendency":0.25,
            "vision": 0.2,
            "composure":0.25,
            "acceleration": 0.1,
            "first_touch": 0.1

        })

class BallPlayingDef(BasePosition):
    def __init__(self):
        super().__init__("Ball Playing Defender","DEF",{
            "first_touch": 0.2,
            "heading": 0.45,
            "marking": 0.6,
            "passing": 0.45,
            "tackling": 0.6,
            "technique": 0.2,
            "aggression": 0.15,
            "anticipation": 0.2,
            "bravery":0.2,
            "composure": 0.25,
            "concentration":0.15,
            "decisions": 0.2,
            "positioning": 0.4,
            "vision": 0.25,
            "jumping_reach": 0.4,
            "pace": 0.3,
            "strength": 0.5


        })

class CenterBack(BasePosition):
    def __init__(self):
        super().__init__("Central Defender","DEF",{
            
            "heading": 0.6,
            "marking": 0.6,
            "tackling": 0.6,
            "technique": 0.2,
            "aggression": 0.2,
            "anticipation": 0.2,
            "bravery":0.2,
            "composure": 0.2,
            "concentration":0.15,
            "decisions": 0.2,
            "positioning": 0.4,
            "jumping_reach": 0.5,
            "pace": 0.3,
            "strength": 0.6


        })

class WingBack(BasePosition):
    def __init__(self):
        super().__init__("Wing Back","DEF",{
            "crossing": 0.4,
            "dribbling": 0.3,
            "first_touch": 0.2,
            "marking": 0.3,
            "passing": 0.25,
            "tackling": 0.35,
            "technique": 0.2,
            "balance": 0.2,
            "anticipation": 0.2,
            "agility": 0.15,
            "off_the_ball": 0.3,
            "concentration":0.15,
            "decisions": 0.2,
            "positioning": 0.25,
            "teamwork": 0.25,
            "work_rate": 0.4,
            "acceleration": 0.35,
            "pace": 0.3,
            "strength": 0.5,
            "stamina":0.4


        })


class DeepLyingPlaymaker(BasePosition):
    def __init__(self):
        super().__init__("Deep Lying Playmaker","MID",{
            
            "first_touch": 0.4,        
            "passing": 0.7,
            "technique": 0.3,
            "anticipation": 0.1,
            "composure": 0.25,
            "decisions": 0.25,
            "off_the_ball": 0.2,
            "positioning": 0.2,
            "teamwork":0.2,
            "vision": 0.55,
            "balance":0.15,



        })

class BallWinningMid(BasePosition):
    def __init__(self):
        super().__init__("Ball Winning Midfielder","MID",{
            
            "marking": 0.45,
            "tackling": 0.7,
            "aggression": 0.5,
            "anticipation": 0.25,
            "bravery":0.2,
            "concentration": 0.2,
            "positioning": 0.25,
            "teamwork":0.3,
            "work_rate": 0.55,
            "agility":0.15,
            "pace":0.15,
            "stamina":0.3,
            "strength":0.35,



        })

class BoxToBox(BasePosition):
    def __init__(self):
        super().__init__("Box to Box Midfielder","MID",{
            "dribbling":0.15,
            "finishing":0.1,
            "first_touch": 0.2,
            "long_shots":0.2,
            "passing": 0.3,
            "tackling": 0.3,
            "technique":0.15,
            "aggression": 0.1,
            "anticipation": 0.15,
            "composure":0.2,
            "decisions":0.15,
            "off_the_ball":0.3,
            "positioning": 0.2,
            "teamwork":0.3,
            "work_rate": 0.6,
            "acceleration":0.15,
            "balance":0.15,
            "pace":0.15,
            "stamina":0.5,
            "strength":0.2



        })

class AdvancedPlaymaker(BasePosition):
    def __init__(self):
        super().__init__("Advanced Playmaker","MID",{
            "dribbling": 0.4,
            "first_touch": 0.4,
            "passing": 0.65,
            "flair":0.2,
            "technique": 0.3,
            "anticipation": 0.1,
            "composure": 0.25,
            "decisions": 0.35,
            "off_the_ball": 0.35,
            "teamwork":0.3,
            "vision": 0.7,
            "agility":0.15



        })

class ShadowStriker(BasePosition):
    def __init__(self):
        super().__init__("Shadow Striker","MID",{
            "dribbling": 0.35,
            "finishing": 0.5,
            "first_touch": 0.35,
            "passing": 0.2,
            "technique": 0.2,
            "anticipation": 0.25,
            "composure": 0.25,
            "concentration":0.1,
            "decisions": 0.15,
            "off_the_ball": 0.6,
            "work_rate":0.2,
            "acceleration":0.4,
            "agility":0.15,
            "balance":0.15,
            "pace":0.15,
            "stamina":0.15



        })

class Winger(BasePosition):
    def __init__(self):
        super().__init__("Winger","ATT",{
            "crossing": 0.7,
            "dribbling": 0.55,
            "first_touch": 0.2,         
            "passing": 0.2,
            "technique": 0.25,
            "balance": 0.15,
            "agility": 0.25,
            "off_the_ball": 0.2,
            "work_rate": 0.2,
            "acceleration": 0.6,
            "pace": 0.5,
            "stamina":0.2,



        })

class InvertedWinger(BasePosition):
    def __init__(self):
        super().__init__("Inverted Winger","ATT",{
            "crossing": 0.35,
            "dribbling": 0.6,
            "first_touch": 0.2,  
            "long_shots": 0.15,
            "composure": 0.15,
            "decisions": 0.15,
            "vision": 0.3,   
            "passing": 0.3,
            "technique": 0.3,
            "balance": 0.15,
            "agility": 0.25,
            "off_the_ball": 0.35,
            "work_rate": 0.15,
            "acceleration": 0.55,
            "pace": 0.45,
            "stamina":0.15,



        })

class InsideForward(BasePosition):
    def __init__(self):
        super().__init__("Inside Forward","ATT",{
            
            "dribbling": 0.4,
            "finishing": 0.55,
            "anticipation": 0.25,
            "first_touch": 0.3,  
            "long_shots": 0.15,
            "composure": 0.15,
            "flair":0.15, 
            "passing": 0.15,
            "technique": 0.3,
            "balance": 0.15,
            "agility": 0.25,
            "off_the_ball": 0.5,
            "work_rate": 0.15,
            "acceleration": 0.55,
            "pace": 0.45,
            "stamina":0.15,



        })

class AdvancedForward(BasePosition):
    def __init__(self):
        super().__init__("Advanced Forward","ATT",{
            "dribbling": 0.3,
            "finishing": 0.7,
            "first_touch": 0.3, 
            "passing": 0.15,
            "technique": 0.25,
            "anticipation": 0.2,
            "decisions": 0.2,
            "work_rate": 0.2,
            "long_shots": 0.2,
            "composure": 0.25,
            "off_the_ball": 0.5,
            "acceleration": 0.6,
            "agility": 0.15,
            "balance": 0.15,
            "pace": 0.4,
            "stamina":0.15,



        })

class DeepLyingForward(BasePosition):
    def __init__(self):
        super().__init__("Deep Lying Forward","ATT",{
            "finishing": 0.55,
            "first_touch": 0.3, 
            "passing": 0.4,
            "technique": 0.25,
            "anticipation": 0.2,
            "flair":0.15,
            "decisions": 0.3,
            "teamwork":0.25,
            "vision": 0.5,
            "strength": 0.2,
            "composure": 0.25,
            "off_the_ball": 0.4,
            "balance": 0.15



        })

class TargetForward(BasePosition):
    def __init__(self):
        super().__init__("Target Forward","ATT",{
            "finishing": 0.5,
            "first_touch": 0.2, 
            "heading": 0.55,
            "anticipation": 0.2,
            "aggression": 0.2,
            "bravery":0.25,
            "decisions": 0.2,
            "composure": 0.25,
            "off_the_ball": 0.35,
            "teamwork":0.2,
            "jumping_reach": 0.55,
            "strength": 0.4,
            "agility": 0.15,
            "balance": 0.2,
            



        })
POSITION_CLASSES = {
    "GoalKeeper": GoalKeeper,
    "SweeperKeeper": SweeperKeeper,
    "BallPlayingDef": BallPlayingDef,
    "CenterBack": CenterBack,
    "WingBack": WingBack,
    "DeepLyingPlaymaker": DeepLyingPlaymaker,
    "BallWinningMidfielder": BallWinningMid,
    "BoxToBox": BoxToBox,
    "AdvancedPlaymaker": AdvancedPlaymaker,
    "ShadowStriker": ShadowStriker,
    "Winger": Winger,
    "InvertedWinger": InvertedWinger,
    "InsideForward": InsideForward,
    "AdvancedForward": AdvancedForward,
    "DeepLyingForward": DeepLyingForward,
    "TargetForward": TargetForward
}

def get_position_class(role_name: str):
    if role_name in POSITION_CLASSES:
        return POSITION_CLASSES[role_name]
    else:
        raise ValueError(f"Unknown role: {role_name}")
    
def create_position(role_name: str):
    position_class = get_position_class(role_name)
    return position_class()