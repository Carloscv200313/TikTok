from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import asyncio

async def fetch_user_followers_manual(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Ejecuta en modo no-headless para evitar bloqueos
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(url, timeout=60000)  # Aumenta el timeout para la carga de la página
            await page.wait_for_load_state("networkidle")  # Espera a que la página se cargue completamente

            # Trata con diferentes posibles selectores que podrían contener el número de seguidores
            follower_count_selectors = [
                "strong[data-e2e='followers-count']",  # Selector original
                "h2:has-text('Seguidores') + strong",  # Alternativa con estructura común
                "[class*='follower'] strong"           # Selector general basado en nombre de clase
            ]

            followers = None
            for selector in follower_count_selectors:
                try:
                    followers = await page.inner_text(selector)
                    if followers:
                        break
                except PlaywrightTimeoutError:
                    continue

            if followers:
                print(f"El usuario tiene {followers} seguidores.")
            else:
                print("No se pudo encontrar el número de seguidores con los selectores disponibles.")

        except PlaywrightTimeoutError:
            print("Error al obtener el número de seguidores: La página no cargó correctamente o el selector es incorrecto.")
        finally:
            await browser.close()

user_url = "https://www.tiktok.com/@ofertas_rapidas"
asyncio.run(fetch_user_followers_manual(user_url))
