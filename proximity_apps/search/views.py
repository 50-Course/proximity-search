# Module contains the core algorithm for performing proximity searches
# within a given location


try:
    from typing import Mapping
except ImportError:
    from collections.abc import Mapping

from django.contrib.gis.geos import Point
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Group, Town
from .permissions import HasAPIKeyPermission


@permission_classes([HasAPIKeyPermission])
@api_view(['GET'])
def search_within_radius(request: Request, city: str, **filters: Mapping) -> Response:
    """
    Search for groups within a given radius of a group

    Essentially, it leverages the ORM and the PostGIS extension to find all
    groups within a given radius of a group. 

    Under the hood, it utilizes the geohashing algorithm, 'bounding box' for finding radius
    and the 'great circle' formula for calculating distances between two points on a sphere.

    Groups within a given radius are returned as a JSON response

    Args:

    city (str): The name of the city to search within
    **filters (dict): A Mapping of filters to apply to the search
                       This could be the radius, member_count, is_private, exclude_categories (categories of groups to exclude)
    """

    town = Town.objects.get(name=city)

    # Get the latitude and longitude of the town
    point  = Point(town.location.x, town.location.y)

    # Apply the bounding box algorithm to get the bounding box
    #
    # The bounding box is a square that surrounds the point, and is used to
    # limit the search radius.
    # see: https://en.wikipedia.org/wiki/Minimum_bounding_box
    # see: https://en.wikipedia.org/wiki/Geohash
    # 
    # We want to apply the radius from the filters if present otherwise,
    # we default to 10km
    radius = filters.get('radius', 10)
    bounding_box = point.buffer(radius * 1609.34)  # 1 mile == 1609.34 meters

    groups_queryset = Group.objects.filter(
        location__within=bounding_box,
        member_count__gte=filters.get('member_count', 0),
        is_private=filters.get('is_private', False)
    ).exclude(
        category__in=filters.get('exclude_categories', [
            'business', 'buy/sell/trade'
        ])
    )

    groups_data = [
        {
            'name': group.name,
            'description': group.description,
            'location': group.location,
            'town': group.town,
            'is_private': group.is_private,
            'member_count': group.member_count
        }
        for group in groups_queryset
    ]
    
    return Response(groups_data, status=status.HTTP_200_OK)
