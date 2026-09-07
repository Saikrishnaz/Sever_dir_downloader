import os
import shutil
import tempfile
from flask import Flask, render_template, send_file, abort, after_this_request, request

app = Flask(__name__)
# Get the parent directory of the dashboard_app folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def resolve_path(relative_path=""):
    """Resolve a requested path while keeping it inside BASE_DIR."""
    base_path = os.path.realpath(BASE_DIR)
    requested_path = os.path.realpath(os.path.join(base_path, relative_path))
    if os.path.commonpath([base_path, requested_path]) != base_path:
        abort(400, "Invalid path")
    return requested_path

@app.route("/")
def index():
    relative_path = request.args.get("path", "").strip("/")
    current_path = resolve_path(relative_path)
    if not os.path.isdir(current_path):
        abort(404, "Directory not found")

    folders = []
    files = []
    for item in sorted(os.listdir(current_path), key=str.lower):
        item_path = os.path.join(current_path, item)
        try:
            if os.path.isdir(item_path):
                num_files = sum(len(file_names) for _, _, file_names in os.walk(item_path))
                folders.append({"name": item, "path": os.path.join(relative_path, item), "num_files": num_files})
            elif os.path.isfile(item_path):
                files.append({"name": item, "path": os.path.join(relative_path, item)})
        except OSError:
            continue

    breadcrumbs = []
    accumulated_path = ""
    for part in relative_path.split("/") if relative_path else []:
        accumulated_path = os.path.join(accumulated_path, part)
        breadcrumbs.append({"name": part, "path": accumulated_path})

    parent_path = os.path.dirname(relative_path) if relative_path else None
    return render_template(
        "index.html",
        folders=folders,
        files=files,
        current_path=relative_path,
        breadcrumbs=breadcrumbs,
        parent_path=parent_path,
    )

@app.route("/download/<path:folder_name>")
def download(folder_name):
    folder_path = resolve_path(folder_name)
    if not os.path.isdir(folder_path):
        abort(404, "Folder not found")
        
    # Create a temporary directory to store the zip
    temp_dir = tempfile.mkdtemp()
    zip_name = os.path.basename(os.path.normpath(folder_name))
    zip_path_base = os.path.join(temp_dir, zip_name)
    
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

    return send_file(zip_filename, as_attachment=True, download_name=f"{zip_name}.zip")

@app.route("/file/<path:file_name>")
def download_file(file_name):
    file_path = resolve_path(file_name)
    if not os.path.isfile(file_path):
        abort(404, "File not found")
    return send_file(file_path, as_attachment=True, download_name=os.path.basename(file_path))

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=7890)
