from django.http import JsonResponse
from .models import *
from django.views import View

class ResidenceDetailView(View) :
    def get(self, request, residence_name) :
        try :
               
            Residence.objects.prefetch_related('rooms','places','residence_images').filter(name = residence_name)
            residences = Residence.objects.get(name = residence_name)
           
            residence_info = {
        
                'residence_id'              : residences.id,
                'name'                      : residences.name,
                'sub_name'                  : residences.sub_name,
                'category'                  : residences.category.title,
                'region'                    : residences.region.title,
                'residence_thumbnail'       : residences.thumbnail,
                'description'               : residences.description,
                'latitude'                  : residences.latitude,
                'longitude'                 : residences.longitude,
                'address'                   : residences.address,
                'email'                     : residences.email,
                'image'                     : [residence.image_url for residence in residences.residence_images.all()],
                
                'room_info' :[{
                    'room_id'        : room.id ,
                    'room_name'      : room.name, 
                    'room_images'    : [room_image.image_url for room_image in room.room_images.all()],
                    'price'          : room.price,
                    'person'         : room.person,       
                    'max_person'     : room.max_person,
                    'bedspace'       : room.bedspace,   
                    
                }for room in residences.rooms.all()],
                
                'places' : [{
                    'place_name'  : place.name,
                    'description' : place.description,
                    'latitude'    : place.latitude,
                    'longitude'   : place.longitude
                    
                }for place in residences.places.all()]
            }

            return JsonResponse({'result' : residence_info}, status = 200)
        
        except Residence.DoesNotExist:
            return JsonResponse({'message' : 'RESIDENCE_NOT_FOUND'}, status = 404)

class RoomDetailView(View) :
    def get(self, request, residence_name):
        try:
            room_id = request.GET["room_id"]
            
            Residence.objects.prefetch_related('room').filter(name = residence_name)
            Room.objects.prefetch_related('room_amenities', 'room_features')
                  
            chosen_residence        = Residence.objects.get(name = residence_name)
            chosen_room             = Room.objects.get(id = room_id)

            room_info = {
                'id'               : chosen_room.id,
                'residence_name'   : chosen_residence.name,
                'name'             : chosen_room.name,
                'price'            : chosen_room.price,
                'room_images'      : [value.image_url for value in chosen_room.room_images.all()],
                'description'      : chosen_room.description,
                'person'           : chosen_room.person,
                'max_person'       : chosen_room.max_person,
                'area'             : chosen_room.area,
                'bed'              : chosen_room.bedspace,
                'feature'          : [feature.feature.name for feature in chosen_room.room_features.all()],
                'amenities'        : [amenity.amenity.name for amenity in chosen_room.room_amenities.all()]
                }
                         
            return JsonResponse({'result' : room_info }, status =200)
        
        except Room.DoesNotExist:
            return JsonResponse({'message' : 'ROOM_NOT_FOUND'}, status = 404)
        
