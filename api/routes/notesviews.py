from flask_restx import Namespace, Resource, fields, abort
from http import HTTPStatus
from flask import request, jsonify
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models.models import User, Note, NoteVersion, owners_table
from ..database import db

notes_namespace = Namespace('notes', description="Definitions for Notes routes")

note_model = notes_namespace.model(
    'Note', {
        'id': fields.Integer(description="Id for notes"),
        'heading': fields.String(description="Heading of the node", required=True),
        'content': fields.String(description="Content of the note", required=True),
    }
)

share_model = notes_namespace.model(
    'ShareNote', {
        'note_id': fields.Integer(description="Id for note to be shared", required=True),
        'users': fields.List(fields.Integer(description="User id"), description="List of User Id to share notes with",
                              required=True),
    }
)


@notes_namespace.route('/create')
class CreateNote(Resource):

    @notes_namespace.expect(note_model, validate=True)
    @notes_namespace.doc(
        description="Create a new note",
        security="Bearer Auth",
    )
    @jwt_required()
    def post(self):
        """
        Create a new note
        """
        try:
            data = request.get_json()

            new_note = Note(
                heading=data['heading'],
                content=data['content'],
            )
            new_note.save()

            db.session.execute(owners_table.insert().values(user_id=get_jwt_identity(), note_id=new_note.id))
            db.session.commit()

            created_note_data = {
                "message": f"Note with id {new_note.id} created"
            }

            return created_note_data, HTTPStatus.CREATED

        except Exception as e:

            return {"message": str(e)}, HTTPStatus.BAD_REQUEST


@notes_namespace.route('/<int:note_id>')
class RetrieveAndUpdateNote(Resource):

    @notes_namespace.marshal_with(note_model)
    @notes_namespace.doc(
        description="Retrieve a note by ID",
        security="Bearer Auth",
        params={
            "note_id": "An ID for a given note"
        }
    )
    @jwt_required()
    def get(self, note_id):
        """
        Retrieve a note by ID
        """

        user_id = get_jwt_identity()

        note = Note.query.filter_by(id=note_id).first()

        if note:
            if user_id in [shared_user.id for shared_user in note.owners]:
                return note, HTTPStatus.OK
            else:
                return {
                           "message": "You are unauthorized to access this note"
                       }, HTTPStatus.UNAUTHORIZED
        else:
            return {
                       "message": "Note not found"
                   }, HTTPStatus.NOT_FOUND

    @notes_namespace.expect(note_model, validate=True)
    @notes_namespace.doc(
        description="Update a note by ID",
        security="Bearer Auth",
        params={
            "note_id": "An ID for a given note"
        }
    )
    @jwt_required()
    def put(self, note_id):
        """
        Update a note by ID
        """
        user_id = get_jwt_identity()
        update_data = request.get_json()

        note = Note.query.filter_by(id=note_id).first()

        if note:
            if user_id in [owner.id for owner in note.owners]:
                note.content += "\n" + update_data['content']
                note.updated_at = datetime.utcnow()
                note.save()

                # Log version history
                version = NoteVersion(
                    note_id=note_id,
                    timestamp=datetime.utcnow(),
                    user_id=user_id,
                    changes=update_data['content']
                )
                version.save()

                return {"message": f"Note updated successfully"}, HTTPStatus.OK
            else:
                return {"message": "You are unauthorized to update this note"}, HTTPStatus.UNAUTHORIZED
        else:
            return {"message": "Note not found"}, HTTPStatus.NOT_FOUND


@notes_namespace.route('/share')
class ShareNote(Resource):

    @notes_namespace.expect(share_model, validate=True)
    @notes_namespace.doc(
        description="Share a note with other users",
        security="Bearer Auth",
    )
    @jwt_required()
    def post(self):
        """
        Share a note with other users
        """

        user_id = get_jwt_identity()

        data = request.get_json()

        note_id = data.get('note_id')
        users_to_share_with = data.get('users', [])

        note = Note.query.get(note_id)

        if not note:
            return {"message": "Note not found"}, HTTPStatus.NOT_FOUND

        if user_id != note.user_id:
            return {"message": "You are not authorized to share this note"}, HTTPStatus.UNAUTHORIZED

        # Share the note with the specified users
        for user_id_to_share_with in users_to_share_with:
            user_to_share_with = User.query.get(user_id_to_share_with)
            if user_to_share_with:
                note.owners.append(user_to_share_with)
            else:
                return {"message": f"User with ID {user_id_to_share_with} not found"}, HTTPStatus.NOT_FOUND

        db.session.commit()

        return {"message": "Note shared successfully"}, HTTPStatus.OK


@notes_namespace.route('/version-history/<int:note_id>')
class VersionHistory(Resource):

    @notes_namespace.doc(
        description="Retrieve the version history of a note by ID",
        security="Bearer Auth",
        params={"note_id": "ID of the note to retrieve version history"}
    )
    @jwt_required()
    def get(self, note_id):
        """
        Retrieve the version history of a note by ID
        """
        user_id = get_jwt_identity()

        note = Note.query.filter_by(id=note_id).first()

        if not note:
            return {"message": "Note not found"}, HTTPStatus.NOT_FOUND

        if user_id not in [owner.id for owner in note.owners]:
            return {"message": "You are unauthorized to access this note"}, HTTPStatus.UNAUTHORIZED

        versions = note.versions.all()

        version_history = []
        for version in versions:
            version_info = {
                "timestamp": version.timestamp,
                "user": User.query.get(version.user_id).username,
                "changes": version.changes
            }
            version_history.append(version_info)

        return jsonify(version_history), HTTPStatus.OK


