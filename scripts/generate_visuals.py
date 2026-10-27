from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
BG, PANEL, LINE = '#0B1220', '#121F32', '#263950'
WHITE, MUTED, CYAN, GREEN = '#EDF5FF', '#AABCD3', '#5ADCE6', '#9CE8AF'
FRAMES_PER_STAGE = 40
FRAME_DURATION_MS = 50
STAGES = [
    ('INGEST', 'Start with SSH telemetry', 'ssh_logs.json  /  JSON-based SSH logs', '2,400 events analyzed', ['JSON SSH LOGS', 'SPLUNK ENTERPRISE', 'LOCAL LAB']),
    ('EXAMINE', 'Review authentication outcomes', 'Compare failed and successful events', '1,216 failed  /  612 successful', ['AUTHENTICATION', 'FAILED EVENTS', 'SUCCESSFUL EVENTS']),
    ('INVESTIGATE', 'Follow the suspicious source', 'Source IP: 10.0.0.25', 'Max auth_attempts: 8  /  16 successful logins', ['SOURCE IP', 'REPEATED FAILURES', 'SUCCESSFUL LOGINS']),
    ('DOCUMENT', 'Turn findings into a report', 'Record evidence and reusable detection logic', 'Splunk_SSH_Analysis_Report.pdf', ['EVIDENCE', 'DETECTION LOGIC', 'REPORT']),
]

def font(size, bold=False):
    choices = [Path('C:/Windows/Fonts') / ('segoeuib.ttf' if bold else 'segoeui.ttf'),
               Path('/usr/share/fonts/truetype/dejavu') / ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    for p in choices:
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default(size=size)

def text(d, xy, value, size=20, color=WHITE, bold=False):
    d.text(xy, value, fill=color, font=font(size, bold))

def base(height):
    im = Image.new('RGB', (960, height), BG)
    d = ImageDraw.Draw(im)
    for x in range(0, 960, 40):
        d.line((x, 0, x, height), fill='#101C2C')
    for y in range(0, height, 40):
        d.line((0, y, 960, y), fill='#101C2C')
    return im, d

def hero():
    im, d = base(300)
    d.rounded_rectangle((32, 30, 269, 61), radius=15, fill='#19383F')
    text(d, (47, 33), 'SECURITY OPERATIONS LAB', 15, CYAN, True)
    text(d, (32, 80), 'SSH THREAT HUNTING', 43, bold=True)
    text(d, (34, 143), 'Authentication logs. Suspicious behavior. Evidence.', 24, MUTED)
    for i, (label, value) in enumerate([('PLATFORM', 'Splunk Enterprise'), ('TELEMETRY', 'SSH / JSON'), ('ANALYST', 'Majed Almabadi')]):
        x = 34 + i * 300
        text(d, (x, 213), label, 13, CYAN, True)
        text(d, (x, 237), value, 21)
    im.save(OUT / 'hero.png')

def frame(stage, tick):
    im, d = base(480)
    text(d, (32, 25), 'FROM SSH LOGS TO INVESTIGATION FINDINGS', 21, bold=True)
    text(d, (32, 59), 'ILLUSTRATED WORKFLOW  /  LOCAL SPLUNK LAB', 13, MUTED)
    for i, item in enumerate(STAGES):
        x = 32 + i * 232
        d.rounded_rectangle((x, 102, x + 218, 157), radius=10, fill=PANEL,
                            outline=CYAN if i == stage else LINE, width=2)
        text(d, (x + 15, 118), f'0{i+1}  {item[0]}', 18, CYAN if i == stage else MUTED, True)
    _, title, subtitle, metric, nodes = STAGES[stage]
    text(d, (34, 188), title, 31, bold=True)
    text(d, (34, 237), subtitle, 21, MUTED)
    for i, label in enumerate(nodes):
        x = 34 + i * 310
        d.rounded_rectangle((x, 298, x + 270, 354), radius=8, fill=PANEL, outline=LINE)
        text(d, (x + 14, 316), label, 17, GREEN if i == 2 else WHITE, True)
        if i < 2:
            d.line((x + 278, 326, x + 302, 326), fill=CYAN, width=2)
            p = x + 278 + int(24 * (tick % 20) / 19)
            d.ellipse((p - 3, 323, p + 3, 329), fill=CYAN)
    text(d, (34, 383), metric, 24, CYAN, True)
    text(d, (34, 445), 'ILLUSTRATED INVESTIGATION WORKFLOW', 14, MUTED)
    d.rounded_rectangle((740, 449, 926, 453), radius=2, fill=LINE)
    d.rounded_rectangle((740, 449, 740 + int(186 * (stage * FRAMES_PER_STAGE + tick + 1) / (4 * FRAMES_PER_STAGE)), 453), radius=2, fill=CYAN)
    return im

def overview():
    im, d = base(540)
    text(d, (32, 24), 'INVESTIGATION AT A GLANCE', 29, bold=True)
    text(d, (32, 69), 'Static companion to the animated workflow', 18, MUTED)
    for i, (label, title, subtitle, metric, _) in enumerate(STAGES):
        y = 116 + i * 100
        d.rounded_rectangle((32, y, 928, y + 86), radius=10, fill=PANEL, outline=LINE)
        text(d, (48, y + 13), f'0{i+1}', 30, CYAN, True)
        text(d, (112, y + 10), f'{label}  /  {title}', 21, bold=True)
        text(d, (112, y + 47), metric, 20, MUTED)
    im.save(OUT / 'process.png')

if __name__ == '__main__':
    hero()
    overview()
    frames = [frame(s, t) for s in range(4) for t in range(FRAMES_PER_STAGE)]
    frames[0].save(OUT / 'investigation.gif', save_all=True, append_images=frames[1:],
                   duration=FRAME_DURATION_MS, loop=0, optimize=True, disposal=1)
    preview = Image.new('RGB', (960, 1920), BG)
    for s in range(4):
        preview.paste(frames[s * FRAMES_PER_STAGE], (0, s * 480))
    preview.save(OUT / 'preview.png')
