#!/usr/bin/env python3
"""Gera o blog estático (blog/) a partir da exportação de artigos do LinkedIn.

Uso:
    python3 -I tools/gerar_blog.py <pasta com os .html da exportação> <raiz do repo>

A exportação vem de LinkedIn → Configurações → Privacidade de dados → Obter uma
cópia dos seus dados → Artigos. Só entram as edições da newsletter "Autista
Empreende" já publicadas. Imagens são descartadas (ficam hospedadas no LinkedIn e
quebrariam a regra de zero requisição externa). Edições em EXCLUIR não são
publicadas (ex.: dados pessoais no texto).
"""
import glob
import html
import json
import os
import re
import sys
import unicodedata
from html.parser import HTMLParser

SITE = "https://autistaempreende.com.br"

# Edições que não vão para o site.
EXCLUIR = {
    # Traz CPF e endereço residencial no primeiro parágrafo.
    "Carta aberta para o prefeito de São Paulo Ricardo Nunes",
}

# Tema de cada edição (pelo início do título).
TEMAS = [
    ("autismo", "Autismo, carreira e inclusão"),
    ("contabil", "Contabilidade, compliance e IA"),
    ("cripto", "Cripto e fintech"),
    ("vida", "Vida, jogos e opinião"),
]
TEMA_POR_TITULO = {
    "5 Erros e 5 Acertos": "autismo",
    "Autismo Não É Cargo": "autismo",
    "O intraempreendedor que o mercado": "autismo",
    "Carta Aberta à Sociedade Brasileira": "autismo",
    "Autista, contador e empreendedor": "autismo",
    "Eu parei de explicar": "autismo",
    "Em tempos de golpe": "autismo",
    "Prevenção à Lavagem": "contabil",
    "LM Notebook": "contabil",
    "A Reforma Tributária": "contabil",
    "Banco Master": "contabil",
    "Como posso trabalhar": "contabil",
    "São 5 da manhã": "contabil",
    "O contador, a IA": "contabil",
    "De uma entrevista ao Bitcoin": "cripto",
    "NovaDAX": "cripto",
    "A VERDADE": "cripto",
    "O rumo que tomamos": "cripto",
    "Como Pokémon": "vida",
    "O que é saber perder": "vida",
    "A “Guerra dos Consoles”": "vida",
    "Minha Primeira Action Figure": "vida",
    "A febre do Pokémon": "vida",
}

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]

PERMITIDAS = {"p", "h2", "h3", "h4", "ul", "ol", "li", "strong", "em", "b", "i",
              "a", "blockquote", "br", "hr"}
DESCARTAR_COM_CONTEUDO = {"figure", "script", "style", "iframe", "img", "svg"}


class Limpador(HTMLParser):
    """Mantém só tags seguras; links só http(s), abrindo em nova aba."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.pular = 0

    def handle_starttag(self, tag, attrs):
        if tag in DESCARTAR_COM_CONTEUDO:
            if tag not in ("img", "br", "hr"):
                self.pular += 1
            return
        if self.pular or tag not in PERMITIDAS:
            return
        if tag == "a":
            href = dict(attrs).get("href", "") or ""
            if href.startswith(("http://", "https://")):
                self.out.append('<a href="%s" target="_blank" rel="noopener noreferrer">' % html.escape(href, quote=True))
            else:
                self.out.append("<a>")
            return
        if tag in ("br", "hr"):
            self.out.append("<%s>" % tag)
            return
        tag = {"b": "strong", "i": "em", "h4": "h3"}.get(tag, tag)
        self.out.append("<%s>" % tag)

    def handle_endtag(self, tag):
        if tag in DESCARTAR_COM_CONTEUDO:
            if tag not in ("img", "br", "hr"):
                self.pular = max(0, self.pular - 1)
            return
        if self.pular or tag not in PERMITIDAS or tag in ("br", "hr"):
            return
        tag = {"b": "strong", "i": "em", "h4": "h3"}.get(tag, tag)
        self.out.append("</%s>" % tag)

    def handle_data(self, data):
        if not self.pular:
            self.out.append(html.escape(data, quote=False))


def limpar(fragmento):
    p = Limpador()
    p.feed(fragmento)
    p.close()
    s = "".join(p.out)
    s = re.sub(r"<p>\s*</p>", "", s)
    s = re.sub(r"<a>(.*?)</a>", r"\1", s, flags=re.S)
    return s.strip()


def slugify(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t.lower()).strip("-")
    partes = t.split("-")
    out = ""
    for p in partes:
        if len(out) + len(p) + 1 > 70:
            break
        out = (out + "-" + p) if out else p
    return out


def data_br(iso):
    a, m, d = iso.split("-")
    return "%d de %s de %s" % (int(d), MESES[int(m) - 1], a)


def tema_de(titulo):
    for k, v in TEMA_POR_TITULO.items():
        if titulo.startswith(k):
            return v
    return "vida"


def ler(pasta):
    arts = []
    for f in glob.glob(os.path.join(pasta, "*.html")):
        s = open(f, encoding="utf-8").read()
        if '<span class="series-title">' not in s:
            continue
        pub = re.search(r'class="published">Published on (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})', s)
        if not pub:
            continue  # rascunho
        titulo = html.unescape(re.search(r"<title>(.*?)</title>", s, re.S).group(1)).strip()
        titulo = re.sub(r"\s+", " ", titulo)
        if titulo in EXCLUIR:
            continue
        link = re.search(r'<h1><a href="([^"]+)"', s)
        ini = s.find("<div>", s.find('class="published"'))
        fim = s.rfind("</div>")
        corpo = limpar(s[ini + 5:fim])
        texto = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", corpo))).strip()
        palavras = len(texto.split())
        resumo = texto[:200].rsplit(" ", 1)[0] + "…" if len(texto) > 200 else texto
        arts.append({
            "titulo": titulo,
            "slug": slugify(titulo),
            "data": pub.group(1),
            "hora": pub.group(2),
            "linkedin": link.group(1) if link else "",
            "corpo": corpo,
            "resumo": resumo,
            "minutos": max(1, round(palavras / 200)),
            "tema": tema_de(titulo),
        })
    arts.sort(key=lambda a: (a["data"], a["hora"]), reverse=True)
    return arts


def ativos(raiz):
    s = open(os.path.join(raiz, "index.html"), encoding="utf-8").read()
    fav = re.search(r'<link rel="icon" href="([^"]+)"', s).group(1)
    marca = re.search(r'<span class="brand-mark">(<svg.*?</svg>)</span>', s, re.S).group(1)
    return fav, marca


CSS = """
:root{
  --bg:#f4f8fc;--surface:#ffffff;--surface-2:#e8f2fa;--ink:#0a2236;--muted:#4a6278;--line:#d6e3ee;
  --brand:#0b4a6f;--brand-ink:#ffffff;--brand-soft:#d7ebf9;--blue:#5fa8db;--cyan:#8fd0f3;--sky:#c9e8fb;
  --sun:#ffcf5c;--night:#061a2b;--night-2:#0b2840;--on-night:#eaf4fb;--on-night-muted:#a3c0d6;--focus:#e0701c;
  --shadow:0 1px 2px rgba(6,26,43,.06),0 18px 40px -18px rgba(6,26,43,.28);--maxw:1180px;
  --font:system-ui,-apple-system,"Segoe UI Variable Display","Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --serif:Charter,"Bitstream Charter","Sitka Text",Cambria,Georgia,serif;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#050f18;--surface:#0c1b28;--surface-2:#091620;--ink:#e7f1f8;--muted:#9fb6c8;--line:#19304a;
    --brand:#8fd0f3;--brand-ink:#04192a;--brand-soft:#11304a;--night:#030b12;--night-2:#0a1f31;
    --shadow:0 1px 2px rgba(0,0,0,.4),0 20px 44px -18px rgba(0,0,0,.75);color-scheme:dark;
  }
}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:var(--font);font-size:1.0625rem;line-height:1.7;background:var(--bg);color:var(--ink);-webkit-font-smoothing:antialiased}
a{color:var(--brand);text-underline-offset:3px}
:focus-visible{outline:3px solid var(--focus);outline-offset:3px;border-radius:8px}
.skip{position:absolute;left:-9999px;top:0;background:var(--sun);color:#061a2b;padding:10px 16px;z-index:60;font-weight:700}
.skip:focus{left:0}
.wrap{max-width:var(--maxw);margin:0 auto;padding-inline:20px}
h1,h2,h3{text-wrap:balance;letter-spacing:-.025em;line-height:1.15}
.top{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--night) 82%,transparent);backdrop-filter:saturate(1.5) blur(16px);-webkit-backdrop-filter:saturate(1.5) blur(16px);border-bottom:1px solid rgba(255,255,255,.08)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:70px}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none;color:var(--on-night)}
.brand-mark{flex:none;display:grid;place-items:center;width:46px;height:46px;border-radius:13px;background:var(--sky);padding:5px}
.brand-mark svg{width:100%;height:auto;display:block}
.brand-txt{display:grid;line-height:1.08}
.brand-txt b{text-transform:uppercase;font-weight:900;font-size:1rem;letter-spacing:.02em}
.brand-txt small{font-size:.6rem;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:var(--on-night-muted)}
.nav{display:flex;align-items:center;gap:4px}
.nav a{color:var(--on-night-muted);text-decoration:none;font-size:.94rem;font-weight:600;padding:8px 13px;border-radius:999px;white-space:nowrap}
.nav a:hover,.nav a[aria-current]{color:var(--on-night);background:rgba(255,255,255,.08)}
.nav .cta{background:var(--sun);color:#061a2b}
@media (max-width:640px){.nav a:not(.cta){display:none}.brand-txt small{display:none}}
.eyebrow{display:inline-flex;align-items:center;gap:10px;font-size:.78rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--brand)}
.eyebrow::before{content:"";width:22px;height:3px;border-radius:3px;background:linear-gradient(90deg,var(--blue),var(--sun))}
.hero{background:var(--night);color:var(--on-night);position:relative;overflow:hidden;isolation:isolate;padding-block:64px 72px}
.hero::before{content:"";position:absolute;inset:0;z-index:-1;background:radial-gradient(55% 80% at 90% 0%,rgba(95,168,219,.4),transparent 60%),radial-gradient(35% 50% at 0% 100%,rgba(255,207,92,.12),transparent 60%)}
.hero .eyebrow{color:var(--cyan)}
.hero h1{color:var(--on-night);font-size:clamp(2rem,5vw,3.4rem);font-weight:900;margin-top:14px;max-width:24ch}
.hero p{color:var(--on-night-muted);max-width:62ch;margin-top:16px;font-size:1.12rem}
.meta{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:20px;color:var(--on-night-muted);font-size:.93rem;font-weight:600}
.meta span{display:inline-flex;align-items:center;gap:8px}
.chip{display:inline-block;font-size:.8rem;font-weight:800;letter-spacing:.06em;padding:5px 12px;border-radius:999px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);color:var(--on-night);text-decoration:none}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}
.chips a:hover{border-color:var(--sun)}
main{padding-block:56px 80px}
.post{max-width:720px;margin:0 auto;padding-inline:20px;font-family:var(--serif);font-size:1.18rem;line-height:1.8}
.post p,.post ul,.post ol,.post blockquote{margin-bottom:1.15em}
.post h2,.post h3{font-family:var(--font);margin:1.8em 0 .6em;font-weight:850}
.post h2{font-size:1.6rem}
.post h3{font-size:1.28rem}
.post ul,.post ol{padding-left:1.3em}
.post li{margin-bottom:.4em}
.post blockquote{border-left:4px solid var(--sun);padding:.2em 0 .2em 1em;color:var(--muted);font-style:italic}
.post hr{border:0;height:1px;background:var(--line);margin:2em 0}
.post a{overflow-wrap:anywhere}
.origem{max-width:720px;margin:40px auto 0;padding:22px 24px;border:1px solid var(--line);border-radius:20px;background:var(--surface);box-shadow:var(--shadow);display:grid;gap:12px;margin-inline:auto}
.origem p{color:var(--muted);font-size:.98rem}
.btns{display:flex;flex-wrap:wrap;gap:10px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:12px 20px;border-radius:999px;font-weight:750;text-decoration:none;font-size:.97rem;border:1.5px solid var(--line);color:var(--ink);background:var(--surface)}
.btn.primary{background:var(--brand);border-color:var(--brand);color:var(--brand-ink)}
.btn:hover{border-color:var(--brand)}
.mais{max-width:var(--maxw);margin:72px auto 0;padding-inline:20px}
.mais h2{font-size:1.6rem;margin:10px 0 22px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
@media (max-width:900px){.grid{grid-template-columns:1fr 1fr}}
@media (max-width:600px){.grid{grid-template-columns:1fr}}
.card{display:flex;flex-direction:column;gap:8px;background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:22px;text-decoration:none;color:var(--ink);box-shadow:var(--shadow);min-width:0}
.card:hover{border-color:var(--blue)}
.card time,.card .min{font-size:.8rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.card h3{font-size:1.12rem}
.card p{color:var(--muted);font-size:.95rem;line-height:1.55}
.card .go{margin-top:auto;font-weight:750;color:var(--brand);font-size:.95rem}
.tema{margin-top:56px}
.tema:first-child{margin-top:0}
.tema h2{font-size:clamp(1.5rem,3vw,2rem);margin:10px 0 22px}
footer{padding-block:40px 56px;color:var(--muted);font-size:.93rem;border-top:1px solid var(--line)}
footer .wrap{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px 24px;align-items:center}
@media (prefers-reduced-motion: no-preference){html{scroll-behavior:smooth}.card{transition:transform .2s ease}.card:hover{transform:translateY(-3px)}}
"""

HEAD = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#061a2b">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self' data:; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'; connect-src 'none'">
<meta name="referrer" content="no-referrer">
<meta name="robots" content="index, follow">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="João Carlos Bueno Abitante">
<link rel="canonical" href="{url}">
<link rel="icon" href="{fav}">
<meta property="og:type" content="{ogtype}">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Autista Empreende">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@libertcontador">
<meta name="twitter:title" content="{ogtitle}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{site}/og-image.png">
{extra}<script type="application/ld+json">
{ld}
</script>
<style>{css}</style>
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<header class="top">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Autista Empreende — página inicial">
      <span class="brand-mark">{marca}</span>
      <span class="brand-txt"><b>Autista Empreende</b><small>Interação e empreendedorismo</small></span>
    </a>
    <nav class="nav" aria-label="Site">
      <a href="/#ferramentas">Ferramentas</a>
      <a href="/blog/"{blogcur}>Blog</a>
      <a href="/#quem">Quem faz</a>
      <a class="cta" href="/#contato">Fale comigo</a>
    </nav>
  </div>
</header>
"""

FOOT = """<footer>
  <div class="wrap">
    <span>Autista Empreende · Interação e empreendedorismo</span>
    <span>Sem cookies, sem analytics, sem rastreadores.</span>
  </div>
</footer>
</body>
</html>
"""


def esc(s):
    return html.escape(s, quote=True)


def card(a, nivel="h3"):
    return ('<a class="card" href="/blog/%s/"><time datetime="%s">%s</time>'
            '<%s>%s</%s><p>%s</p><span class="go">Ler · %d min</span></a>'
            % (a["slug"], a["data"], data_br(a["data"]), nivel, esc(a["titulo"]), nivel, esc(a["resumo"]), a["minutos"]))


def pagina_artigo(a, todos, fav, marca):
    url = "%s/blog/%s/" % (SITE, a["slug"])
    tema = dict(TEMAS)[a["tema"]]
    ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": a["titulo"][:110],
        "description": a["resumo"],
        "datePublished": "%sT%s:00-03:00" % (a["data"], a["hora"]),
        "inLanguage": "pt-BR",
        "mainEntityOfPage": url,
        "url": url,
        "image": SITE + "/og-image.png",
        "articleSection": tema,
        "author": {"@type": "Person", "name": "João Carlos Bueno Abitante",
                   "url": "https://www.linkedin.com/in/joaocarlos1"},
        "publisher": {"@type": "Organization", "name": "Autista Empreende", "url": SITE + "/",
                      "logo": {"@type": "ImageObject", "url": SITE + "/logo.svg"}},
        "isPartOf": {"@type": "Blog", "name": "Blog do Autista Empreende", "url": SITE + "/blog/"},
    }
    if a["linkedin"]:
        ld["sameAs"] = a["linkedin"]
    relacionados = [x for x in todos if x["tema"] == a["tema"] and x is not a][:3]
    if len(relacionados) < 3:
        relacionados += [x for x in todos if x is not a and x not in relacionados][:3 - len(relacionados)]
    h = HEAD.format(
        title=esc(a["titulo"] + " | Autista Empreende"), desc=esc(a["resumo"]), url=url, fav=fav,
        ogtype="article", ogtitle=esc(a["titulo"]), site=SITE, ld=json.dumps(ld, ensure_ascii=False, indent=2),
        css=CSS, marca=marca, blogcur="",
        extra='<meta property="article:published_time" content="%sT%s:00-03:00">\n' % (a["data"], a["hora"]))
    origem = ""
    if a["linkedin"]:
        origem = ('<aside class="origem" aria-label="Sobre este texto"><p>Publicado originalmente na newsletter '
                  '<strong>Autista Empreende</strong>, no LinkedIn. Comentários e conversa continuam por lá.</p>'
                  '<div class="btns"><a class="btn primary" href="%s" target="_blank" rel="noopener noreferrer">Ler e comentar no LinkedIn</a>'
                  '<a class="btn" href="https://www.linkedin.com/in/joaocarlos1" target="_blank" rel="noopener noreferrer">Seguir o autor</a></div></aside>'
                  % esc(a["linkedin"]))
    corpo = """<section class="hero">
  <div class="wrap">
    <a class="eyebrow" href="/blog/#%s" style="text-decoration:none">%s</a>
    <h1>%s</h1>
    <div class="meta"><span><time datetime="%s">%s</time></span><span>%d min de leitura</span><span>João Carlos Bueno Abitante</span></div>
  </div>
</section>
<main id="conteudo">
  <article class="post">
%s
  </article>
  %s
  <section class="mais" aria-labelledby="t-mais">
    <span class="eyebrow">Continue lendo</span>
    <h2 id="t-mais">Mais do blog</h2>
    <div class="grid">%s</div>
    <div class="btns" style="margin-top:24px"><a class="btn" href="/blog/">Ver todos os artigos</a></div>
  </section>
</main>
""" % (a["tema"], esc(tema), esc(a["titulo"]), a["data"], data_br(a["data"]), a["minutos"], a["corpo"], origem,
       "".join(card(x) for x in relacionados))
    return h + corpo + FOOT


def pagina_indice(todos, fav, marca):
    url = SITE + "/blog/"
    ld = {
        "@context": "https://schema.org", "@type": "Blog", "name": "Blog do Autista Empreende", "url": url,
        "inLanguage": "pt-BR",
        "description": "Edições da newsletter Autista Empreende: autismo e carreira, contabilidade, compliance, cripto e vida.",
        "publisher": {"@type": "Organization", "name": "Autista Empreende", "url": SITE + "/"},
        "blogPost": [{"@type": "BlogPosting", "headline": a["titulo"][:110], "url": "%s/blog/%s/" % (SITE, a["slug"]),
                      "datePublished": a["data"]} for a in todos],
    }
    desc = "Textos da newsletter Autista Empreende, de João Carlos Bueno Abitante: autismo e carreira, contabilidade, compliance, cripto e vida."
    h = HEAD.format(title="Blog | Autista Empreende", desc=esc(desc), url=url, fav=fav, ogtype="website",
                    ogtitle="Blog do Autista Empreende", site=SITE, ld=json.dumps(ld, ensure_ascii=False, indent=2),
                    css=CSS, marca=marca, blogcur=' aria-current="page"', extra="")
    chips = "".join('<a class="chip" href="#%s">%s</a>' % (k, esc(n)) for k, n in TEMAS
                    if any(a["tema"] == k for a in todos))
    secoes = ""
    for k, n in TEMAS:
        lista = [a for a in todos if a["tema"] == k]
        if not lista:
            continue
        secoes += ('<section class="tema" id="%s" aria-labelledby="t-%s"><span class="eyebrow">%d artigos</span>'
                   '<h2 id="t-%s">%s</h2><div class="grid">%s</div></section>\n'
                   % (k, k, len(lista), k, esc(n), "".join(card(a) for a in lista)))
    corpo = """<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Newsletter Autista Empreende</span>
    <h1>Blog do Autista Empreende</h1>
    <p>Divulgando o empreendedorismo de pessoas com autismo no Brasil. %d textos publicados na newsletter do LinkedIn, organizados por tema.</p>
    <div class="chips">%s</div>
  </div>
</section>
<main id="conteudo">
  <div class="wrap">
%s  </div>
</main>
""" % (len(todos), chips, secoes)
    return h + corpo + FOOT


def main():
    pasta, raiz = sys.argv[1], sys.argv[2]
    todos = ler(pasta)
    slugs = [a["slug"] for a in todos]
    assert len(slugs) == len(set(slugs)), "slug repetido"
    fav, marca = ativos(raiz)
    marca = re.sub(r'id="m\w"', 'id="mb"', marca).replace('href="#ma"', 'href="#mb"')
    blog = os.path.join(raiz, "blog")
    os.makedirs(blog, exist_ok=True)
    for a in todos:
        d = os.path.join(blog, a["slug"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(pagina_artigo(a, todos, fav, marca))
    open(os.path.join(blog, "index.html"), "w", encoding="utf-8").write(pagina_indice(todos, fav, marca))
    json.dump([{k: a[k] for k in ("titulo", "slug", "data", "tema", "resumo", "minutos", "linkedin")} for a in todos],
              open(os.path.join(blog, "artigos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(todos), "artigos gerados")


if __name__ == "__main__":
    main()
