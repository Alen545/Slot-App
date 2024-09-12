from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User, TimeSlot
from .serializers import TimeSlotSerializer, UserSerializer
from datetime import timedelta

class RegisterTimeSlot(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        serializer = TimeSlotSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            start_time = serializer.validated_data['start_time']
            end_time = serializer.validated_data['end_time']

            overlapping_slots = TimeSlot.objects.filter(
                user=user,
                date=serializer.validated_data['date'],
                start_time__lt=end_time,
                end_time__gt=start_time
            )

            if overlapping_slots.exists():
                return Response(
                    {"error": "Time slot overlaps with an existing slot."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetAvailableSlots(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        candidate_id = request.GET.get('candidate_id')
        interviewer_id = request.GET.get('interviewer_id')
        candidate = get_object_or_404(User, id=candidate_id, role='candidate')
        interviewer = get_object_or_404(User, id=interviewer_id, role='interviewer')

        candidate_slots = TimeSlot.objects.filter(user=candidate)
        interviewer_slots = TimeSlot.objects.filter(user=interviewer)
        available_slots = []

        for cs in candidate_slots:
            for islot in interviewer_slots:
                if cs.date == islot.date:  
                    start_time = max(cs.start_time, islot.start_time)
                    end_time = min(cs.end_time, islot.end_time)

                    while start_time < end_time:
                        slot_end = start_time + timedelta(hours=1)
                        if slot_end <= end_time:
                            available_slots.append({
                                "date": cs.date,
                                "start_time": start_time,
                                "end_time": slot_end
                            })
                        start_time = slot_end
        if available_slots:
            slots_str = "\n".join([f"{slot[0]} to {slot[1]}" for slot in available_slots])
            subject = 'Available Interview Slots'
            message = f"Dear {candidate.username} and {interviewer.username},\n\nHere are the available slots:\n\n{slots_str}\n\nPlease confirm your preferred time slot."
            recipient_list = [candidate.email, interviewer.email]

            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

        return Response(available_slots, status=status.HTTP_200_OK)
