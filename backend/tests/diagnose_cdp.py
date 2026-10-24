import asyncio
import json
import urllib.request
import websockets

async def diagnose_route(target_url):
    print(f"\n==========================================")
    print(f"DIAGNOSING ROUTE: {target_url}")
    print(f"==========================================")

    # 1. Get CDP target
    pages = json.loads(urllib.request.urlopen("http://127.0.0.1:9222/json").read().decode("utf-8"))
    page = next((p for p in pages if "5173" in p.get("url", "") or p.get("type") == "page"), None)
    if not page:
        print("No active page found in Chrome CDP.")
        return

    ws_url = page["webSocketDebuggerUrl"]
    print(f"Connecting to CDP: {ws_url}")

    async with websockets.connect(ws_url) as ws:
        msg_id = 1

        async def send_cmd(method, params=None):
            nonlocal msg_id
            cmd = {"id": msg_id, "method": method, "params": params or {}}
            msg_id += 1
            await ws.send(json.dumps(cmd))
            return cmd["id"]

        # Enable domains
        await send_cmd("Page.enable")
        await send_cmd("Runtime.enable")
        await send_cmd("Log.enable")
        await send_cmd("Console.enable")

        console_logs = []
        runtime_exceptions = []

        # Navigate to target_url
        nav_id = await send_cmd("Page.navigate", {"url": target_url})
        print(f"Sent navigation to {target_url} (cmd {nav_id})")

        # Collect events for 3.5 seconds
        start_time = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start_time < 3.5:
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=0.5)
                event = json.loads(raw)
                method = event.get("method")
                params = event.get("params", {})

                if method == "Runtime.exceptionThrown":
                    runtime_exceptions.append(params)
                elif method == "Runtime.consoleAPICalled":
                    console_logs.append(params)
                elif method == "Log.entryAdded":
                    console_logs.append(params.get("entry", {}))
            except asyncio.TimeoutError:
                pass

        # Evaluate document.title, location.href, and #root HTML
        eval_id = await send_cmd("Runtime.evaluate", {
            "expression": "JSON.stringify({ href: window.location.href, title: document.title, rootHTML: document.getElementById('root')?.innerHTML || '', rootText: document.getElementById('root')?.innerText || '', token: localStorage.getItem('masteryloop_token') })",
            "returnByValue": True
        })

        eval_result = None
        while asyncio.get_event_loop().time() - start_time < 6.0:
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=0.5)
                res = json.loads(raw)
                if res.get("id") == eval_id:
                    eval_result = json.loads(res.get("result", {}).get("result", {}).get("value", "{}"))
                    break
            except asyncio.TimeoutError:
                pass

        print(f"\n--- Result for {target_url} ---")
        if eval_result:
            print(f"Final URL: {eval_result.get('href')}")
            print(f"Page Title: {eval_result.get('title')}")
            print(f"Stored Token: {eval_result.get('token')[:20] if eval_result.get('token') else 'None'}")
            print(f"Root Inner Text Length: {len(eval_result.get('rootText', ''))}")
            print(f"Root Inner Text Sample: {eval_result.get('rootText', '')[:200]}")
            print(f"Root Inner HTML Sample: {eval_result.get('rootHTML', '')[:200]}")
        else:
            print("Failed to get evaluate result.")

        print(f"\n--- Runtime Exceptions ({len(runtime_exceptions)}) ---")
        for ex in runtime_exceptions:
            details = ex.get("exceptionDetails", {})
            print(f"EXCEPTION: {details.get('text')} | {details.get('exception', {}).get('description')}")

        print(f"\n--- Console Messages ({len(console_logs)}) ---")
        for cl in console_logs:
            m_type = cl.get("type") or cl.get("level")
            args = cl.get("args", [])
            txt = cl.get("text") or " ".join([a.get("value", a.get("description", "")) for a in args])
            print(f"[{m_type}] {txt}")

async def main():
    await diagnose_route("http://127.0.0.1:5173/")
    await diagnose_route("http://127.0.0.1:5173/login")
    await diagnose_route("http://127.0.0.1:5173/dashboard")

if __name__ == "__main__":
    asyncio.run(main())
