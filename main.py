import requests
import vk_api
import io
import os


def vk_auth(login, password, api = None):
    vk_session = vk_api.VkApi(login, password)
    vk_session.auth()

    if api:
        return vk_session.get_api()
    else:
        return vk_session


def download_file(url, path):
    if not os.path.isdir(path):
        os.mkdir(path)
        
    response = requests.get(url, stream=True)
    file_name = url.split('/')[-1]
    file_path = f'{path}/{file_name}'

    with open(file_path, 'wb') as jf:
        jf.write(response.content)
    
    return file_path


def upload_voice(account, url):
    audio_file = download_file(url, 'messages')
    upload = vk_api.upload.VkUpload(account)
    vk_response = upload.audio_message(audio_file)
    audio_message = vk_response.get('audio_message')

    return audio_message


def voice_loop(account):
    while True:
        try:
            url = input('\nGet URL (.ogg): ')
            voice = upload_voice(account, url)
        except KeyboardInterrupt as e:
            print('\n')
            break
        except Exception as e:
            print(e)
        else:
            print(f'vk.com/doc{voice.get("owner_id")}_{voice.get("id")}')


def main():
    login = input('Login: ')
    password = input('Password: ')

    try:
        account = vk_auth(login, password, True)
    except Exception as e:
        print(e)
    else:
        voice_loop(account)


if __name__ == '__main__':
    main()