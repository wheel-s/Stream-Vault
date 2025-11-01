from flask import Blueprint, request, jsonify , current_app
from app.utils.file_util import allowed_file, save_file
from app.utils.video_util import generate_thumbnail
from app.utils.upload_logs import log_upload
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.file import File
import os




upload_bp = Blueprint('upload_bp',__name__, url_prefix='/api/v1/upload')


upload_root = os.path.join(os.getcwd(), 'uploads')


video =["mp4", "avi", "mov"]
image = ["jpeg", "jpg", "png", "webp", "avif"]
docs = ["pdf", "docx"]


@upload_bp.route('/up', methods = ['POST'])
@jwt_required()
def upload_file():
    identity = get_jwt_identity()
    if  "file" not in request.files:
        return jsonify({"error":"No file part"}), 400
    
    file =request.files['file']

    user_id = identity["id"]

    if file.filename == "":
        return jsonify({"error":"No  selscted File"}), 400
    
    if file and allowed_file(file.filename):

        user_folder = os.path.join(upload_root, str(user_id))
        thumbnail_folder = os.path.join(user_folder, 'Thumbnails')
        videos = os.path.join(user_folder, 'videos')
        images = os.path.join(user_folder, 'images')
        documents = os.path.join(user_folder, 'documents')
        others = os.path.join(user_folder, 'others')

        os.makedirs(user_folder, exist_ok=True)   
        os.makedirs(thumbnail_folder, exist_ok=True)
        os.makedirs(videos, exist_ok=True)
        os.makedirs(images, exist_ok=True)
        os.makedirs(documents, exist_ok=True)
        os.makedirs(others, exist_ok=True)
     
        filetype = file.filename.rsplit(".",1)[1].lower()
    
        if filetype in video:
            mimetype = f'video/{filetype}'
            filename, filepath = save_file(file, videos)
            file1 = file.filename.rsplit(".",1)[0].lower() 
            
            generate_thumbnail(f"{videos}\\{filename}", f"{thumbnail_folder}\\{file1}.png")
        elif filetype in image:
            mimetype = f'image/{filetype}'
            filename, filepath = save_file(file, images)
     
        elif filetype in docs:
            mimetype =f'file/{filetype}'
            filename, filepath = save_file(file, documents)

        size = os.path.getsize(filepath)
        log_upload(user_id, filename,size, "success")
        new_file = File(user_id = user_id,filename =filename, filepath = filepath, mime_type = mimetype, size=size)
        db.session.add(new_file)
        db.session.commit()
        return jsonify({"message":"File uploaded", "filename":filename}), 201
    
    return jsonify({"error":"file type not allowed"}), 400





@upload_bp.route('/',methods=['GET'])
@jwt_required()
def list_files():
   
    identity = get_jwt_identity()
    user_id = identity["id"]
    if identity["role"] == "admin":
        files = File.query.all()
        return jsonify([{
            "id:":f.id,
            "filename":f.filename,
            "size":f"{f.size} bytes",
            "uploaded_at":f.uploaded_at
        } for f in files])

    files = File.query.filter_by(user_id = user_id ).all()
    return jsonify([{
            "id:":f.id,
            "filename":f.filename,
             "size":f"{f.size} bytes",
            "uploaded_at":f.uploaded_at
        } for f in files])




@upload_bp.route("/<int:file_id>", methods=['GET'])
def view_file(file_id):
    file = File.query.filter_by(id = file_id).first()
    return jsonify({  
        "id:":file.id,
        "filename":file.filename,
        "size":f"{file.size} bytes",
        "mime_type":file.mime_type,
        "uploaded_at":file.uploaded_at})