from django.http       import JsonResponse
from django.views      import View

from .models import Residence, RegionEnum, Room

class ResidenceListView(View):
    def get(self, request):
        limit     = int(request.GET.get('limit', 10))
        offset    = int(request.GET.get('offset', 0))
        sort      = request.GET.get('sort', 'id')
        region    = request.GET.getlist('region', [RegionEnum.get_regions()])

        filter_options = {
            'category'  : 'category__title',
            'search'    : 'name__icontains',
            'people'    : 'rooms__max_person__gte',
            'min-price' : 'rooms__price__gte',
            'max-price' : 'rooms__price__lte'
        }
        filter_list_option = {
            'region'    : 'region__title__in'
        }
        sort_type = {
            'id'        : 'id',
            'new'       : '-created_at',
            'high-price': '-room__price',
            'low-price' : 'room__price'
        }
        
        filter_set = {**{filter_list_option.get(key) : value for key, value in dict(request.GET).items()
                if filter_list_option.get(key)},
                **{filter_options.get(key) : value for key, value in request.GET.items()
                if filter_options.get(key)}
        }

        residences = Residence.objects.filter(**filter_set)\
                        .select_related('region', 'category')\
                        .prefetch_related('rooms', 'residence_images')\
                        .order_by(sort_type[sort])[offset:offset+limit]

        residences_list = [{
            'id'       : residence.id,
            'name'     : residence.name,
            'sub_name' : residence.sub_name,
            'thumbnail': residence.thumbnail,
            'region'   : residence.region.title,
            'category' : residence.category.title,
            'image'    : [image.image_url for image in residence.residence_images.all()],
            'room_info': [{
                'person'    : room.person,
                'max_person': room.max_person,
                'price'     : room.price
            } for room in residence.rooms.all()]
        } for residence in residences]

        return JsonResponse({'residences_list' : residences_list}, status=200)

class ResidenceDetailView(View) :
    def get(self, request, residence_id) :
        try :
            residence = Residence.objects.prefetch_related('rooms__room_images','places','residence_images').get(id = residence_id)
           
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

class RoomDetailView(View) :
    def get(self, request, residence_id, room_id):
        try:            
            room = Room.objects.prefetch_related('room_amenities', 'room_features', 'room_images').get(id=room_id)
                
            result = {
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
                         
            return JsonResponse({'result' : result }, status =200)
        
        except Room.DoesNotExist:
            return JsonResponse({'message' : 'ROOM_NOT_FOUND'}, status = 404)
