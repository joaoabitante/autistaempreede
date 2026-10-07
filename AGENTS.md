# AGENTS.md — Autista Empreende

> Contexto para qualquer assistente de IA (Claude Code, Codex, Cursor, Gemini CLI…).
> Autor: João Carlos Bueno Abitante (Contador CRC-SP 320961/O-4).

## Identidade
- **Projeto:** site da iniciativa Autista Empreende — "Interação e empreendedorismo".
- **Repo:** github.com/joaoabitante/autistaempreede
- **Domínio:** autistaempreende.com.br · **Hospedagem:** Vercel (Hostinger como alternativa, via `.htaccess`)
- **Stack:** site estático, página única (`index.html`), sem JavaScript.

## Como trabalhar
- Leia o `README.md` e o `CHANGELOG.md` antes de qualquer mudança.
- O **GitHub é a única fonte da verdade**; a Vercel é espelho (deploy automático no push).
- Nunca faça deploy manual (`vercel --prod`) nem edite no painel da Vercel.
- Commits atômicos (`feat:`, `fix:`, `chore:`, `seo:`) e `CHANGELOG.md` atualizado a cada entrega.
- Nunca commite segredo.

## Princípios não-negociáveis
- **Privacidade/LGPD:** zero coleta de dado pessoal, zero requisição de rede em runtime, zero tracker; `referrer: no-referrer`.
- **Dependências:** autocontido, sem CDN, sem fonte web, sem framework. Imagens embutidas em data URI.
- **Público autista:** baixa estimulação (sem animação chamativa), texto direto, fonte grande, contraste AA nos temas claro e escuro, foco visível.
- **Linguagem:** pt-BR direto e concreto; nunca prometer ferramenta ou serviço que não existe.
- **SEO e segurança:** meta tags, OpenGraph, canonical e JSON-LD; headers em `vercel.json` e `.htaccess` (CSP, HSTS, nosniff, no-referrer, DENY).
