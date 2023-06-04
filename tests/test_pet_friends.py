from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, empty_email, empty_password
import os

pf = PetFriends()

# тесты из модуля
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_post_new_pet_with_photo(name='Мартин', animal_type='Собака', age='3', pet_photo='image\IMG_2733.JPG'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_delete_pet():
    _, auth_key = pf.get_api_key(valid_email,valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Мартин", "собака", "3", 'image\IMG_2733.JPG')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        assert status == 200
        assert pet_id not in my_pets.values()

def test_update_self_pet_info(name='Мерлин', animal_type='Пес', age=7):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("У вас еще нет питомцев.")

# тесты для задания 24.7.2
def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    # тест с неверными почтой и паролем
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    # тест с неверными почтой и паролем
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    # тест с неверными почтой и паролем
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_for_empty_email(email=empty_email, password=valid_password):
    # тест с пустыми полями почты и пароля
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_for_empty_password(email=valid_email, password=empty_password):
    # тест с пустыми полями почты и пароля
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_for_empty_user(email=empty_email, password=empty_password):
    # тест с пустыми полями почты и пароля
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_add_new_pet_without_photo(name='Мартин', animal_type='Собака', age=3):
    # тест на добавление нового питомца без фото
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_add_photo_to_pet(pet_photo='image\IMG_2733.JPG'):
    # тест на добавление фото к существующему питомцу
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info_add_photo(auth_key, my_pets['pets'][-1]['id'], pet_photo)
        assert status == 200
    else:
        raise Exception("У вас еще нет питомцев.")

def test_add_text_to_pet(pet_photo='image\IMG_2732.txt'):
    # тест на вставку вместо фото текстовый файл
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info_add_photo(auth_key, my_pets['pets'][-1]['id'], pet_photo)
        assert status == 500
    else:
        raise Exception("У вас еще нет питомцев.")

def test_add_new_nameless_pet_without_photo(name='', animal_type='', age=3):
    # тест на добавление нового питомца без фото c пустыми текстовыми полями
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    if name and animal_type != None:
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("У вас пустые поля имя и тип животного")