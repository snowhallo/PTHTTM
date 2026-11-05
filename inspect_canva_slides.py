import asyncio
import sys
import json
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        )
        page = await context.new_page()
        url = 'https://www.canva.com/design/DAHZ900uO14/I68j5Pu82YYAFAoV2Z-IIQ/view'
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(3000)

        # Get initial body text
        body_text = await page.inner_text('body')
        with open('canva_view_body.txt', 'w', encoding='utf-8') as f:
            f.write(body_text)
        print(f"Body text saved ({len(body_text)} chars).")

        # Let's inspect elements on page
        # In Canva presentation view, often there's a next page button or arrow right key
        # Let's see how many slides can be navigated
        # Check title and buttons
        buttons = await page.query_selector_all('button')
        print(f"Found {len(buttons)} buttons.")
        btn_info = []
        for i, b in enumerate(buttons):
            t = (await b.inner_text()).strip()
            aria = await b.get_attribute('aria-label')
            btn_info.append(f"Button {i}: text='{t}', aria='{aria}'")
        with open('canva_buttons.txt', 'w', encoding='utf-8') as f:
            f.write("\n".join(btn_info))

        # Let's see if we can iterate through slides by pressing 'ArrowRight' or finding next button
        slides_text = []
        out_dir = Path("canva_slides")
        out_dir.mkdir(exist_ok=True)

        # Iterate through 44 slides
        for slide_num in range(1, 46):
            await page.wait_for_timeout(1000)
            # Take screenshot of slide
            screenshot_path = out_dir / f"slide_{slide_num:02d}.png"
            await page.screenshot(path=str(screenshot_path))
            
            # Extract text on page
            cur_text = await page.inner_text('body')
            slides_text.append({
                "slide": slide_num,
                "text": cur_text
            })
            print(f"Captured slide {slide_num}")
            
            # Press ArrowRight to go to next slide
            await page.keyboard.press("ArrowRight")
            await page.wait_for_timeout(1000)

        with open('canva_slides_text.json', 'w', encoding='utf-8') as f:
            json.dump(slides_text, f, ensure_ascii=False, indent=2)
        print("Done capturing slides!")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())

