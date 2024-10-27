from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField(default=0)
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    phone_number = models.CharField(max_length=50)
    is_staff = models.IntegerField(default=0)
    is_active = models.IntegerField(default=1)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'





class Adrese(models.Model):
    address_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('Clienti', models.CASCADE)
    nume_adresa = models.CharField(max_length=50, default='Home')
    tara = models.CharField(max_length=50, default='Romania')
    judet = models.CharField(max_length=50)
    localitate = models.CharField(max_length=50)
    strada = models.CharField(max_length=50)
    numar = models.CharField(max_length=50)
    bloc = models.CharField(max_length=50)
    scara = models.CharField(max_length=50)
    etaj = models.PositiveIntegerField()
    apartament = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'adrese'
        constraints = [
            models.UniqueConstraint(fields=['nume_adresa', 'client_id'], name='unique_numeadresa_clientid')
        ]


class AdreseComenzi(models.Model):
    comanda_id = models.OneToOneField('Comenzi', models.CASCADE, primary_key=True)
    tara = models.CharField(max_length=50)
    judet = models.CharField(max_length=50)
    localitate = models.CharField(max_length=50)
    strada = models.CharField(max_length=50)
    bloc = models.CharField(max_length=50)
    scara = models.CharField(max_length=50)
    etaj = models.PositiveIntegerField()
    apartament = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'adrese_comenzi'


class AgentiiLivrare(models.Model):
    agentie_id = models.AutoField(primary_key=True)
    nume_agentie_livrare = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'agentii_livrare'

class CarduriClienti(models.Model):
    card_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('Clienti', models.CASCADE)
    denumire = models.CharField(max_length=50)
    numar_card = models.CharField(max_length=50)
    nume_proprietar = models.CharField(max_length=50)
    data_expirare = models.DateField()
    tip_card = models.CharField(max_length=50)
    banca = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'carduri_clienti'
        constraints = [
            models.UniqueConstraint(fields=['card_id', 'client_id'], name='unique_cardid_clientid')
        ]


class Categorie(models.Model):
    categorie_id = models.AutoField(primary_key=True)
    nume_categorie = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'categorie'

    def __str__(self):
        return self.nume_categorie


class Clienti(models.Model):
    client_id = models.AutoField(primary_key=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True, default="NULL")
    nume = models.CharField(max_length=50)
    prenume = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    numar_telefon = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'clienti'

class Colors(models.Model):
    color_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 50)

    class Meta:
        managed = False
        db_table = 'colors'


class Comenzi(models.Model):
    comanda_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Clienti, models.CASCADE)
    livrare_agentie = models.ForeignKey(AgentiiLivrare, models.CASCADE)
    data_plasare = models.DateField()
    status = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'comenzi'


class Cosuri(models.Model):
    cos_id = models.CharField(max_length=50, primary_key=True)
    client = models.ForeignKey(Clienti, on_delete=models.CASCADE)
    produs = models.ForeignKey('Produse', on_delete=models.CASCADE)
    cantitate = models.IntegerField()
    data_adaugare = models.DateField()

    class Meta:
        managed = False
        db_table = 'cosuri'  # Optional, in case you want to control the table name

class Domains(models.Model):
    domain_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 50)

    class Meta:
        managed = False
        db_table = 'domains'

class Favorites(models.Model):
    favorite = models.CharField(max_length = 50, primary_key = True)
    client = models.ForeignKey(Clienti, on_delete=models.CASCADE)
    product = models.ForeignKey('Produse', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'favorites'

class Furnizori(models.Model):
    furnizor_id = models.AutoField(primary_key=True)
    nume_furnizor = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'furnizori'

    def __str__(self):
        return self.nume_furnizor


class NewsletterEmails(models.Model):
    email_id = models.AutoField(primary_key = True)
    client = models.ForeignKey(Clienti, on_delete = models.CASCADE)
    email = models.CharField(max_length = 255)

    class Meta:
        managed = False
        db_table = 'newsletter_emails'

class PageType(models.Model):
    pg_type_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 50)

    class Meta:
        managed = False
        db_table = 'page_types'


class Plati(models.Model):
    comanda = models.OneToOneField(Comenzi, models.CASCADE, primary_key=True)
    client = models.ForeignKey(Clienti, models.CASCADE)
    card = models.ForeignKey(CarduriClienti, models.CASCADE)
    suma = models.FloatField()
    metoda_plata = models.CharField(max_length=50)
    data_plata = models.DateField()

    class Meta:
        managed = False
        db_table = 'plati'


class Produse(models.Model):
    produs_id = models.AutoField(primary_key=True)
    categorie = models.ForeignKey(Categorie, models.CASCADE, default=1)
    furnizor = models.ForeignKey(Furnizori, models.CASCADE, default=1)
    nume = models.CharField(max_length=255)
    stoc = models.SmallIntegerField()
    pret_unitar = models.FloatField()

    class Meta:
        managed = False
        db_table = 'produse'


class ProduseComenzi(models.Model):
    comanda = models.OneToOneField(Comenzi, models.CASCADE, primary_key=True)
    produs = models.ForeignKey(Produse, models.CASCADE)
    cantitate_comanda = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'produse_comenzi'


class ProprietatiProduse(models.Model):
    produs = models.OneToOneField(Produse, models.CASCADE, primary_key=True)
    Category = models.CharField(max_length=50)
    domeniu = models.CharField(max_length=50)
    Dimensiune = models.CharField(max_length=50)
    Culori = models.CharField(max_length=50)
    Foaie = models.CharField(max_length=50)
    Pagina = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'proprietati_produse'

class ProduseImagini(models.Model):
    produs = models.OneToOneField(Produse, models.CASCADE, primary_key=True)
    imagine_catalog = models.BinaryField()

    class Meta:
        managed = False
        db_table = 'produse_imagini'


class Reviews(models.Model):
    review_id = models.AutoField(primary_key = True)
    client_id = models.ForeignKey(Clienti, on_delete = models.CASCADE)
    product_id = models.ForeignKey(Produse, on_delete = models.CASCADE)
    body = models.TextField()
    nr_stars = models.PositiveSmallIntegerField(default = 1,
                                                validators = [
                                                    MinValueValidator(1),
                                                    MaxValueValidator(5)
    ])
    post_date = models.DateField(auto_now = True)

    class Meta:
        managed = False
        db_table = 'reviews'


class Sizes(models.Model):
    size_id = models.AutoField(primary_key=True)
    size_name = models.CharField(max_length = 50)

    class Meta:
        managed = False
        db_table = 'sizes'


