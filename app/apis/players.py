from flask_restx import Namespace, Resource, fields
from flask import request
from http import HTTPStatus
from app.db.utils import serialize_items
from app.db import player
from app.apis import MSG
from app.db.constants import PATH
import os
import pandas as pd
from app.apis import positions
from app.apis.parser import FM24Parser

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
role_model=players_ns.model(
    "Role",
    {
        'role': fields.String(
        required=True,
        enum=['Goalkeeper','SweeperKeeper','BallPlayingDef','CenterBack',
              'WingBack','DeepLyingPlaymaker', 'BallWinningMid','BoxToBox',
              'AdvancedPlaymaker','ShadowStriker'],
        description='Player Roles'
    )
}) 
    


@players_ns.route("/import")
class ImportPlayers(Resource):
    @players_ns.expect(path_model)
    def post(self):
        data = request.json
        path = data.get(PATH)
        if not os.path.exists(path):
            return {'error': 'File not found'}, HTTPStatus.NOT_FOUND

        parser = FM24Parser(path, os.path.basename(path), delimiter="|")
        df = parser.parse()

        # Convert DataFrame columns to lowercase for consistency
        df.columns = df.columns.str.lower()

        # Convert numeric columns to int
        numeric_cols = df.select_dtypes(include=['object']).columns
        for col in numeric_cols:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(df[col])
            except:
                pass

        players_added = []
        for _, row in df.iterrows():
            # Convert row to dict, excluding NaN values
            player_dict = row.dropna().to_dict()
            # Only add if we have at least a name
            if 'name' in player_dict and player_dict['name']:
                player_id = player.add_player(**player_dict)
                players_added.append(player_id)

        return {MSG: f"{len(players_added)} players successfully added"}, HTTPStatus.OK
        


@players_ns.route("/list")
class PrintPlayers(Resource):
    def get(self):
        players = player._get_player_collection().find({})
        player_list = serialize_items(players)
        
        return player_list, HTTPStatus.OK
    
@players_ns.route("/<string:name>")
class FindPlayers(Resource):
    def get(self,name):
        player_doc = player.get_player(name)
        
        return player_doc, HTTPStatus.OK

@players_ns.route("/analyse/<string:name>")
class PlayerAnalysis(Resource):
    @players_ns.expect(role_model)
    def post(self, name):
        player_doc=player.get_player(name)
        data=request.json
        role=data.get('role')
        position=positions.create_position(role)
        rating= position.rating(player_doc)
        return {
            "player":player_doc['name'],
            "role":role,
            "rating": rating
        }
        
@players_ns.route("/analyse/role")
class RoleAnalysis(Resource):
    @players_ns.expect(role_model)
    def post(self):
        data = request.json
        role = data.get('role')
        ratings = {}
        for player_doc in player._get_player_collection().find({}):
            position = positions.create_position(role)
            rating = position.rating(player_doc)
            ratings[player_doc['name']] = rating

        sorted_ratings = dict(sorted(ratings.items(), key=lambda item: item[1], reverse=True))
        return sorted_ratings



            



        


        
        