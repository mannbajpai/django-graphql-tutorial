import graphene
from graphene_django import DjangoObjectType
from app.models import Contact
from graphql_auth.schema import UserQuery
from graphql_auth import mutations


class ContactType(DjangoObjectType):

    class Meta:
        model = Contact
        field = ("id", "name", "phone_number")


class Query(UserQuery,graphene.ObjectType):

    list_contact = graphene.List(ContactType)
    read_contact = graphene.Field(ContactType, id=graphene.Int())

    def resolve_list_contact(root, info):

        return Contact.objects.all()

    def resolve_read_contact(root, info, id):

        return Contact.objects.get(id=id)

    def resolve_read_contact_with_name(root, info, name):

        return Contact.objects.get(name=name)


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()

class ContactMutation(graphene.Mutation):
    class Arguments:

        id = graphene.ID()
        name = graphene.String()
        phone_number = graphene.String()

    contact = graphene.Field(ContactType)

    @classmethod
    def mutate(cls, root, info, name, phone_number, id):

        if id:
            # Update an existing Contact with id
            get_contact = Contact.objects.get(id=id)
            get_contact.name = name
            get_contact.phone_number = phone_number
            get_contact.save()

        else:
            # Create a new Contact
            contact = Contact(name=name, phone_number=phone_number)
            contact.save()

        return ContactMutation(contact=get_contact)


class ContactDelete(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    contact = graphene.Field(ContactType)

    @classmethod
    def mutate(cls, root, info, id):

        contact = Contact.objects.get(id=id)
        contact.delete()


class Mutation(AuthMutation,graphene.ObjectType):

    create_contact = ContactMutation.Field()
    update_contact = ContactMutation.Field()
    delete_contact = ContactDelete.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
