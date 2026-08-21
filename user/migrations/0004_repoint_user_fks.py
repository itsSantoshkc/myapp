from django.db import migrations

FKS = [
    ("cart_cart", "cart_cart_user_id_9b4220b9_fk_auth_user_id"),
    ("user_address", "user_address_user_id_64deb2c7_fk_auth_user_id"),
    ("order_order", "order_order_user_id_7cf9bc2b_fk_auth_user_id"),
]


def repoint(apps, schema_editor):
    for table, old_constraint in FKS:
        schema_editor.execute(
            f"ALTER TABLE {table} DROP CONSTRAINT IF EXISTS {old_constraint}"
        )
        schema_editor.execute(
            f"ALTER TABLE {table} ADD CONSTRAINT {table}_user_id_fk "
            f"FOREIGN KEY (user_id) REFERENCES user_user (id)"
        )


def revert(apps, schema_editor):
    for table, old_constraint in FKS:
        schema_editor.execute(
            f"ALTER TABLE {table} DROP CONSTRAINT IF EXISTS {table}_user_id_fk"
        )
        schema_editor.execute(
            f"ALTER TABLE {table} ADD CONSTRAINT {old_constraint} "
            f"FOREIGN KEY (user_id) REFERENCES auth_user (id)"
        )


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0002_alter_cartitem_unique_together"),
        ("order", "0002_alter_order_transaction_uuid"),
        ("user", "0003_alter_address_id_alter_address_user_alter_user_id"),
    ]

    operations = [
        migrations.RunPython(repoint, revert),
    ]
