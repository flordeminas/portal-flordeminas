---
description: Sincronizar layouts e publicar mudanças no Git automaticamente.
---
// turbo-all

Este workflow automatiza a sincronização de cabeçalhos/rodapés e o processo de commit/push.

1. Rodar a sincronização de layout: `python sync_layout.py`
2. Adicionar as mudanças ao git: `git add .`
3. Criar o commit com a mensagem: `git commit -m "chore: sincronização automática de layout e conteúdos"`
4. Subir para o servidor: `git push origin main`
