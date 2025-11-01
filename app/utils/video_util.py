import os
from moviepy import VideoFileClip
from flask import request, Response




def generate_thumbnail(video_path, thumbnail_path):
    clip = VideoFileClip(video_path)

    clip.save_frame(thumbnail_path, t=2.0)
    return thumbnail_path

