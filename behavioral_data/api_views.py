from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tasks.metric_extraction import extract_session_metrics

class MetricExtractionAPIView(APIView):
    def post(self, request):
        session_id = request.data.get('session_id')
        if not session_id:
            return Response({"error": "Missing session_id."}, status=status.HTTP_400_BAD_REQUEST)
        result = extract_session_metrics.delay(session_id)
        return Response({"task_id": result.id, "status": "started"}, status=status.HTTP_202_ACCEPTED)
