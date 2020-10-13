#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 15:23:27 2020
@author: BFitzpatrick
"""

import os
import json
import numpy as np
import pandas as pd
import requests
from datetime import date
from bs4 import BeautifulSoup
from metis_app.ml_models.aws_util import aws_download

class NhlGameResultsScraper(object):

    url = 'https://www.hockey-reference.com/leagues/NHL_2020_games.html'
    SEASON_END = date(2020, 4, 4)
    BASEDIR = os.path.join('metis_app', 'api', 'static', 'api', 'data')
    TEAM_DATA_FILENAME = os.path.join(
        BASEDIR,
        'nhl_team_data.csv'
    )

    def __init__(self):
        if not os.path.isdir(NhlGameResultsScraper.BASEDIR):
            os.makedirs(NhlGameResultsScraper.BASEDIR)

        self.team_data = self.load_team_data()
        self.data = self.load_data()
    
    def load_data(self):
        cls = NhlGameResultsScraper

        """ if data is greater than season end return AWS file """
        if date.today() > cls.SEASON_END:
            filename = f"nhl_results_{cls.SEASON_END}.json"
            if not os.path.isfile(filename):
                aws_download(filename, local_directory=cls.BASEDIR)

            filename = os.path.join(cls.BASEDIR, filename)
            with open(filename, 'r') as f:
                data = json.load(f)
        else:
            today = date.today().strftime('%Y%m%d')
            filename = os.path.join(cls.BASEDIR, f"nhl_results_{today}.json")

            """ if the data has already been saved in a file, load the file """
            if os.path.isfile(filename):
                with open(filename, 'r') as f:
                    print(filename)
                    data = json.load(f)
            else:
                """ if not either of the first two scrape the NHL API """
                data = self.scrape_nhl_website()

                with open(filename, 'w') as f:
                    json.dump(data, f)
        
        return data

    def scrape_nhl_website(self):
        response = requests.get(NhlGameResultsScraper.url)
    
        soup = BeautifulSoup(response.text, 'html.parser')
    
        table = str(soup.find('table', {'id': 'games'}))
        df = pd.read_html(table)[0]
    
        colmap = {
            'Date': 'date',
            'Visitor': 'away_team',
            'G': 'away_goals',
            'Home': 'home_team',
            'G.1': 'home_goals',
            'Unnamed: 5': 'extra_time',
            'Att.': 'attendance',
            'LOG': 'game_length',
            'Notes': 'notes',
        }
        df = (df.rename(columns=colmap)
            .assign(date=lambda x: pd.to_datetime(x.date))
            .query("date <= '2020-03-11'")
            .pipe(self.filter_unplayed_games)
            .set_index('date', append=True)
            .rename_axis(["game_id", "date"])
            .assign(home_win=lambda x: (x.home_goals > x.away_goals),
                    away_win=lambda x: (x.home_goals < x.away_goals))
        )
    
        df_teams = self.create_df_teams(df)
    
        df_full = self.create_df_full(df_teams)
        
        df_wildcard = self.create_df_wildcard(df_full)
        
        df_full = (df_full.join(df_wildcard)
            .assign(wildcard=lambda x: x.wildcard.fillna('No'))
            .pipe(self.add_wild_contender)
        )
    
        records = self.df_full_to_records(df_full)
        
        return records
    
    @staticmethod
    def points_calc(win, extra_time):
        extra_time_loss = ~win & ~extra_time.isnull()
        loss_points = np.where(extra_time_loss, 1, 0)
        points = np.where(win, 2, loss_points)
        return points
    
    @staticmethod
    def filter_unplayed_games(input_df):
        df = input_df.copy()
        today = date.today().isoformat()
        mask = df.date < today
        return df.loc[mask, ]
    
    def create_df_teams(self, df):
        home_cols = ['home_team', 'home_win', 'extra_time']
        away_cols = ['away_team', 'away_win', 'extra_time']
    
        frames = list()
        for cols in [home_cols, away_cols]:
            df_team = (df.loc[:, cols]
                .rename(columns={
                    'home_team': 'team',
                    'away_team': 'team',
                    'home_win': 'win',
                    'away_win': 'win',
                })
                .set_index('team', append=True)
            )
            frames.append(df_team)
    
        df_teams = (pd.concat(frames)
            .assign(points=lambda x: self.points_calc(x.win, x.extra_time))
            .sort_values(by=['team', 'date'])
            .assign(team_game_id=lambda x: x.groupby('team').cumcount() + 1,
                    total_points=lambda x: x.groupby('team')['points'].cumsum())
        )
        return df_teams
    
    @staticmethod
    def create_index_from_interpolation(df_teams):
        season_start = df_teams.index.get_level_values(1).min()
        season_end = df_teams.index.get_level_values(1).max()
        dates = pd.date_range(season_start, season_end, freq='D').to_list()
        teams = df_teams.index.get_level_values(2).unique().to_list()
        iterables = [dates, teams]
        index = pd.MultiIndex.from_product(iterables, names=['date', 'team'])
        return index
    
    def create_df_full(self, df_teams):
        index = self.create_index_from_interpolation(df_teams)
        df_teams_temp = (df_teams
            .reset_index(level=0)
            .rename(columns={'team_game_id': 'games_played'})
            .loc[:, ['games_played', 'total_points']]
            .rename(columns={'total_points': 'points'})
        )
        df_merged = (pd.DataFrame(index=index)
            .merge(df_teams_temp, how='left', left_index=True, right_index=True)
        )
        df_merged[['games_played', 'points']] = df_merged.groupby(['team']).ffill().fillna(0)
        return df_merged
    
    @staticmethod
    def df_full_to_records(df_full):
        records = list()
        for date in df_full.index.get_level_values(level=0).unique().to_list():
            record = {
                'date': date.strftime('%Y-%m-%d'),
                'teams': df_full.xs(date).reset_index().to_dict(orient='records')
            }
            records.append(record)
        return records
    
    @staticmethod
    def create_df_wildcard(df_full):
        df = df_full.copy()
        df = df.join(self.team_data, how='left', on='team')
        by, ascending = ['date', 'division', 'points'], [True, True, False]
        df = df.sort_values(by=by, ascending=ascending)
        
        by, ascending = ['date', 'division', 'points'], [True, True, False]
        df['division_rank'] = (df.sort_values(by=by, ascending=ascending)
            .groupby(['date', 'division'])
            .points.rank(method='first', ascending=False)
        )
        
        mask = df.division_rank > 3
        df_wildcard = df.loc[mask, ].copy()
        by, ascending = ['date', 'conference', 'points'], [True, True, False]
        df_wildcard = df_wildcard.sort_values(by=by, ascending=ascending)

        by, ascending = ['date', 'conference', 'points'], [True, True, False]
        df_wildcard['conference_rank'] = (df_wildcard
            .sort_values(by=by, ascending=ascending)
            .groupby(['date', 'conference'])
            .points.rank(method='first', ascending=False)
        )
        
        columns_to_drop = [
            'games_played',
            'division',
            'division_rank',
            'conference_rank',
            'points',
        ]
        mask = df_wildcard.conference_rank == 2
        df_wildcard = (df_wildcard.loc[mask, ]
            .drop(columns_to_drop, axis=1)
            .rename(columns={'conference': 'wildcard'})
        )

        return df_wildcard
    
    @staticmethod
    def add_wild_contender(df_full):
        df = df_full.copy()
        
        df = df.join(self.team_data, how='left', on='team')
        
        by = ['date', 'division', 'points']
        ascending = [True, True, False]
        df['division_rank'] = (df.sort_values(by=by, ascending=ascending)
            .groupby(['date', 'division'])
            .points.rank(method='first', ascending=False)
        )
        
        return df
    
    @staticmethod
    def load_team_data():
        df = (pd.read_csv(NhlGameResultsScraper.TEAM_DATA_FILENAME)
            .set_index('team')
            .drop('color', axis=1)
        )
        return df