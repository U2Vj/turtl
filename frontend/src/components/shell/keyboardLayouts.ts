// German keyboard layout map for paste-as-keystrokes into a VNC session.

export type KeySpec = {
  code: string;
  shift?: boolean;
  altgr?: boolean;
  dead?: boolean;
  keysym?: number;
};

export const SHIFT_KEYSYM = 0xffe1;
export const ALTGR_KEYSYM = 0xffea;
export const SPACE_KEYSYM = 0x20;

function buildLayout(): Record<string, KeySpec> {
  const map: Record<string, KeySpec> = {
    ' ': { code: 'Space' },
    '\n': { code: 'Enter', keysym: 0xff0d },
    '\t': { code: 'Tab', keysym: 0xff09 },
  };

  for (let i = 0; i <= 9; i++) map[String(i)] = { code: `Digit${i}` };

  // German layout swaps Y and Z relative to US.
  for (let i = 0; i < 26; i++) {
    const lower = String.fromCharCode(0x61 + i);
    const upper = String.fromCharCode(0x41 + i);
    let phys = upper;
    if (upper === 'Y') phys = 'Z';
    else if (upper === 'Z') phys = 'Y';
    map[lower] = { code: `Key${phys}` };
    map[upper] = { code: `Key${phys}`, shift: true };
  }

  Object.assign(map, {
    '!': { code: 'Digit1', shift: true },
    '"': { code: 'Digit2', shift: true },
    '§': { code: 'Digit3', shift: true },
    '$': { code: 'Digit4', shift: true },
    '%': { code: 'Digit5', shift: true },
    '&': { code: 'Digit6', shift: true },
    '/': { code: 'Digit7', shift: true },
    '(': { code: 'Digit8', shift: true },
    ')': { code: 'Digit9', shift: true },
    '=': { code: 'Digit0', shift: true },
    '?': { code: 'Minus', shift: true },
    '-': { code: 'Slash' },
    '_': { code: 'Slash', shift: true },
    '+': { code: 'BracketRight' },
    '*': { code: 'BracketRight', shift: true },
    '#': { code: 'Backslash' },
    "'": { code: 'Backslash', shift: true },
    '<': { code: 'IntlBackslash' },
    '>': { code: 'IntlBackslash', shift: true },
    ',': { code: 'Comma' },
    ';': { code: 'Comma', shift: true },
    '.': { code: 'Period' },
    ':': { code: 'Period', shift: true },
    '@': { code: 'KeyQ', altgr: true },
    '€': { code: 'KeyE', altgr: true },
    '²': { code: 'Digit2', altgr: true },
    '{': { code: 'Digit7', altgr: true },
    '[': { code: 'Digit8', altgr: true },
    ']': { code: 'Digit9', altgr: true },
    '}': { code: 'Digit0', altgr: true },
    '\\': { code: 'Minus', altgr: true },
    '|': { code: 'IntlBackslash', altgr: true },
    '^': { code: 'Backquote', dead: true },
    '°': { code: 'Backquote', shift: true },
    '´': { code: 'Equal', dead: true },
    '`': { code: 'Equal', shift: true, dead: true },
    '~': { code: 'BracketRight', altgr: true },
    'ä': { code: 'Quote' },
    'Ä': { code: 'Quote', shift: true },
    'ö': { code: 'Semicolon' },
    'Ö': { code: 'Semicolon', shift: true },
    'ü': { code: 'BracketLeft' },
    'Ü': { code: 'BracketLeft', shift: true },
    'ß': { code: 'Minus' },
  } as Record<string, KeySpec>);

  return map;
}

export const KEYBOARD_LAYOUT_DE: Record<string, KeySpec> = buildLayout();
