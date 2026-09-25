from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from ai.brain import LinaBrain


brain = LinaBrain()


HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Lina AI Live</title>

    <style>
        body {
            margin: 0;
            padding: 30px 20px;
            background: #17151f;
            color: white;
            font-family: Arial, sans-serif;
        }

        .container {
            max-width: 600px;
            margin: auto;
        }

        .card {
            background: #242130;
            padding: 25px;
            border-radius: 20px;
        }

        textarea {
            width: 100%;
            min-height: 120px;
            box-sizing: border-box;
            padding: 15px;
            border-radius: 12px;
            border: none;
            margin-top: 15px;
            font-size: 16px;
        }

        button {
            margin-top: 12px;
            padding: 12px 20px;
            border: none;
            border-radius: 12px;
            background: #ff4fa3;
            color: white;
            font-weight: bold;
            font-size: 16px;
        }

        .info {
            opacity: 0.7;
        }
    </style>
</head>

<body>

<div class="container">

    <div class="card">

        <h1>👩 Lina AI Live</h1>

        <p class="info">
            Lina AI yayıncı prototipi
        </p>

        <form method="POST">

            <textarea
                name="message"
                placeholder="Lina'ya bir şey yaz..."
                required
            ></textarea>

            <button type="submit">
                Gönder
            </button>

        </form>

    </div>

</div>

</body>
</html>
"""


class LinaServer(BaseHTTPRequestHandler):

    def send_page(self, html):

        data = html.encode("utf-8")

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(data))
        )

        self.end_headers()

        self.wfile.write(data)

    def do_GET(self):

        self.send_page(HTML)

    def do_POST(self):

        length = int(
            self.headers.get(
                "Content-Length",
                0
            )
        )

        body = self.rfile.read(length).decode(
            "utf-8"
        )

        data = parse_qs(body)

        message = data.get(
            "message",
            [""]
        )[0]

        prompt = brain.create_prompt(
            message
        )

        response_page = f"""
        <!DOCTYPE html>

        <html lang="tr">

        <head>

            <meta charset="UTF-8">

            <meta
                name="viewport"
                content="width=device-width, initial-scale=1.0"
            >

            <title>Lina</title>

        </head>

        <body>

            <h1>👩 Lina</h1>

            <p>
                <strong>İzleyici:</strong>
                {message}
            </p>

            <hr>

            <p>
                <strong>AI Prompt:</strong>
            </p>

            <pre>
{prompt}
            </pre>

            <a href="/">
                ← Geri dön
            </a>

        </body>

        </html>
        """

        self.send_page(response_page)


if __name__ == "__main__":

    server = HTTPServer(
        ("0.0.0.0", 8080),
        LinaServer
    )

    print(
        "Lina AI Live çalışıyor..."
    )

    server.serve_forever()
