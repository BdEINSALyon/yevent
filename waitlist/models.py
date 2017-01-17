from django.db import models


from invitation.models import Guest


class WaitingList(models.Model):

    class Meta:
        verbose_name = "Liste d'attente"

    name = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    maximum_registration_by_guest = models.IntegerField(default=7)

    def __str__(self):
        return self.name


class WaitingTicket(models.Model):

    class Meta:
        verbose_name = "Ticket d'attente"

    owner = models.ForeignKey(Guest, verbose_name='propriétaire')
    amount = models.IntegerField(default=1, verbose_name='nombre')
    created_at = models.DateTimeField(auto_now_add=True)
    registered_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    phone = models.CharField(default="", blank=True, verbose_name="Téléphone", max_length=25)
    waiting_list = models.ForeignKey(WaitingList)

    def position(self):
        return WaitingTicket.objects.filter(registered_at__lt=self.registered_at, used=False).count() + 1

    def __str__(self):
        return "{} - {} ({} place(s))".format(self.waiting_list, self.owner, self.amount)
