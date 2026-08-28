// ============================================================
// 英语学习小助手 - 讯飞语音听写代理（Cloudflare Worker）
// 作用：把讯飞的 APIKey/APISecret 藏到服务端环境变量里，
//       前端只调用本 Worker，网页源码中不再暴露任何凭据。
// ============================================================
//
// 部署后需在 Worker 的环境变量(Setting -> Variables)里配置三个值：
//   XF_APPID   = b6392404
//   XF_KEY     = c757277ed0729711d3b7887a9450b416
//   XF_SECRET  = ZjA3M2ZkZTBmNTVjOTk5Njk3OThkZTRk
//
// 前端调用方式：
//   POST https://<你的worker>.workers.dev/asr
//   body: { "pcm": "<base64 编码的 16kHz/16bit/单声道 PCM>" }
//   返回: { "text": "识别出的英文文本" }
// ============================================================

const XF_HOST = 'iat.xf-yun.com';
const XF_PATH = '/v2/iat';
const CHUNK = 2560; // 1280 个 Int16 = 2560 字节

function bytesToB64(bytes) {
  let bin = '';
  for (let i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
  return btoa(bin);
}

function b64ToBytes(b64) {
  const bin = atob(b64);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return bytes;
}

async function buildAuth(apiKey, apiSecret) {
  const date = new Date().toUTCString();
  const origin = `host: ${XF_HOST}\ndate: ${date}\nGET ${XF_PATH} HTTP/1.1`;
  const key = await crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode(apiSecret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(origin));
  const sigB64 = bytesToB64(new Uint8Array(sig));
  const authOrigin = `api_key="${apiKey}", algorithm="hmac-sha256", headers="host date request-line", signature="${sigB64}"`;
  return {
    date: date,
    auth: btoa(authOrigin),
  };
}

function transcribe(pcmBytes, appId, apiKey, apiSecret) {
  return new Promise((resolve) => {
    let result = '';
    let settled = false;
    const done = () => {
      if (settled) return;
      settled = true;
      try { ws.close(); } catch (e) {}
      resolve(result);
    };

    (async () => {
      const { date, auth } = await buildAuth(apiKey, apiSecret);
      const wsUrl = `wss://${XF_HOST}${XF_PATH}?authorization=${encodeURIComponent(auth)}&date=${encodeURIComponent(date)}&host=${XF_HOST}`;
      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        // 第一帧：业务参数
        ws.send(JSON.stringify({
          common: { app_id: appId },
          business: { language: 'en_us', domain: 'iat', accent: 'mandarin' },
          data: { status: 0, format: 'audio/L16;rate=16000', encoding: 'raw', audio: '' },
        }));
        // 中间帧：音频数据
        for (let off = 0; off < pcmBytes.length; off += CHUNK) {
          const slice = pcmBytes.subarray(off, off + CHUNK);
          ws.send(JSON.stringify({
            data: { status: 1, format: 'audio/L16;rate=16000', encoding: 'raw', audio: bytesToB64(slice) },
          }));
        }
        // 最后一帧：结束标志
        ws.send(JSON.stringify({
          data: { status: 2, format: 'audio/L16;rate=16000', encoding: 'raw', audio: '' },
        }));
      };

      ws.onmessage = (ev) => {
        try {
          const msg = JSON.parse(ev.data);
          if (msg.code !== 0) return;
          const d = msg.data && msg.data.result;
          if (d && d.ws) {
            let t = '';
            d.ws.forEach((seg) => {
              seg.cw && seg.cw.forEach((c) => { t += c.w; });
            });
            result = t;
          }
          if (msg.data && msg.data.status === 2) done();
        } catch (e) {}
      };

      ws.onerror = () => done();
      ws.onclose = () => done();

      // 兜底：10 秒超时
      setTimeout(done, 10000);
    })();
  });
}

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS });
    }

    if (url.pathname === '/asr' && request.method === 'POST') {
      try {
        const { pcm } = await request.json();
        if (!pcm) {
          return new Response(JSON.stringify({ text: '' }), { headers: { ...CORS, 'Content-Type': 'application/json' } });
        }
        const pcmBytes = b64ToBytes(pcm);
        const text = await transcribe(pcmBytes, env.XF_APPID, env.XF_KEY, env.XF_SECRET);
        return new Response(JSON.stringify({ text: text || '' }), {
          headers: { ...CORS, 'Content-Type': 'application/json' },
        });
      } catch (e) {
        return new Response(JSON.stringify({ text: '', error: String(e) }), {
          headers: { ...CORS, 'Content-Type': 'application/json' },
        });
      }
    }

    // 健康检查
    if (url.pathname === '/' || url.pathname === '/health') {
      return new Response(JSON.stringify({ ok: true }), {
        headers: { ...CORS, 'Content-Type': 'application/json' },
      });
    }

    return new Response('not found', { status: 404, headers: CORS });
  },
};
