from sqlalchemy import UUID, Column, DateTime, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.models import Base
from app.utils import enums

# TODO: cascade delete


# Bridge/Association table for Many to Many relationship
role_permissions_association = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True),
)

# class RolePermissionsEntity(Base):
#     __tablename__ = 'role_permissions'
#     role_id = Column(UUID, ForeignKey("roles.id"), primary_key=True)
# permission_id = Column(
#     UUID,
#     ForeignKey("permissions.id"),
#     primary_key=True
# )


class RoleEntity(Base):
    __tablename__ = "roles"
    id = Column(UUID, primary_key=True)
    role = Column(Enum(enums.Roles), nullable=False, unique=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    permissions = relationship(
        "PermissionEntity", secondary=role_permissions_association
    )


class PermissionEntity(Base):
    __tablename__ = "permissions"
    id = Column(UUID, primary_key=True)
    permission = Column(
        Enum(
            enums.Permissions, values_callable=lambda e: [p.value for p in e]
        ),
        nullable=False,
        unique=True,
    )  # lambda to store enum values instead of names in db
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )


# Not using bridge tabels here since
# User will only have 1 role (1 x N relationship)
# class UserRolesEntity(Base):
#     __tablename__ = 'user_roles'
#     # only user_id as primary_key so user can have only 1 role
#     user_id = Column(UUID, ForeignKey("users.id"), primary_key=True)
#     role_id = Column(UUID, ForeignKey("roles.id"))
