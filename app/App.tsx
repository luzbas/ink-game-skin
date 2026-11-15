// Ink Wheel demo page — the player alone, filling the whole window. The controls live on a painted sumi-ink wheel,
// like a game's radial menu: turn the outer ring to scrub, pause for the full wheel, open the chapters as paper cards.
// The skin itself is in src/; this page only feeds it a video.
import { HlsVideo } from '@videojs/react/media/hls-video';
import { VideoPlayer } from '@videojs/react/video';
import { VideoSkin, type Orientation } from '@/video/skin';

// "Nine Strokes" reveal trailer (on Mux): 15 s, five chapters, English captions and a Mux storyboard for the frames on
// the chapter cards. The chapters and captions are served from public/nine-strokes.
const PLAYBACK_ID = 'hE8iC3t2fiIGg9JQj5imNcSPjvlYog7QcVAtJMTj3FY';
const HLS = `https://stream.mux.com/${PLAYBACK_ID}.m3u8`;
const POSTER = `https://image.mux.com/${PLAYBACK_ID}/thumbnail.webp?time=1.6`;
const STORYBOARD = `https://image.mux.com/${PLAYBACK_ID}/storyboard.vtt`;
const CHAPTERS = '/nine-strokes/nine-strokes-chapters.vtt';
const CAPTIONS = '/nine-strokes/nine-strokes-captions-en.vtt';
const TITLE = 'Nine Strokes — reveal trailer';

/** `?shape=tall` previews the 9:16 layouts with this 16:9 video; by default the skin reads the shape from the video. */
function shapeFromUrl(): Orientation | 'auto' {
  if (typeof window === 'undefined') return 'auto';
  const shape = new URLSearchParams(window.location.search).get('shape');
  return shape === 'tall' ? 'portrait' : shape === 'wide' ? 'landscape' : 'auto';
}

export default function InkWheelPage() {
  return (
    // Fixed to the window, so the page's padding does not apply; dvh keeps it to the visible height on phones.
    <section aria-label="Ink Wheel video player" style={{ position: 'fixed', inset: 0, height: '100dvh', background: '#0b0b0b' }}>
      <VideoPlayer poster={POSTER} title={TITLE}>
        <VideoSkin fill progressKey={PLAYBACK_ID} orientation={shapeFromUrl()} style={{ width: '100%', height: '100%', borderRadius: 0 }}>
          <HlsVideo src={HLS} playsInline crossOrigin="anonymous">
            <track kind="chapters" label="Chapters" srcLang="en" src={CHAPTERS} default />
            <track kind="captions" label="English" srcLang="en" src={CAPTIONS} />
            <track kind="metadata" label="thumbnails" src={STORYBOARD} default />
          </HlsVideo>
        </VideoSkin>
      </VideoPlayer>
    </section>
  );
}
