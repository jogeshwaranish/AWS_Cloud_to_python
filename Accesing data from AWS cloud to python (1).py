#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import json
from urllib.request import urlopen
import boto3

# Function to fetch and process data from chess.com API
def fetch_chess_data():
    url = 'https://api.chess.com/pub/player/gmhikaruontwitch/games/2020/07'
    try:
        with urlopen(url) as json_url:
            data = json.loads(json_url.read())
            return data.get('games', [])
    except Exception as e:
        print(f"Error fetching chess data: {e}")
        return []

# Function to process chess data and store it in DynamoDB
def process_and_store_data(data):
    dynamo_list = []
    legal_moves = ['1. e4', '1. d4', '1. c4', '1. Nf3', '1. Nc3', '1. e3', '1. d3', '1. a3', '1. b3', '1. g3']

    for game in data:
        pgn = game.get('pgn', '')
        
        first_move = None
        for move in legal_moves:
            if move in pgn:
                first_move = move[3:]
                break
        
        result = "lost"
        for win_statement in ['checkmate', 'resignation', 'time']:
            if win_statement in pgn:
                result = "won"
                break
        
        side = "White" if "White \"GMHikaruOnTwitch\"" in pgn else "Black"
        
        dynamo_list.append({
            "First_Move": first_move,
            "Players": side,
            "Result": result
        })

    return dynamo_list

# Function to store data in DynamoDB
def store_data_in_dynamodb(data):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('chessgames')
        
        for i, item in enumerate(data):
            table.put_item(Item={
                "GameNum": i + 1,
                "First_Move": item["First_Move"],
                "Players": item["Players"],
                "Result": item["Result"]
            })
        
        print("Data successfully stored in DynamoDB.")
    except Exception as e:
        print(f"Error storing data in DynamoDB: {e}")

if __name__ == "__main__":
    chess_data = fetch_chess_data()
    if chess_data:
        processed_data = process_and_store_data(chess_data)
        if processed_data:
            store_data_in_dynamodb(processed_data)
    else:
        print("No chess data found.")
