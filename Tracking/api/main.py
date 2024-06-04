from outils import read_video, save_video
from trackers import Tracker
from team_assigner import TeamAssigner
import pickle
from camera_movement_estimator import CameraMovementEstimator
from perspective_transformer import PerspectiveTransformer

def main():
 # On lit la vidéo en entrée
 video_frames = read_video('/home/foottracker/myenv/FootTracker/Tracking/input_videos/video1.mp4')

 # On instancie le Tracker
 tracker = Tracker('/home/foottracker/myenv/FootTracker/Tracking/modeles/best.pt')

 # On applique le tracking
 tracks = tracker.get_objects_tracks(video_frames, read_from_file=True, file_path='/home/foottracker/myenv/FootTracker/Tracking/tracks_files/tracks.pkl')

 # On interpole les positions de la balle
 tracks["ball"] = tracker.interpolate_ball(tracks["ball"])

 # On récupère les positions des entités
 tracker.add_position_to_tracks(tracks)

 # On estime les mouvements de la caméra
 camera_movement_estimator = CameraMovementEstimator(video_frames[0])
 camera_movement_per_frame = camera_movement_estimator.get_camera_movement(video_frames, read_from_file=True, file_path='/home/foottracker/myenv/FootTracker/Tracking/tracks_files/camera_movement.pkl')

 camera_movement_estimator.add_adjust_positions_to_tracks(tracks, camera_movement_per_frame)

 # On applique la transformation de perspective sur la partie du terrain qu'on voit toujours
 perspective_transformer = PerspectiveTransformer()
 perspective_transformer.add_transformed_positions_to_tracks(tracks)

 # On instancie un TeamAssigner
 team_assigner = TeamAssigner()

 # On récupère les couleurs des 2 équipes
 team_assigner.assign_team_color(video_frames[0], tracks['players'][0])

 # Pour chaque joueur dans chaaque frame, on lui associe son équipe (et sa couleur respective) et on l'enregistre dans les tracks
 for frame_num, player_track in enumerate(tracks['players']):
  for player_id, track in player_track.items():
        team = team_assigner.assign_player_team(video_frames[frame_num], track['bbox'], player_id)
        tracks['players'][frame_num][player_id]['team'] = team
        tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_colors[team]

 with open('/home/foottracker/myenv/FootTracker/Tracking/tracks_files/tracks.pkl', 'wb') as f:
      pickle.dump(tracks,f)
      f.close()

 # On dessine les annotations
 output_video_frames = tracker.draw_annotations(video_frames,tracks)

 # On enregistre la vidéo une fois les modifs apportées
 save_video(output_video_frames, '/home/foottracker/myenv/FootTracker/Tracking/output_videos/video1.avi')

if __name__ == '__main__': # Fait fonctionner le main
 main()