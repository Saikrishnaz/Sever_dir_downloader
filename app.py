import os
import shutil
import tempfile
from flask import Flask, render_template, send_file, abort, after_this_request

app = Flask(__name__)
# Get the parent directory of the dashboard_app folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.route("/")
def index():
    folders = []
    if os.path.exists(BASE_DIR):
        for item in os.listdir(BASE_DIR):
            item_path = os.path.join(BASE_DIR, item)
            if os.path.isdir(item_path) and item != "dashboard_app":
                # Get some stats
                try:
                    num_files = sum([len(files) for r, d, files in os.walk(item_path)])
                    folders.append({
                        "name": item,
                        "num_files": num_files
                    })
                except Exception as e:
                    pass
    
    return render_template("index.html", folders=folders)

@app.route("/download/<path:folder_name>")
def download(folder_name):
    # Security check to prevent directory traversal
    if ".." in folder_name or folder_name.startswith("/") or folder_name.startswith("\\"):
        abort(400, "Invalid folder name")
        
    folder_path = os.path.join(BASE_DIR, folder_name)
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        abort(404, "Folder not found")
        
    # Create a temporary directory to store the zip
    temp_dir = tempfile.mkdtemp()
    zip_path_base = os.path.join(temp_dir, folder_name)
    
    try:
        # Create the zip archive
        zip_filename = shutil.make_archive(zip_path_base, 'zip', folder_path)
    except Exception as e:
        abort(500, f"Error creating zip: {str(e)}")
        
    @after_this_request
    def remove_file(response):
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response

    return send_file(zip_filename, as_attachment=True, download_name=f"{folder_name}.zip")

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=7890)
