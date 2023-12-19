# Définition des caractéristiques de base et de leur extension pour chaque modèle
base_features = {
    'common': ['strength', 'is_playoff', 'time_since_prev_event', 'is_rebound',
               'distance_to_prev_event', 'speed_since_prev_event', 'is_penalty_shot',
               'shot_distance', 'shot_angle', 'change_in_angle', 'time_since_pp',
               'relative_strength', 'shot_type_Backhand', 'shot_type_Deflected',
               'shot_type_Slap Shot', 'shot_type_Snap Shot', 'shot_type_Tip-In',
               'shot_type_Wrap-around', 'shot_type_Wrist Shot',
               'prev_event_type_Blocked Shot', 'prev_event_type_Faceoff',
               'prev_event_type_Giveaway', 'prev_event_type_Goal',
               'prev_event_type_Hit', 'prev_event_type_Missed Shot',
               'prev_event_type_Penalty', 'prev_event_type_Shot', 'prev_event_type_Takeaway'],
    'coordinates': ['x_coordinate', 'y_coordinate'],
    'game_info': ['period', 'game_time(s)', 'prev_event_x', 'prev_event_y'],
    'team_strength': ['home_strength', 'away_strength']
}

# Construction des listes de caractéristiques pour différents modèles
feature_list_xgb = base_features['common'] + base_features['coordinates'] + base_features['game_info'] + base_features['team_strength']
feature_list_lgbm = feature_list_xgb.copy()
feature_list_nn = [feature for feature in base_features['common'] if feature not in ['x_coordinate', 'y_coordinate', 'prev_event_x', 'prev_event_y', 'period', 'game_time(s)']]
feature_list_logreg = ['shot_distance', 'shot_angle']
feature_list_stack_trained = feature_list_xgb.copy()
feature_list = base_features['common'] + base_features['game_info'] + ['shot_type', 'prev_event_type']

# Affichage des listes de caractéristiques
print("Feature List for XGBoost:", feature_list_xgb)
print("Feature List for LightGBM:", feature_list_lgbm)
print("Feature List for Neural Network:", feature_list_nn)
print("Feature List for Logistic Regression:", feature_list_logreg)
print("Feature List for Stacked Model:", feature_list_stack_trained)
print("General Feature List:", feature_list)
