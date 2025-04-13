from rest_framework import serializers
from admin_dashboard.models import ScamPost

class GetAllPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = ScamPost
        fields = '__all__'

class PostScamSerializers(serializers.ModelSerializer):
    class Meta:
        model = ScamPost
        fields = ['name_scam', 'stk_scam', 'sdt_scam', 'noi_dung']
