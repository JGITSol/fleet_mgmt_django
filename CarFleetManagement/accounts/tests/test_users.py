import pytest

# Models imported inside test function

@pytest.mark.django_db
def test_create_all_roles():
    from CarFleetManagement.accounts.models import CustomUser, UserRole
    roles = [UserRole.ADMIN, UserRole.MANAGER, UserRole.COORDINATOR, UserRole.DRIVER, UserRole.TESTUSER]
    role_objs = {}
    for role_name in roles:
        role_objs[role_name] = UserRole.objects.create(name=role_name)
        assert role_objs[role_name].name == role_name

    users = {}
    for role_name in roles:
        user = CustomUser.objects.create_user(
            username=f'{role_name}_user',
            email=f'{role_name}@example.com',
            password='testpassword',
            role=role_objs[role_name],
            phone_number='1234567890',
            emergency_contact='Emergency Contact'
        )
        users[role_name] = user
        assert user.role.name == role_name

    # Check helper properties
    assert users[UserRole.ADMIN].is_admin
    assert users[UserRole.MANAGER].is_manager
    assert users[UserRole.COORDINATOR].is_coordinator
    assert users[UserRole.DRIVER].is_driver
    assert users[UserRole.TESTUSER].is_testuser
