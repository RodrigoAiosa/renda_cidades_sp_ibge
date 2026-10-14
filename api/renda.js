/**
 * Dados de renda dos municípios paulistas a partir da API SIDRA do IBGE.
 *
 *   /api/renda               → ano mais recente com PIB municipal publicado
 *   /api/renda?ano=2021      → um ano específico
 *   /api/renda?anos=1        → lista de anos com PIB municipal disponível
 *   /api/renda?serie=3550308 → série histórica de PIB e PIB per capita de um município
 *
 * Fontes:
 *   PIB dos municípios ............ Tabela 5938, variável 37 (mil R$, preços correntes)
 *   População (estimativas) ....... Tabela 6579, variável 9324
 *   População (Censo 2022) ........ Tabela 4709, variável 93
 *
 * As respostas ficam 24h no cache da CDN da Vercel.
 */
const BASE = "https://apisidra.ibge.gov.br/values";
const SP = "in%20n3%2035"; // todos os municípios do estado de São Paulo

async function sidra(path) {
  let ultimo;
  for (let t = 0; t < 3; t++) {
    try {
      const r = await fetch(`${BASE}${path}`, { headers: { Accept: "application/json" }, signal: AbortSignal.timeout(25000) });
      if (r.ok) {
        const j = await r.json();
        return Array.isArray(j) ? j.slice(1) : []; // a 1ª linha é o cabeçalho
      }
      ultimo = `HTTP ${r.status}`;
      if (r.status < 500 && r.status !== 429) break; // período inexistente etc.
    } catch (e) {
      ultimo = e.name === "TimeoutError" ? "timeout" : e.message;
    }
    await new Promise((ok) => setTimeout(ok, 800 * (t + 1)));
  }
  const err = new Error(`SIDRA ${path}: ${ultimo}`);
  err.sidra = ultimo;
  throw err;
}
const num = (v) => { const n = Number(v); return Number.isFinite(n) ? n : null; };

// População de um ano: Censo em 2022, estimativas nos demais. Se o ano não
// tiver dado, tenta os anos vizinhos (o IBGE não publica estimativas em anos de Censo).
async function populacao(ano, local) {
  const tentativas = [ano, ano - 1, ano + 1, ano - 2, ano + 2];
  for (const a of tentativas) {
    try {
      const linhas = a === 2022
        ? await sidra(`/t/4709/n6/${local}/v/93/p/2022`)
        : await sidra(`/t/6579/n6/${local}/v/9324/p/${a}`);
      const mapa = {};
      linhas.forEach((l) => { const v = num(l.V); if (v) mapa[l.D1C] = v; });
      if (Object.keys(mapa).length) return { ano: a, fonte: a === 2022 ? "Censo 2022 (Tabela 4709)" : `Estimativas ${a} (Tabela 6579)`, mapa };
    } catch { /* tenta o próximo ano */ }
  }
  return null;
}

async function anosDisponiveis() {
  const linhas = await sidra(`/t/5938/n3/35/v/37/p/all`);
  return linhas.map((l) => +l.D3C).filter(Boolean).sort((a, b) => a - b);
}

async function dadosAno(anoPedido) {
  const pib = await sidra(`/t/5938/n6/${SP}/v/37/p/${anoPedido || "last"}`);
  if (!pib.length) throw new Error(`Sem PIB municipal para ${anoPedido || "o ano mais recente"}`);
  const ano = +pib[0].D3C;
  const pop = await populacao(ano, SP);
  const municipios = pib.map((l) => [
    +l.D1C,
    String(l.D1N || "").replace(/\s*-\s*SP$/, ""),
    num(l.V),
    pop ? pop.mapa[l.D1C] || null : null,
  ]).filter((m) => m[2] != null);
  return { ano, populacao: pop ? { ano: pop.ano, fonte: pop.fonte } : null, colunas: ["codigo", "municipio", "pib_mil_reais", "populacao"], municipios };
}

async function serie(cod) {
  const [pib, est, censo] = await Promise.all([
    sidra(`/t/5938/n6/${cod}/v/37/p/all`),
    sidra(`/t/6579/n6/${cod}/v/9324/p/all`).catch(() => []),
    sidra(`/t/4709/n6/${cod}/v/93/p/2022`).catch(() => []),
  ]);
  const pops = {};
  est.forEach((l) => { const v = num(l.V); if (v) pops[+l.D3C] = v; });
  censo.forEach((l) => { const v = num(l.V); if (v) pops[2022] = v; });
  const popDe = (a) => pops[a] || pops[a - 1] || pops[a + 1] || null;
  return {
    codigo: +cod,
    pontos: pib.map((l) => {
      const ano = +l.D3C, mil = num(l.V), p = popDe(ano);
      return { ano, pib_mil_reais: mil, populacao: p, pib_per_capita: mil && p ? Math.round((mil * 1000) / p) : null };
    }).filter((x) => x.pib_mil_reais != null).sort((a, b) => a.ano - b.ano),
  };
}

module.exports = async (req, res) => {
  const q = req.query || {};
  const debug = q.debug === "1";
  try {
    let corpo;
    if (q.anos) corpo = { anos: await anosDisponiveis() };
    else if (q.serie) {
      if (!/^35\d{5}$/.test(String(q.serie))) return res.status(400).json({ erro: "código de município inválido" });
      corpo = await serie(String(q.serie));
    } else {
      const ano = q.ano ? parseInt(q.ano, 10) : null;
      if (q.ano && !(ano >= 2002 && ano <= 2100)) return res.status(400).json({ erro: "ano inválido" });
      corpo = await dadosAno(ano);
    }
    res.setHeader("Cache-Control", "public, s-maxage=86400, stale-while-revalidate=604800");
    return res.status(200).json(corpo);
  } catch (e) {
    return res.status(debug ? 200 : 502).json({ erro: "Não foi possível consultar o IBGE agora.", detalhe: e.message });
  }
};
