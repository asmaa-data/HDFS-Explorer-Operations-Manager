from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import subprocess
import os
import tempfile
import shutil
import uuid

os.environ["HADOOP_USER_NAME"] = "bigdata"
os.environ["HADOOP_HOME"] = "/usr/local/hadoop"
os.environ["PATH"] += ":/usr/local/hadoop/bin"

app = Flask(__name__)

# =========================================================
# CONFIGURATION
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMP_FOLDER = os.path.join(BASE_DIR, "temp")
UPLOAD_FOLDER = os.path.join(BASE_DIR,"uploads")


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

# =========================================================
# HELPER FUNCTION
# Execute HDFS Commands
# =========================================================

def run_hdfs_command(command):
    print("RUN:", command)

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    print("RETURN CODE:", result.returncode)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    return result.stdout + result.stderr

# =========================================================
# FEATURE: LIST FILES / DYNAMIC NAVIGATION
# =========================================================

@app.route("/")
@app.route("/browse")
def browse():

    path = request.args.get("path", "/")

    command = f'/home/bigdata/hadoop-2.7.3/bin/hdfs dfs -ls "{path}"'

    output = run_hdfs_command(command)
    if "No such file" in output or "command not found" in output:
        return f"<pre style='color:red'>{output}</pre>"

    files = []

    lines = output.split("\n")

    for line in lines:

        parts = line.split()

        if len(parts) >= 8:

            permissions = parts[0]
            owner = parts[2]
            size = parts[4]
            date = parts[5]
            time = parts[6]
            file_path = parts[7]

            name = os.path.basename(file_path)

            file_type = "directory" if permissions.startswith("d") else "file"

            files.append({
                "permissions": permissions,
                "owner": owner,
                "size": size,
                "date": date,
                "time": time,
                "path": file_path,
                "name": name,
                "type": file_type
            })

    return render_template(
        "index.html",
        files=files,
        current_path=path
    )

# =========================================================
# FEATURE: CREATE DIRECTORY
# =========================================================

@app.route("/mkdir", methods=["POST"])
def mkdir():

    current_path = request.form.get("current_path")
    folder_name = request.form.get("folder_name")

    if not folder_name:
        return redirect(url_for("browse", path=current_path))

    target_path = current_path.rstrip("/") + "/" + folder_name

    command = f'/home/bigdata/hadoop-2.7.3/bin/hdfs dfs -mkdir "{target_path}"'

    result = run_hdfs_command(command)

    print(result)

    return redirect(url_for("browse", path=current_path))
# =========================================================
# FEATURE: CREATE file
# =========================================================

@app.route("/touch", methods=["POST"])
def touch_file():

    current_path = request.form.get("current_path")
    file_name = request.form.get("file_name")

    if not file_name:
        return redirect(url_for("browse", path=current_path))

    # HDFS destination
    hdfs_path = current_path.rstrip("/") + "/" + file_name

    # Local temporary file
    local_temp = "/tmp/" + file_name

    # Create empty local file
    open(local_temp, "w").close()

    # Upload to HDFS
    command = '/home/bigdata/hadoop-2.7.3/bin/hdfs dfs -put "{}" "{}"'.format(
        local_temp,
        hdfs_path
    )

    result = run_hdfs_command(command)

    print(result)

    # Remove local temp file
    os.remove(local_temp)

    return redirect(url_for("browse", path=current_path))
# =========================================================
# FEATURE: DELETE FILE OR DIRECTORY
# =========================================================

@app.route("/delete", methods=["POST"])
def delete_item():

    path = request.form.get("path")
    current_path = request.form.get("current_path")

    command = f'/home/bigdata/hadoop-2.7.3/bin/hdfs dfs -rm -r -skipTrash "{path}"'

    result=run_hdfs_command(command)
    print (result)

    return redirect(url_for("browse", path=current_path))

# =========================================================
# FEATURE: RENAME FILE OR DIRECTORY
# =========================================================

@app.route("/rename", methods=["POST"])
def rename_item():

    old_path = request.form.get("old_path")
    new_name = request.form.get("new_name")
    current_path = request.form.get("current_path")

    parent_dir = os.path.dirname(old_path)

    new_path = os.path.join(parent_dir, new_name)

    command = f'/home/bigdata/hadoop-2.7.3/bin/hdfs dfs -mv "{old_path}" "{new_path}"'

    run_hdfs_command(command)

    return redirect(url_for("browse", path=current_path))

# =========================================================
# FEATURE: MOVE FILE OR DIRECTORY
# =========================================================

@app.route("/move", methods=["POST"])
def move_item():

    source = request.form.get("source")
    destination = request.form.get("destination")
    current_path = request.form.get("current_path")

    command = f'/home/bigdata/hadoop-2.7.3/bin/hdfs dfs -mv "{source}" "{destination}"'

    run_hdfs_command(command)

    return redirect(url_for("browse", path=current_path))

# =========================================================
# FEATURE: COPY FILE OR DIRECTORY
# =========================================================

@app.route("/copy", methods=["POST"])
def copy_item():

    source = request.form.get("source")
    destination = request.form.get("destination")
    current_path = request.form.get("current_path")

    command = f'/home/bigdata/hadoop-2.7.3/bin/hdfs dfs -cp "{source}" "{destination}"'

    run_hdfs_command(command)

    return redirect(url_for("browse", path=current_path))

# =========================================================
# FEATURE: UPLOAD FILES TO HDFS
# =========================================================

@app.route("/upload", methods=["POST"])
def upload():

    current_path = request.form.get("current_path")

    uploaded_files = request.files.getlist("files")

    for file in uploaded_files:

        local_path = os.path.join(UPLOAD_FOLDER, file.filename)

        file.save(local_path)

        command = f'/home/bigdata/hadoop-2.7.3/bin/hdfs dfs -put "{local_path}" "{current_path}"'

        run_hdfs_command(command)

        os.remove(local_path)

    return redirect(url_for("browse", path=current_path))

# =========================================================
# FEATURE: DOWNLOAD FILE FROM HDFS
# =========================================================

@app.route("/download")
def download():

    hdfs_path = request.args.get("path")

    filename = os.path.basename(hdfs_path)

    local_temp = os.path.join(TEMP_FOLDER, f"{uuid.uuid4()}_{filename}")

    command = f'/home/bigdata/hadoop-2.7.3/bin/hdfs dfs -get "{hdfs_path}" "{local_temp}"'

    run_hdfs_command(command)

    return send_file(local_temp, as_attachment=True)

# =========================================================
# FEATURE: VIEW FILE CONTENT
# =========================================================

@app.route("/view")
def view_file():

    path = request.args.get("path")

    command = f'/home/bigdata/hadoop-2.7.3/bin/hdfs dfs -cat "{path}"'

    content = run_hdfs_command(command)

    return f"""
    <html>
    <head>
        <title>View File</title>
        <style>
            body {{
                background: #111827;
                color: white;
                font-family: monospace;
                padding: 20px;
            }}
            pre {{
                white-space: pre-wrap;
                word-wrap: break-word;
            }}
        </style>
    </head>
    <body>
        <h2>{path}</h2>
        <pre>{content}</pre>
    </body>
    </html>
    """

# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

