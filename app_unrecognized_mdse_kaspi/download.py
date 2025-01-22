import requests


def main():
    # 1) Настраиваем сессию
    session = requests.Session()

    # Общие заголовки, похожие на браузерные
    common_headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/132.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/avif,image/webp,image/apng,*/*;"
            "q=0.8,application/signed-exchange;v=b3;q=0.7"
        ),
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
    }

    # 2) Логин на idmc.shop.kaspi.kz
    login_url = "https://idmc.shop.kaspi.kz/api/p/login"
    login_payload = {
        "_u": "program@sck-1.kz",  # <-- Ваш логин
        "_p": "oyB9beYr4O",  # <-- Ваш пароль
    }
    # Заголовки для логина (JSON)
    login_headers = {
        **common_headers,
        "Content-Type": "application/json",
        "Referer": "https://idmc.shop.kaspi.kz/login",
        "Origin": "https://idmc.shop.kaspi.kz",
    }

    print("=== Шаг 1: Логин через /api/p/login ===")
    resp_login = session.post(
        login_url, json=login_payload, headers=login_headers, allow_redirects=False
    )
    print("Логин:", resp_login.status_code, resp_login.reason)
    if resp_login.status_code != 200:
        print("Не удалось залогиниться (ожидали 200).")
        return

    # Проверим, какие куки теперь есть для idmc.shop.kaspi.kz
    # print("Cookies (idmc.shop.kaspi.kz):", session.cookies.get_dict(domain="idmc.shop.kaspi.kz"))

    # 3) GET /?continue => 302 => kaspi.kz/mc/
    print("=== Шаг 2: /?continue ===")
    step2_url = "https://idmc.shop.kaspi.kz/?continue"
    step2_headers = {**common_headers, "Referer": "https://idmc.shop.kaspi.kz/login"}
    resp_continue = session.get(step2_url, headers=step2_headers, allow_redirects=True)
    print("Шаг 2 ответ:", resp_continue.status_code, resp_continue.url)
    # Обычно здесь в итоге r.url = "https://kaspi.kz/mc/" или что-то похожее
    # print("Redirect history:", [r.url for r in resp_continue.history])

    # 4) Попробуем сходить на https://mc.shop.kaspi.kz/oauth2/authorization/1
    #    Это инициирует OAuth (PKCE). Если вы уже авторизованы на idmc.shop.kaspi.kz,
    #    возможно сервер пройдёт всю цепочку: idmc.shop.kaspi.kz/oauth2/authorize => code => mc-sid
    print("=== Шаг 3: GET /oauth2/authorization/1 на mc.shop.kaspi.kz ===")
    oauth_url = "https://mc.shop.kaspi.kz/oauth2/authorization/1"
    oauth_headers = {
        **common_headers,
        "Referer": "https://kaspi.kz/",  # судя по логам, часто реферер - https://kaspi.kz/
    }
    resp_oauth = session.get(oauth_url, headers=oauth_headers, allow_redirects=True)
    print("Шаг 3 ответ:", resp_oauth.status_code, resp_oauth.url)
    print("Redirect history:", [r.url for r in resp_oauth.history])

    # Проверим, появилась ли кука mc-sid для mc.shop.kaspi.kz
    mc_cookies = session.cookies.get_dict(domain="mc.shop.kaspi.kz")
    print("Cookies для mc.shop.kaspi.kz:", mc_cookies)
    if "mc-sid" not in mc_cookies:
        print("Не появился mc-sid => Скорее всего, не завершена OAuth-авторизация.")
        print("Сервер, вероятно, перекинул нас на форму логина (или 401).")
        return

    print("=== Похоже, мы авторизованы на mc.shop.kaspi.kz! ===")

    # 5) Пробуем скачать файл
    download_url = "https://mc.shop.kaspi.kz/content/pending/mc/product/BUGA/download?approvalStatus=CHECK"
    download_headers = {
        **common_headers,
        # В логах видно, что реферер = "https://kaspi.kz/" или иногда "https://mc.shop.kaspi.kz/..."
        "Referer": "https://kaspi.kz/",
    }
    print("=== Шаг 4: Скачиваем файл ===")
    resp_file = session.get(download_url, headers=download_headers, stream=True)
    print("Download status:", resp_file.status_code, resp_file.reason)

    if resp_file.status_code == 200:
        with open("pending_products.xlsx", "wb") as f:
            for chunk in resp_file.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print("Файл успешно скачан!")
    else:
        print("Не удалось скачать файл. Код:", resp_file.status_code)


if __name__ == "__main__":
    main()
