from django.db import models

class Thread(models.Model):
    first_person = models.ForeignKey('api.User', on_delete=models.CASCADE, related_name='first_person')
    second_person = models.ForeignKey('api.User', on_delete=models.CASCADE, related_name='second_person')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('first_person', 'second_person')

    def __str__(self):
        return f'{self.first_person} - {self.second_person}'
    
    def get_last_message(self):
        return self.message_set.order_by('-created_at').first()
    

class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sender = models.ForeignKey('api.User', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.thread} - {self.sender} - {self.text}'
