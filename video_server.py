from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip
from io import BytesIO
import tempfile
import os

class VideoServer(BaseHTTPRequestHandler):
    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/generate":
            self.send_error(404, "Not found")
            return

        params = parse_qs(parsed.query)
        text = params.get("text", [""])[0]
        if not text:
            self.send_error(400, "Missing text")
            return

        # Read music if provided
        music_data = None
        if 'Content-Length' in self.headers:
            length = int(self.headers['Content-Length'])
            if length > 0:
                music_data = self.rfile.read(length)

        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = None
            audio_clip = None
            duration = 6  # default

            if music_data:
                audio_path = os.path.join(tmpdir, "music.mp3")
                with open(audio_path, "wb") as f:
                    f.write(music_data)

                audio_clip = AudioFileClip(audio_path)
                duration = audio_clip.duration

            # Create a moving text clip
            W, H = 1280, 720
            fontsize = 60
            text_clip = TextClip(text, fontsize=fontsize, color='white', font='Arial')
            text_clip = text_clip.set_position(lambda t: (W * (t / duration) - text_clip.w, 'center')) \
                                 .set_duration(duration)

            video = CompositeVideoClip([text_clip], size=(W, H), bg_color='black') \
                    .set_duration(duration)

            if audio_clip:
                video = video.set_audio(audio_clip)

            output_path = os.path.join(tmpdir, "out.mp4")
            video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')

            with open(output_path, "rb") as f:
                out = f.read()

            self.send_response(200)
            self.send_header("Content-Type", "video/mp4")
            self.send_header("Content-Length", str(len(out)))
            self.end_headers()
            self.wfile.write(out)

def run():
    port = 8080
    print(f"Server running on port {port}")
    HTTPServer(('0.0.0.0', port), VideoServer).serve_forever()

if __name__ == "__main__":
    run()
