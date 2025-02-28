addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url);
  const targetUrl = `https://bots.qq.com${url.pathname}${url.search}`;

  try {
      const response = await fetch(targetUrl, {
          method: request.method,
          headers: request.headers,
          body: request.body
      });

      return new Response(response.body, {
          status: response.status,
          statusText: response.statusText,
          headers: response.headers
      });
  } catch (error) {
      return new Response(`Error: ${error.message}`, { status: 500 });
  }
}
