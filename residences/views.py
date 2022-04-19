from django.http       import JsonResponse
from django.views      import View

from .models import Residence, RegionEnum

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