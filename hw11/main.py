import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, LargeBinary

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///database.sqlite')


class ReprMixin:
    def __repr__(self):
        d = {k: v for k, v in vars(self).items()
             if not k.startswith('_')}
        basic = super().__repr__()
        if not d:
            return basic
        basic, cut = basic[:-1], basic[-1]

        add = ', '.join([f'{k}={v!r}' for k, v in d.items()])

        res = f'{basic} ~ ({add}){cut}'
        return res


class File(ReprMixin, db.Model):
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    directory_id = Column(Integer)
    size = Column(Integer)
    content = Column(LargeBinary)


class Directory(ReprMixin, db.Model):
    __tablename__ = 'directories'
    id = Column(Integer, primary_key=True)
    name = Column(String(32 + len('.webm')))
    parent_id = Column(Integer)


def list_files(dir):
    # List of file objects that we are going to gather and return
    files = []
    # Use the os module to list the files in the folder
    file_names = os.listdir(f"./{dir.name}")
    id = get_last_file_id() + 1
    # Loop through each file and print its name, size, and content
    for file in file_names:
        # Get the full path to the file
        file_path = os.path.join(f"./{dir.name}", file)

        # Get the size of the file
        file_size = os.path.getsize(file_path)

        # Open the file and read its content
        with open(file_path, "rb") as f:
            file_content = f.read()

        # Add the details to our Files array with defined fields
        files.append(File(id=id, name=file, directory_id=dir.id, size=file_size, content=file_content))

        # Increment the file ID
        id += 1
    return files


def get_dir_name(id):
    directories = Directory.query.all()
    for dir in directories:
        if dir.id == id:
            return dir.name
    return None


def get_dir_id(name):
    directories = Directory.query.all()
    for dir in directories:
        if dir.name == name:
            return dir.id
    return None


def get_last_dir_id():
    directories = Directory.query.all()
    if len(directories) > 0:
        return directories[-1].id
    else:
        return 0


def get_last_file_id():
    files = File.query.all()
    if len(files) > 0:
        return files[-1].id
    else:
        return 0


def get_files_in_dir(dir_name):
    file_list = []
    # Create a list of dictionaries from the files
    for f in File.query.all():
        if dir_name == get_dir_name(f.directory_id):
            file_list.append({
                'name': f.name, 'directory': get_dir_name(f.directory_id), 'size': f.size, 'content': str(f.content)
            })
    return file_list


def save_dir_in_db(name):
    directory = Directory(id=get_last_dir_id() + 1, name=name, parent_id=get_last_dir_id())
    db.session.add(directory)
    db.session.commit()

    # Add the files to our database
    for f in list_files(directory):
        db.session.add(f)
    # Commit the changes
    db.session.commit()


'''
    Below start the Flask app routes
'''


# dummy route used to view dummy files in a sample folder
@app.route('/files')
@app.route('/files/')
def get_files():
    # Get dummy files data from the database that are inside the sample_files folder
    return jsonify(get_files_in_dir('sample_files'))


# route that allows to view all files inside a specific folder in the project directory
@app.route('/directory/<name>')
@app.route('/directory/<name>/')
def get_files_from_directory(name):
    save_dir_in_db(name=name)
    return jsonify(get_files_in_dir(name))


# route used to view all directories and files currently added to the database
@app.route('/view_database')
@app.route('/view_database/')
def view_database():
    db = {}
    for dir in Directory.query.all():
        db[dir.name] = get_files_in_dir(dir.name)
    return jsonify(db)


# route used to get info about the file inside a specific folder by its name
# simply works like a search option
@app.route('/<directory>/<file>')
@app.route('/<directory>/<file>/')
def get_file_from_directory(directory, file):
    for f in get_files_in_dir(directory):
        if f['name'] == file:
            return jsonify(f)
    return None


# route allowing to modify the content data of the file stored in the database by its directory location and file name
@app.route('/change_file/<directory>/<file>/<data>')
@app.route('/change_file/<directory>/<file>/<data>/')
def change_file_in_directory(directory, file, data):
    # Find the file object based on the directory name and file name
    file_obj = File.query.filter_by(directory_id=get_dir_id(directory), name=file).first()

    if file_obj:
        # Update the file content with the provided data
        file_obj.content = data.encode('utf-8')

        # Commit the changes to the database
        db.session.commit()

        # Return the updated file as a JSON response
        return jsonify({
            'name': file_obj.name,
            'directory': get_dir_name(file_obj.directory_id),
            'size': file_obj.size,
            'content': str(file_obj.content, 'utf-8')
        })
    else:
        # Return a 404 Not Found error if the file was not found
        return jsonify({'error': 'File not found'}), 404


# route allowing to remove files from the database by the specified directory and file name
@app.route('/remove_file/<directory>/<file>')
@app.route('/remove_file/<directory>/<file>/')
def remove_file_from_directory(directory, file):
    # Find the file in the database
    file_to_delete = File.query.filter_by(name=file, directory_id=get_dir_id(directory)).first()

    # If the file exists, delete it from the database
    if file_to_delete:
        db.session.delete(file_to_delete)
        db.session.commit()
        return jsonify({'message': f'File "{file}" in directory "{directory}" was successfully deleted'})
    else:
        return jsonify({'message': f'File "{file}" in directory "{directory}" was not found'})


if __name__ == '__main__':

    # Delete the existing database file
    if os.path.exists('./instance/database.sqlite'):
        os.remove('./instance/database.sqlite')

    db.init_app(app)

    with app.app_context():
        db.create_all()
        save_dir_in_db('sample_files')
        # Get all files from db
        files = File.query.all()
        print(files)
    app.run(debug=True)
