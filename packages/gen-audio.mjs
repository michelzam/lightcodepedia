/*!
 * gen-audio — studio voices from text (ElevenLabs → static files).
 *
 * Authoring-time tool: scans a markdown page for `.avatar` fences, sends each
 * script line's text to the ElevenLabs TTS API ONCE, and writes the mp3s into
 * docs/assets/audio/. Files are CONTENT-ADDRESSED (name = hash of voice+model+
 * text), so re-running skips every unchanged line — editing one sentence costs
 * exactly one line of credits. The site then serves static files: no API key
 * in the browser, no credits burned by visitors, works offline.
 *
 *   ELEVENLABS_API_KEY=sk_… node packages/gen-audio.mjs docs/components/avatar.md
 *     --voice <voice_id>   (or ELEVEN_VOICE_ID env; a cloned voice id works —
 *                           that's how the site speaks with YOUR voice)
 *     --model <model_id>   default eleven_multilingual_v2 (handles French too)
 *     --out   <dir>        default docs/assets/audio
 *     --write              rewrite the fence in place, adding audio: to each line
 *     --dry                list what would be generated; no API calls, no key needed
 *
 * The avatar plays audio: lines with real waveform lip-sync (built-in face and
 * Rive mouths both follow it) and falls back to browser TTS if a file is missing.
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';
import yaml from 'js-yaml';

const args = process.argv.slice(2);
const opt = (name, def) => {
  const i = args.indexOf('--' + name);
  return i >= 0 && args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : def;
};
const flag = (name) => args.includes('--' + name);

const page   = args.find((a) => !a.startsWith('--') && (args.indexOf(a) === 0 || !args[args.indexOf(a) - 1] || !args[args.indexOf(a) - 1].startsWith('--')));
const voice  = opt('voice', process.env.ELEVEN_VOICE_ID || '');
const model  = opt('model', 'eleven_multilingual_v2');
const outDir = opt('out', 'docs/assets/audio');
const dry    = flag('dry');
const write  = flag('write');
const key    = process.env.ELEVENLABS_API_KEY || '';

if (!page) { console.error('usage: node packages/gen-audio.mjs <page.md> [--voice id] [--model id] [--out dir] [--write] [--dry]'); process.exit(1); }
if (!dry && !key) { console.error('gen-audio: set ELEVENLABS_API_KEY (or use --dry to preview). The key stays on your machine — never in the repo.'); process.exit(1); }
if (!dry && !voice) { console.error('gen-audio: set --voice <voice_id> or ELEVEN_VOICE_ID (your cloned voice id works).'); process.exit(1); }

// name = hash(voice|model|text) → same text = same file = zero new credits
const fileFor = (text) => 'lc-' + createHash('sha1').update(voice + '|' + model + '|' + text).digest('hex').slice(0, 16) + '.mp3';
const webPath = (f) => '/' + join(outDir, f).replace(/^docs\//, '').replace(/\\/g, '/');

async function tts(text, dest) {
  const r = await fetch('https://api.elevenlabs.io/v1/text-to-speech/' + encodeURIComponent(voice) + '?output_format=mp3_44100_128', {
    method: 'POST',
    headers: { 'xi-api-key': key, 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, model_id: model }),
  });
  if (!r.ok) throw new Error('ElevenLabs HTTP ' + r.status + ': ' + (await r.text()).slice(0, 200));
  writeFileSync(dest, Buffer.from(await r.arrayBuffer()));
}

// .avatar fences: ```yaml … ``` followed by {: .avatar … }. The body may not
// cross a fence boundary, and ````-quoted documentation examples are masked
// out so they are never scanned or rewritten.
const FENCE = /```yaml\r?\n((?:(?!```)[\s\S])*?)```\s*\r?\n\{:\s*\.avatar\b([^}]*)\}/g;

// the site's voice manifest — ONE file (seeded in the repo so it always
// exists; per-page files would 404 and dirty the console), same file the
// in-browser 🎙️ studio maintains: { pageSlug: { avatarId: { textHash16:
// file } } } → playback needs no fence config
const slug = page.replace(/^docs\//, '').replace(/\.md$/, '').replace(/\/+$/, '').replace(/\//g, '-') || 'index';
const manPath = join(outDir, 'vox.json');
const textKey = (text) => createHash('sha1').update(text).digest('hex').slice(0, 16);
let manifest = {};
try { manifest = JSON.parse(readFileSync(manPath, 'utf8')) || {}; } catch (e) {}

const src = readFileSync(page, 'utf8');
const masked = src.replace(/````[\s\S]*?````/g, (m) => ' '.repeat(m.length));
let md = src, fences = 0, made = 0, kept = 0, delta = [];

for (const m of masked.matchAll(FENCE)) {
  const body = m[1];
  let cfg;
  try { cfg = yaml.load(body) || {}; } catch (e) { console.error('skip fence (bad YAML): ' + e.message); continue; }
  if (!Array.isArray(cfg.script) || !cfg.script.length) continue;
  fences++;

  const avId = (/#([A-Za-z0-9_-]+)/.exec(m[2]) || [])[1] || '';
  const lines = cfg.script.map((l) => (typeof l === 'string' ? { say: l } : { ...l }));
  for (const l of lines) {
    const text = String(l.say || '').trim();
    if (!text || l.video) continue;                       // video lines carry their own sound
    const f = fileFor(text), dest = join(outDir, f);
    if (existsSync(dest)) { kept++; }
    else if (dry) { made++; console.log('  would generate  ' + f + '  ← "' + text.slice(0, 60) + (text.length > 60 ? '…' : '') + '"'); }
    else {
      mkdirSync(outDir, { recursive: true });
      process.stdout.write('  generating ' + f + ' … ');
      await tts(text, dest);
      console.log('ok');
      made++;
    }
    l.audio = webPath(f);
    if (avId) ((manifest[slug] = manifest[slug] || {})[avId] = manifest[slug][avId] || {})[textKey(text)] = f;
  }

  if (write) {
    cfg.script = lines;
    const newBody = yaml.dump(cfg, { lineWidth: 100 });
    md = md.replace(m[0], '```yaml\n' + newBody + '```\n{: .avatar' + m[2] + '}');
  } else {
    delta.push('```yaml\n' + yaml.dump({ ...cfg, script: lines }, { lineWidth: 100 }) + '```\n{: .avatar' + m[2] + '}');
  }
}

if (!dry && fences && Object.keys(manifest).length) {
  mkdirSync(outDir, { recursive: true });
  writeFileSync(manPath, JSON.stringify(manifest, null, 1));
  console.log('manifest → ' + manPath + ' (playback wires itself; no fence config needed)');
}
if (write && md !== src) { writeFileSync(page, md); console.log('rewrote ' + page + ' with audio: paths'); }
if (!write && delta.length) { console.log('\n─ paste back into ' + page + ' ─\n'); console.log(delta.join('\n\n')); }
console.log('\n' + fences + ' avatar fence(s): ' + made + ' ' + (dry ? 'to generate' : 'generated') + ', ' + kept + ' already cached (no credits spent).');
