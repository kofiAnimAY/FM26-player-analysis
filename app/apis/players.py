from flask_restx import Namespace, Resource, fields
from flask import request
from http import HTTPStatus
from app.db.utils import serialize_items
from app.db import player
from app.apis import MSG
from app.db.constants import PATH
import os
players_ns = Namespace(
    "players",
    description="Player API"
)

player_model = players_ns.model('Player', {
    'id': fields.String(description='Player ID'),
    'NAME': fields.String(description="Name"),
    'crossing': fields.Integer(description='Crossing'),
    'dribbling': fields.Integer(description='Dribbling'),
    'finishing': fields.Integer(description='Finishing'),
    'first_touch': fields.Integer(description='First Touch'),
    'free_kick_taking': fields.Integer(description='Free Kick Taking'),
    'heading': fields.Integer(description='Heading'),
    'long_shots': fields.Integer(description='Long Shots'),
    'long_throws': fields.Integer(description='Long Throws'),
    'marking': fields.Integer(description='Marking'),
    'passing': fields.Integer(description='Passing'),
    'penalty_taking': fields.Integer(description='Penalty Taking'),
    'tackling': fields.Integer(description='Tackling'),
    'technique': fields.Integer(description='Technique'),
    'corners': fields.Integer(description='Corners'),
    'aggression': fields.Integer(description='Aggression'),
    'anticipation': fields.Integer(description='Anticipation'),
    'bravery': fields.Integer(description='Bravery'),
    'composure': fields.Integer(description='Composure'),
    'concentration': fields.Integer(description='Concentration'),
    'decisions': fields.Integer(description='Decisions'),
    'determination': fields.Integer(description='Determination'),
    'flair': fields.Integer(description='Flair'),
    'leadership': fields.Integer(description='Leadership'),
    'off_the_ball': fields.Integer(description='Off The Ball'),
    'positioning': fields.Integer(description='Positioning'),
    'teamwork': fields.Integer(description='Teamwork'),
    'vision': fields.Integer(description='Vision'),
    'work_rate': fields.Integer(description='Work Rate'),
    'adaptability': fields.Integer(description='Adaptability'),
    'ambition': fields.Integer(description='Ambition'),
    'acceleration': fields.Integer(description='Acceleration'),
    'agility': fields.Integer(description='Agility'),
    'balance': fields.Integer(description='Balance'),
    'jumping_reach': fields.Integer(description='Jumping Reach'),
    'natural_fitness': fields.Integer(description='Natural Fitness'),
    'pace': fields.Integer(description='Pace'),
    'stamina': fields.Integer(description='Stamina'),
    'strength': fields.Integer(description='Strength'),
    'aerial_reach': fields.Integer(description='Aerial Reach'),
    'command_of_area': fields.Integer(description='Command of Area'),
    'communication': fields.Integer(description='Communication'),
    'eccentricity': fields.Integer(description='Eccentricity'),
    'handling': fields.Integer(description='Handling'),
    'kicking': fields.Integer(description='Kicking'),
    'one_on_ones': fields.Integer(description='One on Ones'),
    'punching_tendency': fields.Integer(description='Punching Tendency'),
    'reflexes': fields.Integer(description='Reflexes'),
    'rushing_out_tendency': fields.Integer(description='Rushing Out Tendency'),
    'throwing': fields.Integer(description='Throwing'),
})
path_model= players_ns.model(
    "Path",
    {
        PATH: fields.String(example="players.rtf")
    }
)


@players_ns.route("/import")
class ImportPlayers(Resource):
    @players_ns.expect(path_model)
    def post(self):
        data=request.json
        path=data.get(PATH)
        if not os.path.exists(path):
            return {'error': 'File not found'}, HTTPStatus.NOT_FOUND
        attributes=[
            "name", 
        ]
        with open(path,"r",encoding='utf-8')as file:
            players=[]

            for line in file:
                line=line.strip()
                if not line:
                    continue
                info=[]
                info=[part.strip() for part in line.split("|")]
                for i in range(1,len(info)):
                    try:
                        info[i]=int(info[i])
                    except ValueError:
                       info[i]=0
                        
                if len(info)<len(attributes):
                    continue
                player_dict=dict(zip(attributes,info))
                player_id= player.add_player(player_dict)
                players.append(player_id)
            return {MSG: f"{len(players)} players added"}, HTTPStatus.OK

        





        
        