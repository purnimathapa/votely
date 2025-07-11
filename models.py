from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Election(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_elections')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.title

    @property
    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    @property
    def status(self):
        now = timezone.now()
        if now < self.start_date:
            return 'Upcoming'
        elif now <= self.end_date:
            return 'Active'
        return 'Closed'

class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates')
    name = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='candidates/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.election.title}"

    @property
    def vote_count(self):
        return self.votes.count()

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='votes')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['voter', 'election']
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.voter.username} voted for {self.candidate.name} in {self.election.title}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.election_id or not self.election:
            raise ValidationError("Vote must be associated with an election.")
        # Check if the election is active
        if not self.election.is_active:
            raise ValidationError("This election is not active.")
        # Check if the voter has already voted in this election
        if Vote.objects.filter(voter=self.voter, election=self.election).exists():
            raise ValidationError("You have already voted in this election.")

    def save(self, *args, **kwargs):
        if not self.election_id or not self.election:
            raise ValueError("Vote must be associated with an election.")
        # Check if the election is active
        if not self.election.is_active:
            raise ValueError("This election is not active.")
        # Check if the voter has already voted in this election
        if Vote.objects.filter(voter=self.voter, election=self.election).exists():
            raise ValueError("You have already voted in this election.")
        super().save(*args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            self.save()
            return True
        else:
            print('DEBUG: form.errors =', form.errors)
            return False 