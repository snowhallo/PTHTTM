import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        )
        page = await context.new_page()
        await page.goto('https://www.canva.com/design/DAHZ900uO14/I68j5Pu82YYAFAoV2Z-IIQ/view', wait_until='networkidle')
        await page.wait_for_timeout(3000)

        # Find grid view button
        grid_btn = await page.query_selector('button[aria-label*="Grid view"], button[aria-label*="grid"]')
        if not grid_btn:
            # Look through all buttons
            buttons = await page.query_selector_all('button')
            for b in buttons:
                aria = (await b.get_attribute('aria-label')) or ''
                txt = (await b.inner_text()).strip()
                if 'grid' in aria.lower() or 'grid' in txt.lower():
                    grid_btn = b
                    print(f"Found button: aria={aria}, text={txt}")
                    break

        if grid_btn:
            print("Clicking grid button...")
            await grid_btn.click()
            await page.wait_for_timeout(3000)
            # Scroll down slowly to load all 44 slides in grid view
            for step in range(15):
                await page.keyboard.press("PageDown")
                await page.wait_for_timeout(1000)
            
            grid_text = await page.inner_text('body')
            with open('canva_grid_text.txt', 'w', encoding='utf-8') as f:
                f.write(grid_text)
            print(f"Saved canva_grid_text.txt, length: {len(grid_text)}")
        else:
            print("Grid button not found!")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(inspect())

