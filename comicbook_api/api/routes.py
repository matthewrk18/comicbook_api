from flask import Blueprint, request, jsonify

from comicbook_api.helpers import token_required
from comicbook_api.models import User, Comic, db, comic_schema, comics_schema


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 800}



@api.route('/comics', methods=['POST'])
@token_required
def create_comic(current_user_token):
    publisher = request.json['publisher']
    title = request.json['title']
    volume_num = request.json['volume_num']
    issue_num = request.json['issue_num']
    print_num = request.json['print_num']
    cover_date = request.json['cover_date']
    cover_price = request.json['cover_price']
    condition = request.json['condition']
    comments = request.json['comments']
    token = current_user_token.token

    print(f'TEST: {current_user_token.token}')

    comic = Comic(publisher, title, volume_num, issue_num, print_num, cover_date, cover_price, condition, comments, user_token = token)

    db.session.add(comic)
    db.session.commit()

    response = comic_schema.dump(comic)
    return jsonify(response)


@api.route('/comics', methods = ['Get'])
@token_required
def get_comics(current_user_token):
    owner = current_user_token.token
    comics = Comic.query.filter_by(user_token = owner).all()
    response = comics_schema.dump(comics)
    return jsonify(response)


@api.route('/comics/<id>', methods = ['GET'])
@token_required
def get_comic(current_user_token, id):
    comic = Comic.query.get(id)
    response = comic_schema.dump(comic)
    return jsonify(response)



@api.route('/comics/<id>', methods = ['POST', 'PUT'])
@token_required
def update_comic(current_user_token, id):
    comic = Comic.query.get(id)
    print(comic)
    if comic:
        comic.publisher = request.json['publisher']
        comic.title = request.json['title']
        comic.volume_num = request.json['volume_num']
        comic.issue_num = request.json['issue_num']
        comic.print_num = request.json['print_num']
        comic.cover_date = request.json['cover_date']
        comic.cover_price = request.json['cover_price']
        comic.condition = request.json['condition']
        comic.comments = request.json['comments']
        comic.user_token = current_user_token.token
        db.session.commit()

        response = comic_schema.dump(comic)
        return jsonify(response)
    
    else:
        return jsonify({'Error': 'That comic does not exist!'})


@api.route('/comics/<id>', methods = ['DELETE'])
@token_required
def delete_comic(current_user_token, id):
    comic = Comic.query.get(id)
    
    if comic:
        db.session.delete(comic)
        db.session.commit()
        return jsonify({'Success': f'Comic ID # {comic.id} has been deleted'})

    else:
        return jsonify({'Error': 'That comic does not exist!'})