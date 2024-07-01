from rest_framework import viewsets
from .models import User, Friend
from .serializers import UserSerializer, FriendSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from django.db.models import Q

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

# * Verifies user - If user already exists, it verifies and send user details i.e, with userid 
# * else It creates new user and send newly created user details
# * Verification and also Creation of User - table 'User'
@api_view(['POST'])
def verify_user(request):
    if request.method == 'POST':
        try:
            username = request.data.get('username')
            if not username:
                return Response({"status": 0, "message": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.filter(username=username).first()

            if user:
                # User exists, generate and send token
                user_data = UserSerializer(user).data
                return Response({"status":1, "message": 'user verified', "data": user_data}, status=status.HTTP_200_OK)
            else :
                serializer = UserSerializer(data={'username': username})
                if serializer.is_valid():
                    user = serializer.save()
                    user_data = UserSerializer(user).data
                    return Response({"status":1,"message": "User created", "data": user_data}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"status": 0, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError as e:
            return Response({"status": 0, "message": "Integrity error: likely a unique constraint violation."}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"status": 0, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return Response({"status": 0, "message": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# * Once User is verified with their id, Get all the details
# * List of friends added by user, list of friends that are not added by user, and non friends list
# * Fetching User Details - table 'User', 'Friend'
@api_view(['GET'])
def get_friends(request, id):
    try:
        user = User.objects.get(pk=id)
        user_details = UserSerializer(user).data

        # Friends added by the user
        friends_added_by_user = Friend.objects.filter(user=user).values_list('friend_id', flat=True)

        # Friends added as the user
        friends_added_as_user = Friend.objects.filter(friend=user).values_list('user_id', flat=True)

        # Combine both lists to get all friends
        all_friends_ids = set(friends_added_by_user).union(set(friends_added_as_user))

        # Get all users excluding the current user and friends
        non_friends = User.objects.exclude(pk__in=all_friends_ids).exclude(pk=user.pk)

        # Friends added as user but not added by the user
        friends_not_added_by_user = set(friends_added_as_user) - set(friends_added_by_user)
        friends_not_added_by_user_list = User.objects.filter(pk__in=friends_not_added_by_user)

        # Fetch friend details
        friends_added_by_user_list = User.objects.filter(pk__in=friends_added_by_user)
        friends_added_as_user_list = User.objects.filter(pk__in=friends_added_as_user)

        # Serialize the user lists
        friends_added_by_user_serializer = UserSerializer(friends_added_by_user_list, many=True)
        friends_added_as_user_serializer = UserSerializer(friends_added_as_user_list, many=True)
        friends_not_added_by_user_serializer = UserSerializer(friends_not_added_by_user_list, many=True)
        non_friends_serializer = UserSerializer(non_friends, many=True)

        return Response({
            "status": 1,
            "data": {
                "user_details": user_details,
                "friends_added_by_user": friends_added_by_user_serializer.data,
                "friends_added_as_user": friends_added_as_user_serializer.data,
                "friends_not_added_by_user": friends_not_added_by_user_serializer.data,
                "non_friends": non_friends_serializer.data
            }
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"status": 0, "message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(str(e))
        return Response({"status": 0, "message": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# * Add Friends
# * When user addes friends -> insertion to "friend" table
# * Establishing Friend connection by adding record - table 'Friend'
@api_view(['POST'])
def add_friend(request):
    if request.method == 'POST':
        try:
            userid = int(request.data.get('userid'))
            friendid = int(request.data.get('friendid'))
            if not userid:
                return Response({"status":0,"message": "userid is required."}, status=status.HTTP_400_BAD_REQUEST)
            if not friendid:
                return Response({"status":0,"message": "friendid is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.filter(userid=userid).first()
            friend = User.objects.filter(userid=friendid).first()
            if not user: 
                return Response({"status":0, "message": "Userid does not exists."}, status=status.HTTP_200_OK)
            if not friend: 
                return Response({"status":0, "message": "Friendid does not exists."}, status=status.HTTP_200_OK)
            
            checkforduplicate = Friend.objects.filter(user=userid, friend=friendid).first()

            if checkforduplicate:
                return Response({"status":0, "message": "Record already exists."}, status=status.HTTP_200_OK)
            
            serializer = FriendSerializer(data={'user': userid, 'friend': friendid});

            if serializer.is_valid():
                friend_insert = serializer.save()
                friend_data = FriendSerializer(friend_insert).data
                return Response({"status": 1, "message": "Added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": 0, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError as e:
            return Response({"status": 0,"message": "Integrity error: likely a unique constraint violation."}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"status": 0,"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return Response({"status": 0,"message": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# * Edit Username
# * Editing username by userid - table 'User'
@api_view(['PATCH'])
def edit_username(request):
    if request.method == 'PATCH':
        try:
            userid = request.data.get('userid')
            username = request.data.get('username')
            
            if not userid:
                return Response({"status": 0, "message": "userid is required."}, status=status.HTTP_400_BAD_REQUEST)
            if not username:
                return Response({"status": 0, "message": "username is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.filter(pk=userid).first()
            if not user:
                return Response({"status": 0, "message": "User details do not exist."}, status=status.HTTP_404_NOT_FOUND)
            
            # Check for duplicate username
            if User.objects.filter(username=username).exclude(pk=userid).exists():
                return Response({"status": 0, "message": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Update the user's username
            user.username = username
            user.save()
            
            return Response({"status": 1, "message": "Updated successfully"}, status=status.HTTP_200_OK)

        except IntegrityError as e:
            return Response({"status": 0, "message": "Integrity error: likely a unique constraint violation."}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"status": 0, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return Response({"status": 0, "message": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ! DELETE RECORD is not good practice, added this api for assessment requirements only !
# * Remove Friend
# * Removing friends from user list
# * Deleteing record in - table 'Friend'
@api_view(['DELETE'])
def remove_friend(request, id, friendid):
    if request.method == 'DELETE':
        try:
            friend = Friend.objects.filter(user=id, friend=friendid).first()
            
            if not friend:
                return Response({"status": 0, "message": "friend does not exists."}, status=status.HTTP_400_BAD_REQUEST)
            
            friend.delete()
            
            return Response({"status": 1, "message": "Removed successfully."}, status=status.HTTP_200_OK)

        except IntegrityError as e:
            return Response({"status": 0, "message": "Integrity error: likely a unique constraint violation."}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"status": 0, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return Response({"status": 0, "message": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ! DELETE RECORD is not good practice, added this api for assessment requirements only !
# * Deleting User
# * Removing User - also removing all the connections in friends list.
# * Deleteing record in - table 'User'
@api_view(['DELETE'])
def delete_user(request, id):
    if request.method == 'DELETE':
        try:
            user = User.objects.filter(pk=id).first()
            
            if not user:
                return Response({"status": 0, "message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            user.delete()
            return Response({"status": 1, "message": "User and all related friends records deleted successfully."}, status=status.HTTP_200_OK)

        except IntegrityError as e:
            return Response({"status": 0, "message": "Integrity error: likely a unique constraint violation."}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"status": 0, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return Response({"status": 0, "message": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)