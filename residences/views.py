from django.http import JsonResponse
from django.views import View

from .models import *


class ResidenceDetailView(View) :
    def get(self, request, id) :
        try :
            residence = Residence.objects.prefetch_related('rooms__room_images','places','residence_images').get(id = id)
           
            result = {
                'id'                        : residence.id,
                'name'                      : residence.name,
                'sub_name'                  : residence.sub_name,
                'category'                  : residence.category.title,
                'region'                    : residence.region.title,
                'residence_thumbnail'       : residence.thumbnail,
                'description'               : residence.description,
                'latitude'                  : residence.latitude,
                'longitude'                 : residence.longitude,
                'address'                   : residence.address,
                'email'                     : residence.email,
                'image'                     : [residence.image_url for residence in residence.residence_images.all()],
            
                'rooms' :[{
                    'id'        : room.id ,
                    'name'      : room.name, 
                    'images'    : [room_image.image_url for room_image in room.room_images.all()],
                    'price'          : room.price,
                    'person'         : room.person,       
                    'max_person'     : room.max_person,
                    'bedspace'       : room.bedspace,  
                } for room in residence.rooms.all()],
                
                'places' : [{
                    'place_name'  : place.name,
                    'description' : place.description,
                    'latitude'    : place.latitude,
                    'longitude'   : place.longitude             
                }for place in residence.places.all()]
            }

            return JsonResponse({'result' : result}, status = 200)
        
        except Residence.DoesNotExist:
            return JsonResponse({'message' : 'RESIDENCE_NOT_FOUND'}, status = 404)

# 8000/rooms/1
# 8000/residence/10/rooms/1


class RoomDetailView(View) :
    def get(self, request, residence_id, room_id):
        try:            
            room = Room.objects.prefetch_related('room_amenities', 'room_features', 'room_images').get(id=room_id)
                
            room_info = {
                'id'               : room.id,
                'residence_name'   : room.residence.name,
                'name'             : room.name,
                'price'            : room.price,
                'room_images'      : [value.image_url for value in room.room_images.all()],
                'description'      : room.description,
                'person'           : room.person,
                'max_person'       : room.max_person,
                'area'             : room.area,
                'bed'              : room.bedspace,
                'feature'          : [feature.feature.name for feature in room.room_features.all()],
                'amenities'        : [amenity.amenity.name for amenity in room.room_amenities.all()]
                }
                         
            return JsonResponse({'result' : room_info }, status =200)
        
        except Room.DoesNotExist:
            return JsonResponse({'message' : 'ROOM_NOT_FOUND'}, status = 404)
        
