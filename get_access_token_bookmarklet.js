// this bookmarklet was generated using ChatGPT, it will extract your
// accessToken from the page, so you can copy and paste it into .env
javascript: (function () { const data = window.__NEXT_DATA__.props.pageProps; if (data && data.accessToken) { const tempInput = document.createElement('input'); tempInput.style = 'position: absolute; left: -1000px; top: -1000px'; tempInput.value = data.accessToken; document.body.appendChild(tempInput); tempInput.select(); document.execCommand('copy'); document.body.removeChild(tempInput); alert('Access token copied to clipboard!'); } })();
