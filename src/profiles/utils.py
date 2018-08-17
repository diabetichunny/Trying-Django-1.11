import uuid


def code_generator(instance):
    code = str(uuid.uuid4())

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(activation_key=code).exists()

    if qs_exists:
        code = code_generator(instance)

    return code

