from django.shortcuts import render

#this is specifically for newsletter
#from rest_framework.views import APIView
#from rest_framework import status
#class EBookSignupView(APIView):
#    def post(self, request, format =None):
 #       data = self.request.data
 #       first_name = data['first_name']
 #       email = data['email']
 #       agree = data['agree']
 #       changing agree to a boolean value
 #       try:
 #           agree = bool(agree)
 #       except:
 #           return Response(
 #               {'error':'Must agree to Privacy Policy and Terms of Service'},
#                #now bnring in the status code,import it
#                status = status.HTTP_400_BAD_REQUEST
#            )
#
#        if not agree:
#            return Response(
 #               {'error':'Must agree to Privacy Policy and Terms of Service'},
 #               #now bnring in the status code,import it
#               status = status.HTTP_400_BAD_REQUEST
#            )
#        return Response(
#                {'success':'contact added to Newsletter'},
#                #now bnring in the status code,import it
#                status = status.HTTP_200_OK
 #           )*/


import requests
import logging
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

# Setup logging
logger = logging.getLogger(__name__)

# ActiveCampaign credentials
activecampaign_url = settings.ACTIVE_CAMPAIGN_URL
activecampaign_key = settings.ACTIVE_CAMPAIGN_KEY


@permission_classes([AllowAny])
class EBookSignupView(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            first_name = data.get('first_name')
            email = data.get('email')
            agree = data.get('agree')

            if not (first_name and email and agree):
                return Response(
                    {'error': 'First name, email, and agreement are required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create or update contact
            contact_data = {
                'contact': {
                    'email': email,
                    'firstName': first_name,
                }
            }

            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Api-Token': activecampaign_key
            }

            logger.info(f"Syncing contact: {email}")
            response = requests.post(
                f'{activecampaign_url}/api/3/contact/sync',
                json=contact_data,
                headers=headers
            )

            if response.status_code not in [200, 201]:
                logger.error(f"Contact sync failed: {response.text}")
                return Response({'error': 'Failed to sync contact.'}, status=500)

            contact = response.json()
            contact_id = str(contact['contact']['id'])
            logger.info(f"Synced contact ID: {contact_id}")

            # Use your actual IDs
            master_list_id = getattr(settings, 'AC_MASTER_LIST_ID', None)
            ebook_list_id = getattr(settings, 'AC_EBOOK_LIST_ID', None)
            tag_id = getattr(settings, 'AC_EBOOK_TAG_ID', None)

            if not master_list_id or not tag_id:
                return Response({'error': 'ActiveCampaign list or tag ID not configured.'}, status=500)

            # Add contact to lists
            if not self.add_contact_to_list(contact_id, master_list_id, headers)['success']:
                return Response({'error': 'Failed to add to master list'}, status=500)

            if ebook_list_id:
                self.add_contact_to_list(contact_id, ebook_list_id, headers)

            # Add tag by ID
            self.add_tag_to_contact(contact_id, tag_id, headers)

            return Response({'success': 'Contact successfully added!'}, status=200)

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({'error': 'Internal server error'}, status=500)

    def add_contact_to_list(self, contact_id, list_id, headers):
        try:
            payload = {
                'contactList': {
                    'list': str(list_id),
                    'contact': contact_id,
                    'status': '1'
                }
            }
            response = requests.post(
                f'{activecampaign_url}/api/3/contactLists',
                json=payload,
                headers=headers
            )

            if response.status_code in [200, 201]:
                return {'success': True}
            else:
                logger.error(f"List add failed: {response.text}")
                return {'success': False, 'error': response.text}
        except Exception as e:
            logger.error(f"List add exception: {e}")
            return {'success': False, 'error': str(e)}

    def add_tag_to_contact(self, contact_id, tag_id, headers):
        try:
            payload = {
                'contactTag': {
                    'contact': contact_id,
                    'tag': str(tag_id)
                }
            }
            response = requests.post(
                f'{activecampaign_url}/api/3/contactTags',
                json=payload,
                headers=headers
            )

            if response.status_code in [200, 201]:
                return {'success': True}
            else:
                logger.warning(f"Tag add failed: {response.text}")
                return {'success': False, 'error': response.text}
        except Exception as e:
            logger.warning(f"Tag add exception: {e}")
            return {'success': False, 'error': str(e)}
