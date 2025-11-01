from flask import Blueprint, request, jsonify,send_from_directory, send_file, Response
import io, os
from app.utils.file_util import read_docx, read_pdf
from app.models.file import File
from app.extensions import db

from app.utils.access_logs import log_access



read_bp = Blueprint("rerad_bp", __name__, url_prefix='/api/v1/read')

@read_bp.route('/<int:file_id>', methods=['GET'])
def read_file(file_id):

    file = File.query.get_or_404(file_id)
  
    if file.mime_type == 'file/pdf':
        text = read_pdf(file.filepath)
        log_access(1,"bra", file.filename, file.size, "success")
        return ({"filename": file.filename, "text":text})
    elif file.mime_type == 'file/docx':
        text= read_docx(file.filepath)
        log_access(1,"bra", file.filename, file.size, "success")
        return ({"filename": file.filename, "text":text})
    
    elif file.mime_type.startswith('image'):  
        path = f"{file.filepath}"
        filename = file.filename
        folder = path[0:-len(filename)]
        log_access(1,"bra", file.filename, file.size, "success")
        return send_from_directory(folder,filename, as_attachment=False)

    if not file.mime_type.startswith('video'):
        path = file.filepath
        range_h = request.headers.get('Range',None)
        chunk_size = 1024 * 512

        if not os.path.exists(path):
            return 'File not found',404
        

        file_size = os.path.getsize(path)
        start, end = 0, file_size - 1


        if range_h:
            bytes_range = range_h.replace("bytes=","").split("-")
            start = int(bytes_range[0])
            if bytes_range[1]:
                end = int(bytes_range[1])
            else:
                end = min(start + chunk_size - 1, file_size -1)


        print(f"New video stream started: sololeveling.mp4({file_size/1024/1024:.2f}MB)")
        progress =''

        def generate():
            total_sent = 0
            with open(path, 'rb') as f:
                f.seek(start)
                while(True):
                    data = f.read(chunk_size)
                    if not data:
                        break
                    total_sent+=len(data)

                    progress = (start + total_sent)/file_size *100
                    print(f"➡️ Sent: {progress:.2f}%")

                    yield data
        response = Response(generate(), status=206, mimetype="video/mp4")
        response.headers.add('Content-Range', f'bytes {start}-{end}/{file_size}')
        response.headers.add('Accept-Ranges', 'bytes')
        log_access(1,"bra", file.filename, file.size, "success")
        return response
      
    else:
        return jsonify({"error":"File type not readable"})
    

@read_bp.route('/img/<int:file_id>',methods=['GET'])
def view_img(file_id):
     file = File.query.get_or_404(file_id)
     path = f"{file.filepath}"
     filename = file.filename
     if file.mime_type.startswith('image'):  
        folder = path[0:-len(filename)]
        return send_from_directory(folder,filename, as_attachment=False)
     
     return jsonify({"error":"file type not readable"})




@read_bp.route('/vid/<int:file_id>')
def stream_video(file_id):

    file = File.query.get_or_404(file_id)
    if not file.mime_type.startswith('video'):
        return jsonify({"error":"file type not readable"})

  
    path = file.filepath
    range_h = request.headers.get('Range',None)
    chunk_size = 1024 * 512

    if not os.path.exists(path):
        return 'File not found',404
    

    file_size = os.path.getsize(path)
    start, end = 0, file_size - 1


    if range_h:
        bytes_range = range_h.replace("bytes=","").split("-")
        start = int(bytes_range[0])
        if bytes_range[1]:
            end = int(bytes_range[1])
        else:
            end = min(start + chunk_size - 1, file_size -1)


    print(f"New video stream started: sololeveling.mp4({file_size/1024/1024:.2f}MB)")
    progress =''

    def generate():
        total_sent = 0
        with open(path, 'rb') as f:
            f.seek(start)
            while(True):
                data = f.read(chunk_size)
                if not data:
                    break
                total_sent+=len(data)

                progress = (start + total_sent)/file_size *100
                print(f"➡️ Sent: {progress:.2f}%")

                yield data
    response = Response(generate(), status=206, mimetype="video/mp4")
    response.headers.add('Content-Range', f'bytes {start}-{end}/{file_size}')
    response.headers.add('Accept-Ranges', 'bytes')
    
    return response

