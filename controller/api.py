


from flask import jsonify, request
import requests
from app import Crpm, app


# @app.route('/api/get_sms', methods=['GET'])
# def get_sms():
#     query = Crpm.query
#     result = query.all()
#     sms_list = []
#     for entry in result:
#         sms_list.append({
#             'transactionId': entry.transactionId,
#             'recipient': entry.recpient,
#             'sender': entry.sender,
#             'description': entry.description,
#             'totalPdu': entry.totalPdu,
#             'deliverystatus': entry.deliverystatus,
#             'deliverydt': entry.deliverydt,
#             'submitdt': entry.submitdt,
#             'corelationId': entry.corelationId,
#             'message': entry.message
#         })
#     return jsonify(sms_list)


# @app.route('/api/add_sms', methods=['POST'])
# def add_sms():
#     if request.method == 'POST':
#         data = request.json
#         sms = Crpm(
#             transactionId=data.get('transactionId'),
#             recpient=data.get('recpient'),
#             sender=data.get('sender'),
#             description=data.get('description'),
#             totalPdu=data.get('totalPdu'),
#             status=data.get('status'),
#             doneDate=data.get('doneDate'),
#             submittedDate=data.get('submittedDate'),
#             corelationid=data.get('corelationid'),
#             message=data.get('message')
#         )
#         db.session.add(sms)
#         db.session.commit()
        
#         return jsonify({'message': 'Crpm data added successfully'})



    